import threading
import time
from collections import deque
from typing import Callable, Any, List, Optional


class Buffr:
    """
    A buffer that stores messages and flushes them when a maximum capacity is reached
    or after a specified time interval.

    Parameters
    ----------
    max_capacity : int
        The maximum number of messages the buffer can hold before automatically flushing.
    flush_func : Callable[[list], None]
        The function to call with the list of messages when the buffer flushes.
    buffer_ttl : Optional[float], optional
        The time-to-live (TTL) for messages in the buffer, in seconds. If specified,
        the buffer will flush after this time interval has passed since the last flush.
    fifo : bool, default=True
        Determines the order in which messages are flushed. If True, messages are
        flushed in First-In-First-Out (FIFO) order. If False, they are flushed
        in Last-In-First-Out (LIFO) order.

    Attributes
    ----------
    max_capacity : int
        The maximum number of messages the buffer can hold.
    buffer : deque[Any]
        The internal deque structure holding the buffered messages.
    size : int
        The current number of messages in the buffer.
    """

    max_capacity: int
    buffer: deque[Any]
    _flush_func: Callable[[List], None]
    _lock: threading.Lock
    _last_flush_time: float = None
    _t_expiration_clock: threading.Thread
    _expiration_event: threading.Event
    _time_interval = float
    _fifo: bool

    def __init__(
        self,
        max_capacity: int,
        flush_func: Callable[[list], None],
        buffer_ttl: Optional[float] = None,
        fifo: bool = True,
    ):
        """
        Initializes the Buffr instance, setting up the flush function, maximum capacity, and an optional expiration timer. Starts a background thread to monitor and flush the buffer based on the TTL.
        """

        self.max_capacity = max_capacity
        self._buffer_ttl = buffer_ttl
        self._flush_func = flush_func

        self.buffer = deque()
        self._lock = threading.Lock()
        self._last_flush_time = time.time()

        # Start a background thread for the timer
        self._t_expiration_clock = threading.Thread(
            target=self._expiration_clock, daemon=True
        )
        self._t_expiration_clock.start()
        self._expiration_event = threading.Event()
        self._fifo = fifo

    def __str__(self) -> str:
        return (
            f"<Buffr capacity={self.size}/{self.max_capacity}, TTL={self._buffer_ttl}s>"
        )

    @property
    def size(self) -> int:
        """
        Returns the current number of messages in the buffer.

        Returns
        -------
        int
            The number of messages currently stored in the buffer.
        """

        with self._lock:
            return len(self.buffer)

    def add(self, message: Any):
        """
        Adds a message to the buffer. If the buffer reaches its maximum capacity,
        it automatically flushes the messages.

        Parameters
        ----------
        message : Any
            The message or data to add to the buffer.
        """
        with self._lock:
            self.buffer.append(message)
            if len(self.buffer) >= self.max_capacity:
                self.flush()

    def _expiration_clock(self):
        """
        Monitors the buffer for expiration based on the specified TTL. If the buffer
        is not flushed within the TTL, this method triggers an automatic flush.

        This method is intended to be run in a background thread.
        """
        time.sleep(0.0001)
        # check every bufferttl / 10 seconds but not more frequent than 1 second.
        check_interval = self._buffer_ttl / 10
        while not self._expiration_event.is_set():
            time.sleep(check_interval)
            with self._lock:
                if time.time() - self._last_flush_time >= self._buffer_ttl:
                    self.flush()

    def flush(self):
        """
        Flushes all messages from the buffer. The messages are passed to the
        specified flush function in either FIFO or LIFO order based on the `fifo` flag.

        If the buffer is empty, this method does nothing.
        """
        if self.buffer is not None:
            messages = list(self.buffer)
            if not self._fifo:
                messages.reverse()
            self.buffer.clear()
            self._last_flush_time = time.time()
            self._flush_func(messages)

    def stop(self):
        """
        Stops the expiration clock thread, allowing for a clean shutdown of the Buffr instance.

        This method should be called before deleting the Buffr instance to prevent
        the background thread from running indefinitely.
        """
        self._expiration_event.set()  # Signal the thread to stop
        self._t_expiration_clock.join()  # Ensure thread has finished
