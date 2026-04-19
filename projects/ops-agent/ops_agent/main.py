import logging
from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from .config import settings
from .db import close_pool, init_pool
from .fusion_conn import start_fusion, stop_fusion
from .routes import context, drafts, tickets

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
