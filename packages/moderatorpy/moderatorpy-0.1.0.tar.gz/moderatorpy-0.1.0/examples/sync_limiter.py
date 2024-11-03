from httpx import Client
from moderatorpy import LimiterTransport, RedisBucket

DEFAULT_BASE_URL = "https://public-api.birdeye.so"
DEFAULT_API_KEY = "5c85c95570c74f75bb5c9f0fd2772927"


def main():
    transport = LimiterTransport(
        per_second=10,
        per_minute=100,
        bucket_class=RedisBucket,
        bucket_kwargs={"redis_url": "redis://localhost:6379/0"},
    )
    with Client(base_url=DEFAULT_BASE_URL, transport=transport) as client:
        response = client.get(
            "/defi/tokenlist",
            headers={"x-chain": "solana", "x-api-key": DEFAULT_API_KEY},
            params={
                "limit": 1,
                "sort_by": "v24hChangePercent",
                "offset": 0,
            },
        )
        response_json = response.json()
        print(response_json.get("data", {}).get("total", 0))


if __name__ == "__main__":
    main()
