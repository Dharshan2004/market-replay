import ndjson
import numpy as np
from datetime import datetime

def analyze_metrics(filename, epsilon=1e-8):
    # Initializing variables
    update_id_regressions = 0
    delta_t = []
    ask_ge_bid_minus_epsilon = []

    print(f"Analyzing metrics for {filename}")
    with open(filename, 'r') as f:
        data = ndjson.load(f)

    print(f"Symbol: {data[0]['symbol']}, Venue: {data[0]['venue']}, Epsilon: {epsilon}")
    
    # Rows
    rows = len(data)
    print(f"Rows: {rows}")
    
    # Duration using both monotonic and wall timing for sanity check
    if len(data) >= 2:
        # Monotonic duration (authoritative for replay)
        start_mono_ns = data[0]['recv_mono_ns']
        end_mono_ns = data[-1]['recv_mono_ns']
        duration_mono_ns = end_mono_ns - start_mono_ns
        duration_mono_seconds = duration_mono_ns / 1e9
        
        # Wall duration (for sanity check)
        start_wall_ms = data[0]['recv_wall_ms']
        end_wall_ms = data[-1]['recv_wall_ms']
        duration_wall_ms = end_wall_ms - start_wall_ms
        duration_wall_seconds = duration_wall_ms / 1000
        
        print(f"Duration (mono): {duration_mono_seconds:.3f} seconds")
        print(f"Duration (wall): {duration_wall_seconds:.3f} seconds")
        print(f"Clock drift: {abs(duration_mono_seconds - duration_wall_seconds):.3f} seconds")
    else:
        print("Not enough data points for duration calculation")

    # Update ID regressions, delta t, Ask≥Bid-ε check
    if len(data) >= 2:
        for i in range(1, len(data)):
            # Check for update_id regressions (u[i] < u[i-1])
            if data[i]['update_id'] < data[i-1]['update_id']:
                update_id_regressions += 1
            
            # Compute Δt as (mono[i] - mono[i-1]) / 1e6 ms
            delta_t_ns = data[i]['recv_mono_ns'] - data[i-1]['recv_mono_ns']
            delta_t_ms = delta_t_ns / 1e6  # Convert nanoseconds to milliseconds
            delta_t.append(delta_t_ms)

            # Check if ask >= bid - ε
            ask_ge_bid_minus_epsilon.append(data[i]['best_ask_px'] >= (data[i]['best_bid_px'] - epsilon))
    

    delta_t = np.array(delta_t)

    print(f"Update ID regressions: {update_id_regressions}")
    print(f"Delta T mean: {np.mean(delta_t):.3f} ms")
    print(f"Delta T median: {np.median(delta_t):.3f} ms")
    print(f"Delta T 95th percentile: {np.percentile(delta_t, 95):.3f} ms")

    
    # Summary statistics for ask >= bid - ε
    if ask_ge_bid_minus_epsilon:
        valid_count = sum(ask_ge_bid_minus_epsilon)
        total_count = len(ask_ge_bid_minus_epsilon)
        print(f"Ask >= Bid - ε compliance: {valid_count}/{total_count} ({valid_count/total_count*100:.2f}%)")
