import asyncio
import collections
import contextlib
import time
from typing import Dict

base = contextlib.AbstractAsyncContextManager
_current_task = asyncio.current_task


class RateLimiter(base):
    """Context manager class to rate limit certain API requests."""

    def __init__(
        self,
        max_rate: float,
        time_period: float = 60,
        loop: asyncio.AbstractEventLoop | None = None,
    ):
        """Initializes an instance of the `RateLimiter`.

        Args:
            max_rate (float): The maximum allowed rate of an action per time period.
            time_period (float, optional): The time period in seconds over which the maximum
                rate applies. Defaults to 60.
            loop (asyncio.AbstractEventLoop | None, optional): A reference to the event loop.
                Defaults to None.
        """

        self._loop = loop
        self._max_level = max_rate
        self._rate_per_second = max_rate / time_period
        self._level = 0.0
        self._last_check = 0.0
        self._waiters: Dict[asyncio.Task, asyncio.Future] = collections.OrderedDict()

    def has_capacity(self, amount: float = 1):
        """Returns true if capacity under the current max rate is available.

        Args:
            amount (float, optional): The number of available slots of capacity to check for.
                Defaults to 1.

        Returns:
            bool: True if capacity is available.
        """

        self._leak()
        requested = self._level + amount

        if requested < self._max_level:
            for future in self._waiters.values():
                if not future.done():
                    future.set_result(True)

                    break

        return self._level + amount <= self._max_level

    async def acquire(self, amount: float = 1):
        """Aquire the next available capacity to perform an action. If rate limit has been reached,
        the request for capacity will be delayed until under the rate.

        Args:
            amount (float, optional): The number of slots of capacity to aquire. Defaults to 1.

        Raises:
            ValueError: If the amount of requested capacity is over the maximum allowed.
        """

        if amount > self._max_level:
            raise ValueError("Can't acquire more than the rate limiter capacity")

        loop = self._loop or asyncio.get_event_loop()
        task = _current_task(loop)
        assert task is not None

        while not self.has_capacity(amount):
            future = loop.create_future()
            self._waiters[task] = future

            try:
                await asyncio.wait_for(
                    asyncio.shield(future), 1 / self._rate_per_second * amount
                )
            except asyncio.TimeoutError:
                pass

            future.cancel()

        self._waiters.pop(task, None)
        self._level += amount

        return None

    async def __aenter__(self):
        await self.acquire()

        return None

    async def __aexit__(self, exc_type, exc, tb):
        return None

    def _leak(self):
        if self._level:
            elapsed = time.time() - self._last_check
            decrement = elapsed * self._rate_per_second
            self._level = max(self._level - decrement, 0)

        self._last_check = time.time()
