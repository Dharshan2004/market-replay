import ndjson
import threading
import queue
import os
from datetime import datetime

class DataLogger:
    def __init__(self):
        self.data_queue = queue.Queue()
        self.writer_thread = None
        self.running = False
        self.output_file = f"data/data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.ndjson"
        os.makedirs(os.path.dirname(self.output_file), exist_ok=True)
    
    def start(self):
        self.running = True
        self.writer_thread = threading.Thread(target=self._writer_thread)
        self.writer_thread.start()
        print(f"Data logger started, writing to {self.output_file}")
    
    def stop(self):
        self.running = False
        if self.writer_thread and self.writer_thread.is_alive():
            self.writer_thread.join(timeout=5)
        print(f"Data logger stopped")
    
    def write_data(self, normalized_data):
        try:
            self.data_queue.put(normalized_data)
        except queue.Full:
            print(f"Warning: Data queue is full, dropping data")
    
    def _writer_thread(self):
        with open(self.output_file, 'w') as f:
            writer = ndjson.writer(f)
            while self.running:
                try:
                    data = self.data_queue.get(timeout=1)
                    writer.writerow(data)
                    f.flush()
                    self.data_queue.task_done()
                    
                except queue.Empty:
                    continue
                except Exception as e:
                    print(f"Error writing data: {e}")
                    break
        
        while not self.data_queue.empty():
            try:
                data = self.data_queue.get_nowait()
                with open(self.output_file, 'a') as f:
                    writer = ndjson.writer(f)
                    writer.writerow(data)
                self.data_queue.task_done()
            except queue.Empty:
                break
            except Exception as e:
                print(f"Error writing remaining data: {e}")
                break

# Global logger instance
logger = None

def start_logger():
    global logger
    if logger is None:
        logger = DataLogger()
    logger.start()
    return logger

def stop_logger():
    global logger
    if logger:
        logger.stop()
        logger = None

def write_data(normalized_data):
    global logger
    if logger:
        logger.write_data(normalized_data)
    else:
        print("Warning: Logger not started, data not saved")