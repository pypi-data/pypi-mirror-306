import time
import threading
from collections import deque
from typing import Callable, Any, List


class Buffr:
    max_capacity: int
    time_interval = float
    _flush_func: Callable[[List], None]
    buffer: deque[Any]
    _lock: threading.Lock
    last_flush_time: float = None
    _t_expiration_clock: threading.Thread
    _expiration_event: threading.Event
    fifo:bool


    def __init__(self, max_capacity: int, time_interval: float, flush_func: Callable[[list], None], fifo:bool=True):
        self.max_capacity = max_capacity
        self.time_interval = time_interval
        self._flush_func = flush_func

        self.buffer = deque()
        self._lock = threading.Lock()
        self.last_flush_time = time.time()

        # Start a background thread for the timer
        self._t_expiration_clock = threading.Thread(target=self._expiration_clock, daemon=True)
        self._t_expiration_clock.start()
        self._expiration_event = threading.Event()
        self.fifo = fifo

    @property
    def size(self) -> int:
        with self._lock:
            return len(self.buffer)


    def add(self, message: Any):
        with self._lock:
            self.buffer.append(message)
            if len(self.buffer) >= self.max_capacity:
                self.flush()

    def _expiration_clock(self):
        time.sleep(0.0001)
        while not self._expiration_event.is_set():
            time.sleep(self.time_interval)
            with self._lock:
                if time.time() - self.last_flush_time >= self.time_interval:
                    self.flush()

    def flush(self):
        if self.buffer is not None:
            messages = list(self.buffer)
            if not self.fifo:
                messages.reverse()
            self.buffer.clear()
            self.last_flush_time = time.time()
            self._flush_func(messages)

    def stop(self):
        self._expiration_event.set()  # Signal the thread to stop
        self._t_expiration_clock.join()  # Ensure thread has finished
