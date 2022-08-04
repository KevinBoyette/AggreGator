from sqlalchemy import Column, Date, Enum, Float, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from .asset_type import AssetType
from .base import Base

TABLENAME = 'trades'


class Trades(Base):
    __tablename__ = TABLENAME

    id = Column(Integer, primary_key=True, autoincrement=True)
    symbol = Column(String)
    quantity = Column(Float)
    date = Column(Date, nullable=False, primary_key=True)
    price = Column(Float)
    type = Column(Enum(AssetType))
    lot_id = Column(Integer, ForeignKey('lots.id'))
    lot = relationship("Lots")


# https://docs.timescale.com/api/latest/hypertable/create_hypertable/#optional-arguments
hypertable = f"SELECT create_hypertable('{TABLENAME}', 'date');"
