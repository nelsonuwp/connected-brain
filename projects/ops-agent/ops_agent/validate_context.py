"""CLI: build T-context for one issue key (no web server)."""

from __future__ import annotations

import asyncio
import json
import sys

from .context.t_context import build_t_context
from .db import close_pool, init_pool
from .fusion_conn import start_fusion, stop_fusion


async def _run(issue_key: str) -> int:
    await init_pool()
    start_fusion()
    try:
        from .db import get_pool

        pool = await get_pool()
        ctx = await build_t_context(pool, issue_key)
    finally:
        stop_fusion()
        await close_pool()

    slim = {k: v for k, v in ctx.items() if k != "prompt_block"}
    print(json.dumps(slim, indent=2, default=str))
    pb = ctx.get("prompt_block") or ""
    print("\n--- prompt_block (first 2000 chars) ---\n")
    print(pb[:2000])
    if len(pb) > 2000:
        print(f"\n... ({len(pb) - 2000} more chars)")
    return 0


def main() -> None:
    if len(sys.argv) < 2:
        print("Usage: python3 -m ops_agent.validate_context APTUM-12345", file=sys.stderr)
        sys.exit(2)
    sys.exit(asyncio.run(_run(sys.argv[1])))


if __name__ == "__main__":
    main()
