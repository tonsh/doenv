import os
from unittest import mock
from redis import Redis


def redis_client() -> Redis:
    host = os.environ.get("REDIS_SERVER_HOST", "dotenv-redis")
    port = int(os.environ.get("REDIS_SERVER_PORT", 6379))
    db = int(os.environ.get("REDIS_SERVER_DB", 0))

    return Redis(host=host, port=port, db=db, encoding="utf-8", decode_responses=True)


def get_users() -> list[str]:
    return redis_client().lrange("test.user.names", 0, -1)  # type: ignore


@mock.patch("tests.test_redis.redis_client")
def test_get_users(mock_redis_client):
    mock_redis_client.return_value.lrange.return_value = ["Alice", "Bob", "Charlie"]
    assert get_users() == ["Alice", "Bob", "Charlie"]
