from sqlalchemy import Column, Date, Float, Integer, String

from .base import Base

TABLENAME = 'market'


class Market(Base):
    __tablename__ = TABLENAME

    id = Column(Integer, primary_key=True, autoincrement=True)
    symbol = Column(String)
    date = Column(Date, nullable=False, primary_key=True)
    open = Column(Float)
    high = Column(Float)
    low = Column(Float)
    close = Column(Float)
    adjusted_close = Column(Float)
    volume = Column(Integer)


# https://docs.timescale.com/api/latest/hypertable/create_hypertable/#optional-arguments
hypertable = f"SELECT create_hypertable('{TABLENAME}', 'date');"
