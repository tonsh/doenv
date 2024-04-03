import os
from unittest import TestCase
from redis import Redis
from testcontainers.redis import RedisContainer


def redis_client() -> Redis:
    host = os.environ.get("REDIS_SERVER_HOST", "dotenv-redis")
    port = int(os.environ.get("REDIS_SERVER_PORT", 6379))
    db = int(os.environ.get("REDIS_SERVER_DB", 0))

    return Redis(host=host, port=port, db=db, encoding="utf-8", decode_responses=True)


def get_users() -> list[str]:
    return redis_client().lrange("test.user.names", 0, -1)  # type: ignore


class TestRedisClient(TestCase):

    def setUp(self) -> None:
        self.container = RedisContainer(image="redis:latest")
        self.container.start()

        # mock redis server to redis testcontainer
        os.environ["REDIS_SERVER_HOST"] = self.container.get_container_host_ip()
        os.environ["REDIS_SERVER_PORT"] = self.container.get_exposed_port(6379)

        self.redis_client = redis_client()
        return super().setUp()

    def tearDown(self) -> None:
        self.container.stop()
        return super().tearDown()

    def init_users(self):
        """ Initialize users in redis """
        users = ["Alice", "Bob", "Charlie"]
        for user in users:
            self.redis_client.lpush("test.user.names", user)

        return users

    def test_get_users(self):
        users = self.init_users()

        for user in get_users():
            assert user in users
