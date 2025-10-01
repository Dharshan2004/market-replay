# Market Replay CLI

A high-precision market data capture and analysis tool for cryptocurrency exchanges, designed for accurate replay and timing analysis.

## Features

- **High-precision timing**: Nanosecond-accurate monotonic timestamps for reliable replay
- **Real-time data capture**: WebSocket-based streaming from Binance Spot
- **Comprehensive metrics**: Timing analysis, data integrity checks, and market compliance validation
- **CLI interface**: Easy-to-use command-line tools for data capture and analysis

## Installation

```bash
pip install -r requirements.txt
```

## Usage

### Data Capture

Capture real-time market data from Binance:

```bash
python3 main.py datacapture --ticker btcusdt --time 10
```

**Parameters:**
- `--ticker`: Trading pair symbol (e.g., btcusdt, ethusdt)
- `--time`: Capture duration in seconds

**Example Output:**
```
Starting collector for btcusdt for 10 seconds
Connection opened
Subscribed to btcusdt@bookTicker
First message received, starting 10s timer
Normalized data: {'venue': 'binance-spot', 'symbol': 'BTCUSDT', 'recv_wall_ms': 1759295523244, 'recv_mono_ns': 8046576053666, 'update_id': 77130729886, 'best_bid_px': 114707.37, 'best_bid_qty': 13.74864, 'best_ask_px': 114707.38, 'best_ask_qty': 3.6567}
...
Data capture completed for btcusdt
```

**Output Files:**
- Data is saved to `data/data_YYYYMMDD_HHMMSS.ndjson`
- Each line contains a JSON object with normalized market data

### Metrics Analysis

Analyze captured data for timing precision, data integrity, and market compliance:

```bash
python3 main.py metrics --filename data/data_20251001_131155.ndjson
```

**Parameters:**
- `--filename`: Path to the captured data file

**Example Output:**
```
Analyzing metrics for data/data_20251001_131155.ndjson
Symbol: BTCUSDT, Venue: binance-spot, Epsilon: 1e-08
Rows: 4092
Duration (mono): 10.097 seconds
Duration (wall): 10.097 seconds
Clock drift: 0.000 seconds
Update ID regressions: 0
Delta T mean: 2.468 ms
Delta T median: 0.069 ms
Delta T 95th percentile: 13.298 ms
Ask >= Bid - ε compliance: 4091/4091 (100.00%)
```

**Metrics Explained:**

| Metric | Description | Expected Values |
|--------|-------------|-----------------|
| **Rows** | Total number of data points captured | Varies by capture duration |
| **Duration (mono)** | Monotonic clock duration (authoritative for replay) | Should match capture time |
| **Duration (wall)** | Wall clock duration (for sanity check) | Should be close to mono duration |
| **Clock drift** | Difference between wall and mono clocks | Should be < 1 second |
| **Update ID regressions** | Count of times update_id decreased (should be 0) | 0 (indicates proper ordering) |
| **Delta T mean** | Average time between consecutive updates | ~2-10 ms for active markets |
| **Delta T median** | Median time between updates | > 0 (indicates nanosecond precision) |
| **Delta T 95th percentile** | 95th percentile of update intervals | < 100 ms for good performance |
| **Ask >= Bid - ε compliance** | Percentage of valid ask/bid relationships | 100% (market integrity) |

## Data Schema

### @bookTicker Normalized Schema

The collected market data follows this normalized schema:

| Field | Type | Description |
|-------|------|-------------|
| `venue` | string | Exchange/venue identifier |
| `symbol` | string | Trading pair symbol |
| `recv_wall_ms` | int | Wall clock timestamp in milliseconds (for plotting & human-time) |
| `recv_mono_ns` | int | Monotonic timestamp in nanoseconds (authoritative for replay/Δt) |
| `update_id` | int | Payload update ID (for gap checks) |
| `best_bid_px` | float | Best bid price |
| `best_bid_qty` | float | Best bid quantity |
| `best_ask_px` | float | Best ask price |
| `best_ask_qty` | float | Best ask quantity |

This schema ensures consistent data structure across different venues and enables reliable replay functionality.

## Timing Precision

The system uses two timing mechanisms:

1. **Monotonic Clock (`recv_mono_ns`)**: Nanosecond-precision, monotonic timestamps that are immune to system clock adjustments. This is the authoritative timing source for replay and Δt calculations.

2. **Wall Clock (`recv_wall_ms`)**: Millisecond-precision wall clock timestamps for human-readable time and plotting.

## Data Quality Validation

The metrics analysis performs several quality checks:

- **Timing Precision**: Ensures nanosecond precision is working (median Δt > 0)
- **Data Ordering**: Verifies update_id sequence integrity (regressions = 0)
- **Clock Consistency**: Compares wall vs monotonic clock drift
- **Market Integrity**: Validates ask >= bid - ε constraint (100% compliance expected)

## File Structure

```
market-replay/
├── main.py              # CLI entry point
├── collector.py         # WebSocket data capture
├── normalizer.py        # Data normalization
├── metrics.py           # Analysis and metrics
├── logger.py            # Data logging utilities
├── requirements.txt     # Python dependencies
├── data/               # Captured data files
│   └── data_*.ndjson   # Timestamped data files
└── README.md           # This file
```