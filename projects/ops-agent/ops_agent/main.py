import logging
from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from .config import settings
from .db import close_pool, init_pool
from .fusion_conn import start_fusion, stop_fusion
from .routes import context, drafts, status, tickets

logging.basicConfig(
    level=getattr(logging, settings.log_level.upper(), logging.INFO),
    format="%(asctime)s %(levelname)-8s %(name)s: %(message)s",
)
logger = logging.getLogger(__name__)

_HERE = Path(__file__).parent


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_pool()
    start_fusion()
    # Warm the sentence-transformer so first user request isn't slow.
    # This downloads ~440MB on the very first run of this process; from then on
    # it's a local disk cache (~/.cache/huggingface/…).
    from .embedder import get_model, MODEL_NAME
    try:
        get_model()
        logger.info("Embedder warm (%s)", MODEL_NAME)
    except Exception:
        logger.exception("Embedder failed to warm — sidebar will fall back to recency ordering")
    logger.info("ops-agent started at http://%s:%d", settings.ops_agent_host, settings.ops_agent_port)
    yield
    stop_fusion()
    await close_pool()
    logger.info("ops-agent shut down")


app = FastAPI(title="ops-agent", lifespan=lifespan)

app.mount("/static", StaticFiles(directory=str(_HERE / "static")), name="static")
app.include_router(tickets.router)
app.include_router(context.router)
app.include_router(drafts.router)
app.include_router(status.router)


def main() -> None:
    import uvicorn
    uvicorn.run(
        "ops_agent.main:app",
        host=settings.ops_agent_host,
        port=settings.ops_agent_port,
        reload=True,
    )


if __name__ == "__main__":
    main()
