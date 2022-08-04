import click

from .helpers.init_db import init_db


@click.group()
# pylint: disable-next=invalid-name
def db():
    pass


@db.command()
def init():
    """Create the Timescale DB with AggreGator (hyper)tables"""
    init_db()
