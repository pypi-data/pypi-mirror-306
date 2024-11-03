import time
from typing import Optional

from pyrate_limiter import AbstractBucket, RateItem
from redis import Redis


class RedisBucket(AbstractBucket):
    """Redis-backed bucket for rate limiting"""

    def __init__(
        self,
        rates=None,
        redis_client: Optional[Redis] = None,
        redis_url: str = "redis://localhost:6379/0",
        key_prefix: str = "httpx_ratelimit:",
    ):
        """
        Initialize Redis bucket

        Args:
            rates: Rate limits to apply
            redis_client: Optional pre-configured Redis client
            redis_url: Redis connection URL if client not provided
            key_prefix: Prefix for Redis keys
        """
        super().__init__()
        self.rates = rates
        self.failing_rate = None  # Required by AbstractBucket
        self.redis = redis_client or Redis.from_url(redis_url)
        self.key_prefix = key_prefix

    def _get_key(self, item_name: str, rate_idx: int) -> str:
        """Generate Redis key for an item and rate combination"""
        return f"{self.key_prefix}{item_name}:rate{rate_idx}"

    def put(self, item: RateItem) -> bool:
        """Add an item to the bucket, return False if rate limit exceeded"""
        if not self.rates:
            return True

        # Check each rate limit before adding
        for idx, rate in enumerate(self.rates):
            key = self._get_key(item.name, idx)
            now = time.time()
            cutoff = now - rate.interval

            # Count items in window
            pipe = self.redis.pipeline()
            pipe.zremrangebyscore(key, "-inf", cutoff)
            pipe.zcount(key, cutoff, "+inf")
            _, count = pipe.execute()

            if int(count) + item.weight > rate.limit:
                self.failing_rate = rate
                return False

        # If we get here, we can add the item
        pipe = self.redis.pipeline()
        for idx, rate in enumerate(self.rates):
            key = self._get_key(item.name, idx)
            pipe.zadd(key, {str(item.timestamp): item.weight})
            pipe.expire(key, int(rate.interval * 1.5))
        pipe.execute()

        self.failing_rate = None
        return True

    def count(self, item_name: str = None) -> int:
        """Count items in the smallest rate limit window"""
        if not self.rates:
            return 0

        # Use the first (smallest) rate window
        rate = self.rates[0]
        key = self._get_key(item_name, 0)

        # Get current time
        now = time.time()
        # Calculate cutoff time for the rate window
        cutoff = now - rate.interval

        # Remove old entries and count remaining ones
        pipe = self.redis.pipeline()
        pipe.zremrangebyscore(key, "-inf", cutoff)
        pipe.zcount(key, cutoff, "+inf")
        _, count = pipe.execute()

        return int(count)

    def clear(self) -> None:
        """Clear all rate limit data"""
        # Find and delete all keys with our prefix
        keys = self.redis.keys(f"{self.key_prefix}*")
        if keys:
            self.redis.delete(*keys)

    def flush(self) -> None:
        """Clear tokens for all rate limits"""
        # Find and delete all keys with our prefix
        keys = self.redis.keys(f"{self.key_prefix}*")
        if keys:
            self.redis.delete(*keys)
        self.failing_rate = None  # Required by AbstractBucket

    def leak(self, current_timestamp: Optional[int] = None) -> int:
        """Remove outdated items from the bucket"""
        if not self.rates:
            return 0

        # Use first rate window
        key = self._get_key("default", 0)  # Using "default" as base item name
        if current_timestamp:
            cutoff = current_timestamp - self.rates[0].interval
            # Remove old entries
            self.redis.zremrangebyscore(key, "-inf", cutoff)

        count = self.redis.zcard(key)
        return int(count)

    def peek(self, index: int) -> Optional[RateItem]:
        """Peek at rate-item at specific index"""
        if not self.rates:
            return None

        key = self._get_key("default", 0)  # Using "default" as base item name
        # Get item at reverse index
        items = self.redis.zrange(key, -index - 1, -index - 1, withscores=True)
        if not items:
            return None

        # Convert Redis response to RateItem
        _, timestamp = items[0]
        return RateItem("default", int(timestamp))

    def acquire(self, item: RateItem) -> bool:
        """
        Try to acquire a token for the given item.
        Returns True if acquired, False if rate limit exceeded.
        """
        if not self.rates:
            return True

        # Add the item
        self.put(item)

        # Check each rate limit
        for idx, rate in enumerate(self.rates):
            key = self._get_key(item.name, idx)
            now = time.time()
            cutoff = now - rate.interval

            # Count items in window
            count = self.redis.zcount(key, cutoff, "+inf")

            # If count exceeds rate limit
            if count > rate.limit:
                self.failing_rate = rate  # Set the failing rate
                return False

        return True
