# Depthy MCP Server

[![YellowMCP Reliability](https://yellowmcp.com/api/v1/servers/depthy/badge)](https://yellowmcp.com/servers/depthy)

MCP server that gives AI assistants access to real-time crypto market structure data from [Depthy](https://depthy.io) — order book depth, liquidity walls, liquidation clusters, and Polymarket signals.

**Remote endpoint:** `https://depthy.io/mcp/sse`

## Quick Start

### Install

```bash
pip install depthy-mcp
```

### Get an API Key

Sign up for a free API key at [depthy.io](https://depthy.io).

### Claude Desktop Configuration

Add to your Claude Desktop config (`~/Library/Application Support/Claude/claude_desktop_config.json` on macOS):

```json
{
  "mcpServers": {
    "depthy": {
      "command": "python",
      "args": ["-m", "mcp_server"],
      "env": {
        "DEPTHY_API_KEY": "dk_live_your_key_here"
      }
    }
  }
}
```

### Cursor Configuration

Add to `.cursor/mcp.json` in your project:

```json
{
  "mcpServers": {
    "depthy": {
      "command": "python",
      "args": ["-m", "mcp_server"],
      "env": {
        "DEPTHY_API_KEY": "dk_live_your_key_here"
      }
    }
  }
}
```

## Available Tools

| Tool | Description | Free Tier |
|---|---|---|
| `list_symbols` | List all tradable symbols | Yes |
| `get_depth` | Order book depth & bid/ask imbalance | Yes (T1) |
| `get_depth_recent` | Depth snapshots over last N minutes | Yes (T1) |
| `get_walls` | Large resting orders in the book | Yes (T1) |
| `get_liquidation_clusters` | Liquidation cascade risk zones | Yes (T1) |
| `get_market` | Price, volume, funding, open interest | Yes (T1) |
| `get_oi_change` | Open interest changes | Yes |
| `compare_symbols` | Multi-symbol comparison | Pro+ |
| `list_pm_markets` | Active Polymarket markets | Yes |
| `get_pm_signals` | Polymarket smart-money signals | Yes |
| `get_pm_top_wallets` | Top Polymarket wallets by profit | Yes |

## Example Queries

Once configured, ask your AI assistant:

- "What's the current order book depth for BTC?"
- "Are there any large walls near the current ETH price?"
- "Where are the liquidation clusters for SOL?"
- "Compare liquidity depth for BTC, ETH, and SOL"
- "What are the latest Polymarket signals?"

## Environment Variables

| Variable | Required | Default | Description |
|---|---|---|---|
| `DEPTHY_API_KEY` | Yes | — | Your Depthy API key |
| `DEPTHY_BASE_URL` | No | `https://depthy.io` | API base URL |

## Links

- [Depthy](https://depthy.io) — Platform & signup
- [API Documentation](https://depthy.io/api-docs) — Full endpoint reference
- [Python SDK](https://github.com/depthy-io/depthy-python) — For programmatic access

## License

MIT
