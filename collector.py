import websocket
import json
import threading
import time
from normalizer import normalize_data
from logger import start_logger, stop_logger, write_data

ticker_symbol = None
capture_duration = None

def on_message(ws, message):
    data = json.loads(message)
    normalized_data = normalize_data(data)
    write_data(normalized_data)
    print(f"Normalized data: {normalized_data}")

def on_error(ws, error):
    print(f"Error: {error}")
    

def on_close(ws, close_status_code, close_msg):
    print(f"WebSocket connection closed: {close_status_code} - {close_msg}")

def on_open(ws):
    global ticker_symbol
    print("Connection opened")
    subscribe_message = {
        "method": "SUBSCRIBE",
        "params": [f"{ticker_symbol}@bookTicker"],
        "id": 1
    }
    ws.send(json.dumps(subscribe_message))
    print(f"Subscribed to {ticker_symbol}@bookTicker")

def on_ping(ws, message):
    print(f"Received ping: {message}")

def on_pong(ws, message):
    print(f"Received pong: {message}")

def start_collector(ticker, duration):
    global ticker_symbol, capture_duration
    start_logger()
    ticker_symbol = ticker.lower()
    capture_duration = int(duration)
    
    print(f"Starting collector for {ticker_symbol} for {capture_duration} seconds")
    
    socket = 'wss://stream.binance.com:9443/ws'
    ws = websocket.WebSocketApp(socket,
                                on_message=on_message,
                                on_error=on_error,
                                on_close=on_close,
                                on_open=on_open,
                                on_ping=on_ping,
                                on_pong=on_pong)
    
    # Start WebSocket in a separate thread
    ws_thread = threading.Thread(target=ws.run_forever)
    ws_thread.daemon = True
    ws_thread.start()
    
    # Wait for the specified duration
    time.sleep(capture_duration)
    
    stop_logger()
    # Close the WebSocket connection
    ws.close()
    print(f"Data capture completed for {ticker_symbol}")

if __name__ == "__main__":
    # For direct execution, you can still use it with hardcoded values
    start_collector("btcusdt", "10")