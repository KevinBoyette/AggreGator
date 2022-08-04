import click

from .helpers.populate_market_data import populate_market_data


@click.group()
def market():
    pass


@market.command()
def populate():
    """Identify islands and fetch+insert market data for each day each security is held"""
    populate_market_data()
