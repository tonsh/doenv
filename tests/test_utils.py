import os


def test_is_test_env():
    assert os.getenv("APP_ENV") == "test"
