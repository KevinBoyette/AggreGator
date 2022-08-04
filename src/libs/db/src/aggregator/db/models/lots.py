from sqlalchemy import Column, Date, Enum, Float, Integer, String
from sqlalchemy.orm import relationship

from .asset_type import AssetType
from .base import Base


class Lots(Base):
    __tablename__ = 'lots'

    id = Column(Integer, primary_key=True, autoincrement=True)
    symbol = Column(String)
    date = Column(Date)
    price = Column(Float)
    type = Column(Enum(AssetType))
    trades = relationship("Trades", single_parent=True)
