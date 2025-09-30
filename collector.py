import websocket
import json
import threading
import datetime

message_count = 0

def on_message(ws, message):
    global message_count
    data = json.loads(message)
    message_count += 1
    print(f"Received message: {message}")

def on_error(ws, error):
    print(f"Error: {error}")
    

def on_close(ws, close_status_code, close_msg):
    time_now = datetime.datetime.now()
    time_diff = time_now - start_time
    print(f"Time taken: {time_diff}")
    print(f"Message count: {message_count}")
    print(f"Message rate: {message_count / time_diff.total_seconds()}")
    print(f"WebSocket connection closed: {close_status_code} - {close_msg}")

def on_open(ws):
    print("Connection opened")
    subscribe_message = {
        "method": "SUBSCRIBE",
        "params": ["btcusdt@bookTicker"],
        "id": 1
    }
    ws.send(json.dumps(subscribe_message))
    print(f"Subscribed to btcusdt@bookTicker")
    global start_time
    start_time = datetime.datetime.now()

def on_ping(ws, message):
    print(f"Received ping: {message}")

def on_pong(ws, message):
    print(f"Received pong: {message}")

if __name__ == "__main__":
    socket = 'wss://stream.binance.com:9443/ws'
    ws = websocket.WebSocketApp(socket,
                                on_message=on_message,
                                on_error=on_error,
                                on_close=on_close,
                                on_open=on_open,
                                on_ping=on_ping,
                                on_pong=on_pong)
    ws.run_forever()