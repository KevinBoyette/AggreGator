import re
from operator import itemgetter
from typing import TypedDict

from sqlalchemy import engine_from_config


class DbCredentials(TypedDict):
    username: str
    password: str
    host: str
    port: str


def is_includable(line: str) -> bool:
    stripped = line.strip()
    return stripped and not stripped.startswith('#')


def get_dot_env() -> dict[str, str]:
    with open(".env", encoding="utf-8") as dotenv:
        lines = (line.strip() for line in dotenv if is_includable(line))
        pairs = (re.split(r"\s*=\s*", line, 1) for line in lines)
        return dict(pairs)


def get_db_config(credentials: DbCredentials):
    username, password, host, port = itemgetter(
        "username", "password", "host", "port")(credentials)
    return {
        "sqlalchemy.url": f"postgresql://{username}:{password}@{host}:{port}/aggregator",
        "sqlalchemy.echo": True,
    }


def get_db_engine():
    dotenv = get_dot_env()
    config = get_db_config(dotenv)
    return engine_from_config(config)
