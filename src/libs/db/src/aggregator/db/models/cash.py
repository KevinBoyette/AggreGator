from sqlalchemy import Column, Date, Float, Integer, String

from .base import Base

TABLENAME = 'cash'


class Cash(Base):
    __tablename__ = TABLENAME

    id = Column(Integer, primary_key=True, autoincrement=True)
    type = Column(String)
    date = Column(Date, nullable=False, primary_key=True)
    amount = Column(Float)
    lhs = Column(String)
    rhs = Column(String)


# https://docs.timescale.com/api/latest/hypertable/create_hypertable/#optional-arguments
hypertable = f"SELECT create_hypertable('{TABLENAME}', 'date');"
