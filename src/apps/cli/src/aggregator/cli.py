import click

from .subcommands.db import db
from .subcommands.market import market


def main():
  cli = click.CommandCollection(sources=[db, market])
  cli()


if __name__ == '__main__':
  main()
