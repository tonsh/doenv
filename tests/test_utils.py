import os


def test_is_test_env():
    assert os.getenv("APP_ENV") == "test"


def test_is_dev_env():
    assert os.getenv("APP_ENV") != "dev"
