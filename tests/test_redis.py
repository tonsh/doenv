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


def add_user(user: str) -> None:
    redis_client().lpush("test.user.names", user)


class TestRedisClient(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.container = RedisContainer(image="redis:latest")
        cls.container.start()

        # mock redis server to redis testcontainer
        os.environ["REDIS_SERVER_HOST"] = cls.container.get_container_host_ip()
        os.environ["REDIS_SERVER_PORT"] = cls.container.get_exposed_port(6379)
        super().setUpClass()

    @classmethod
    def tearDownClass(cls):
        cls.container.stop()
        super().tearDownClass()

    def setUp(self) -> None:
        self.redis_client = redis_client()
        self.users = self.init_users()
        return super().setUp()

    def tearDown(self) -> None:
        self.redis_client.delete("test.user.names")
        return super().tearDown()

    def init_users(self):
        """ Initialize users in redis """
        users = ["Alice", "Bob", "Charlie"]
        for user in users:
            self.redis_client.lpush("test.user.names", user)

        return users

    def test_get_users(self):
        users = get_users()
        assert len(users) == len(self.users)

        for user in get_users():
            assert user in self.users

    def test_add_user(self):
        add_user("David")

        users = get_users()
        assert "David" in users
        assert len(users) == len(self.users) + 1
