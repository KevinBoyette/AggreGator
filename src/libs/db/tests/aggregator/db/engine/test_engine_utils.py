# pylint: disable=redefined-outer-name
# https://github.com/PyCQA/pylint/issues/6531
from unittest import mock

import pytest
from aggregator.db.engine.engine_utils import (get_db_config, get_db_engine,
                                               get_dot_env, is_includable)
from sqlalchemy.engine.url import URL


@pytest.mark.parametrize("line", [
    "a",
    "  a   ",
    "a=b",
    " a=b ",
    "doesn't really matter",
])
def test_is_includable(line):
    assert is_includable(line)


@pytest.mark.parametrize("line", [
    "# commented=out",
    "  # commented=out   ",
    "",
    "  ",
    "\n",
])
def test_not_is_includable(line):
    assert not is_includable(line)


@pytest.fixture
def dot_env_file():
    return """
  # username=sandyCrocodile
  username=a11yGator
    # password=drowssap
  password=12345678
  host=db.server.lan
  port=5432

  """


@pytest.fixture
def dot_env_dict():
    return {
        "username": "a11yGator",
        "password": "12345678",
        "host": "db.server.lan",
        "port": "5432",
    }


def test_get_dot_env(dot_env_file, dot_env_dict):
    with mock.patch("builtins.open", mock.mock_open(read_data=dot_env_file)):
        assert get_dot_env() == dot_env_dict


def test_get_db_config(dot_env_dict):
    assert get_db_config(dot_env_dict) == {
        "sqlalchemy.url": "postgresql://a11yGator:12345678@db.server.lan:5432/aggregator",
        "sqlalchemy.echo": True,
    }


def test_get_db_config_invalid():
    with pytest.raises(KeyError):
        get_db_config({})


def test_get_db_engine(dot_env_file):
    with mock.patch("builtins.open", mock.mock_open(read_data=dot_env_file)):
        assert get_db_engine().url == URL.create("postgresql", "a11yGator",
                                                 "12345678", "db.server.lan", "5432", "aggregator")
