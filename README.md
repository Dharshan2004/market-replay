# Market Replay CLI

## Data Schema

### @bookTicker Normalized Schema

The collected market data follows this normalized schema:

| Field | Type | Description |
|-------|------|-------------|
| `venue` | string | Exchange/venue identifier |
| `symbol` | string | Trading pair symbol |
| `recv_wall_ms` | int | Wall clock timestamp in milliseconds (for plotting & human-time) |
| `recv_mono_ms` | int | Monotonic timestamp in milliseconds (for replay timing) |
| `update_id` | int | Payload update ID (for gap checks) |
| `best_bid_px` | float | Best bid price |
| `best_bid_qty` | float | Best bid quantity |
| `best_ask_px` | float | Best ask price |
| `best_ask_qty` | float | Best ask quantity |

This schema ensures consistent data structure across different venues and enables reliable replay functionality.