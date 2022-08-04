import csv
from datetime import datetime

import requests
from aggregator.db.engine.engine_utils import get_db_engine
from aggregator.db.models.market import Market
from aggregator.db.models.trades import Trades
from sqlalchemy.orm import Session


def populate_market_data():
    start = int(datetime.strptime("01/01/2020", '%m/%d/%Y').timestamp())
    end = int(datetime.strptime("12/29/2021", '%m/%d/%Y').timestamp())
    headers = {
        # pylint: disable-next=line-too-long
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36',
    }
    engine = get_db_engine()
    with Session(engine) as sess, requests.Session() as req:
        symbols = sess.query(Trades.symbol).distinct().all()
        for symbol, *_ in symbols:
            # pylint: disable-next=line-too-long
            url = f"https://query1.finance.yahoo.com/v7/finance/download/{symbol}?period1={start}&period2={end}&interval=1d&events=history&includeAdjustedClose=true"
            yahoo = req.get(url, headers=headers)
            lines = (line for line in yahoo.iter_lines(decode_unicode=True))
            history = csv.DictReader(lines)
            for row in history:
                data = Market(
                    symbol=symbol,
                    date=row['Date'],
                    open=row['Open'],
                    high=row['High'],
                    low=row['Low'],
                    close=row['Close'],
                    adjusted_close=row['Adj Close'],
                    volume=row['Volume'])
                sess.add(data)
            sess.commit()
