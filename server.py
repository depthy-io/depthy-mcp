"""Depthy MCP Server — exposes Depthy market-structure intelligence as MCP tools."""

import json
import os

import httpx
from mcp.server.fastmcp import FastMCP

API_KEY = os.environ.get("DEPTHY_API_KEY", "")
BASE_URL = os.environ.get("DEPTHY_BASE_URL", "https://depthy.io")

if not API_KEY:
    raise RuntimeError(
        "DEPTHY_API_KEY environment variable is required.\n"
        "Get a free API key at https://depthy.io"
    )

mcp = FastMCP(
    "Depthy",
    instructions="Real-time crypto order book depth, liquidity walls, liquidation clusters, and Polymarket signals.",
)


def _normalize(symbol: str) -> str:
    """Normalize symbol to uppercase, append -PERP if needed."""
    s = symbol.upper().strip()
    if not s.endswith("-PERP"):
        s += "-PERP"
    return s


async def _api_get(path: str, params: dict | None = None) -> dict:
    """Call the Depthy REST API and return parsed JSON."""
    async with httpx.AsyncClient(base_url=BASE_URL, timeout=30) as client:
        resp = await client.get(
            path,
            params=params,
            headers={"Authorization": f"Bearer {API_KEY}"},
        )
        if resp.status_code == 401:
            return {"error": "Invalid API key. Get a free key at https://depthy.io"}
        if resp.status_code == 403:
            return {"error": "This endpoint requires a Pro key. Upgrade at https://depthy.io"}
        if resp.status_code == 429:
            return {"error": "Rate limit exceeded. Free tier: 30 req/min, 100/day"}
        if resp.status_code >= 500:
            return {"error": "Depthy API temporarily unavailable"}
        resp.raise_for_status()
        return resp.json()


# ── Hyperliquid tools ──────────────────────────────────────────────


@mcp.tool()
async def list_symbols(exchange: str = "hyperliquid") -> str:
    """List all available trading symbols on an exchange.

    Args:
        exchange: Exchange name (default: hyperliquid)
    """
    data = await _api_get(f"/v1/symbols", {"exchange": exchange})
    return json.dumps(data, indent=2)


@mcp.tool()
async def get_depth(symbol: str, levels: int = 20) -> str:
    """Get order book depth and bid/ask imbalance for a Hyperliquid perpetual.

    Args:
        symbol: Trading pair (e.g. BTC, ETH, SOL)
        levels: Number of price levels (1-50, default 20)
    """
    data = await _api_get(f"/v1/depth/hyperliquid/{_normalize(symbol)}", {"levels": levels})
    return json.dumps(data, indent=2)


@mcp.tool()
async def get_depth_recent(symbol: str, minutes: int = 30) -> str:
    """Get recent depth snapshots for a symbol over the last N minutes.

    Args:
        symbol: Trading pair (e.g. BTC, ETH, SOL)
        minutes: Lookback window in minutes (1-120, default 30)
    """
    data = await _api_get(
        f"/v1/depth/hyperliquid/{_normalize(symbol)}/recent", {"minutes": minutes}
    )
    return json.dumps(data, indent=2)


@mcp.tool()
async def get_walls(symbol: str, min_size_usd: float = 100000) -> str:
    """Find large resting orders (walls) in the order book.

    Args:
        symbol: Trading pair (e.g. BTC, ETH, SOL)
        min_size_usd: Minimum wall size in USD (default 100000)
    """
    data = await _api_get(
        f"/v1/walls/hyperliquid/{_normalize(symbol)}", {"min_size_usd": min_size_usd}
    )
    return json.dumps(data, indent=2)


@mcp.tool()
async def get_liquidation_clusters(symbol: str) -> str:
    """Get liquidation cluster zones where cascading liquidations are likely.

    Args:
        symbol: Trading pair (e.g. BTC, ETH, SOL)
    """
    data = await _api_get(f"/v1/liquidations/hyperliquid/{_normalize(symbol)}/clusters")
    return json.dumps(data, indent=2)


@mcp.tool()
async def get_market(symbol: str) -> str:
    """Get comprehensive market overview: price, volume, funding rate, open interest.

    Args:
        symbol: Trading pair (e.g. BTC, ETH, SOL)
    """
    data = await _api_get(f"/v1/market/hyperliquid/{_normalize(symbol)}")
    return json.dumps(data, indent=2)


@mcp.tool()
async def get_oi_change(symbol: str) -> str:
    """Get open interest changes over recent time windows.

    Args:
        symbol: Trading pair (e.g. BTC, ETH, SOL)
    """
    data = await _api_get("/api/oi/change", {"symbol": _normalize(symbol)})
    return json.dumps(data, indent=2)


@mcp.tool()
async def compare_symbols(symbols: str) -> str:
    """Compare depth and liquidity metrics across multiple symbols. Requires Pro key.

    Args:
        symbols: Comma-separated list of symbols (e.g. "BTC,ETH,SOL")
    """
    data = await _api_get(f"/v1/compare/hyperliquid", {"symbols": symbols})
    return json.dumps(data, indent=2)


# ── Polymarket tools ───────────────────────────────────────────────


@mcp.tool()
async def list_pm_markets(market_type: str = "", limit: int = 20) -> str:
    """List active Polymarket prediction markets.

    Args:
        market_type: Filter by type (e.g. crypto_15m, sports). Empty for all.
        limit: Max number of markets to return (default 20)
    """
    params = {"limit": limit}
    if market_type:
        params["market_type"] = market_type
    data = await _api_get("/v1/polymarket/markets/active", params)
    return json.dumps(data, indent=2)


@mcp.tool()
async def get_pm_signals(limit: int = 10) -> str:
    """Get latest Polymarket trading signals from smart-money analysis.

    Args:
        limit: Max number of signals to return (default 10)
    """
    data = await _api_get("/v1/pm/signals/latest", {"limit": limit})
    return json.dumps(data, indent=2)


@mcp.tool()
async def get_pm_top_wallets(limit: int = 10) -> str:
    """Get top-performing Polymarket wallets by profit.

    Args:
        limit: Max number of wallets to return (default 10)
    """
    data = await _api_get("/v1/pm/wallets/top", {"limit": limit})
    return json.dumps(data, indent=2)
