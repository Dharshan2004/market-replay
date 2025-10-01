import time

def normalize_data(data):
    # Get timestamps at receipt
    recv_wall_ms = int(time.time() * 1000)  # UTC milliseconds (wall clock)
    recv_mono_ns = int(time.perf_counter() * 1e9)  # Monotonic nanoseconds (authoritative for replay/Δt)
    
    venue = 'binance-spot'
    symbol = str(data['s'])
    update_id = int(data['u'])
    best_bid_px = float(data['b'])
    best_bid_qty = float(data['B'])
    best_ask_px = float(data['a'])
    best_ask_qty = float(data['A'])
    
    return {
        'venue': venue,
        'symbol': symbol,
        'recv_wall_ms': recv_wall_ms,
        'recv_mono_ns': recv_mono_ns,
        'update_id': update_id,
        'best_bid_px': best_bid_px,
        'best_bid_qty': best_bid_qty,
        'best_ask_px': best_ask_px,
        'best_ask_qty': best_ask_qty
    }