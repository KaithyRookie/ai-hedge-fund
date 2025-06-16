from src.back_worker_db.stock_price_db import StockPriceDB
from src.back_worker_db.stock_db import StockType
from src.data.models import Price
import logging
import akshare as ak
import datetime

class StockPriceWorker:
    def __init__(self, stock_price_db: StockPriceDB):
        self.stock_price_db = stock_price_db

    def get_stock_price(self, ticker: str, stock_type: StockType):
        # 获取股票最近一日的价格
        price = self.stock_price_db.get_latest_stock_price_by_ticker(ticker, stock_type)
        start_time = '19700101'
        if price is not None:
            start_time = price.time
        end_time = datetime.now().strftime('%Y%m%d')
        prices = []
        
        if stock_type == StockType.A_SHARE:
            df = ak.stock_zh_a_hist(symbol=ticker, adjust='hfq', period='daily', start_date=start_time, end_date=end_time)
            for index, row in df.iterrows():
                price_date = row['日期']
                price_date = price_date.replace('-', '')
                price = Price(
                    time=price_date,
                    open=row['开盘'],
                    high=row['最高'],
                    low=row['最低'],
                    close=row['收盘'],
                    volume=row['成交量']
                )
                prices.append(price)
        elif stock_type == StockType.B_SHARE:
            df = ak.stock_zh_b_daily(symbol=ticker, adjust='hfq', period='daily', start_date=start_time, end_date=end_time)
            for index, row in df.iterrows():
                price_date = row['date']
                price_date = price_date.replace('-', '')
                price = Price(
                    time=price_date,
                    open=row['open'],
                    high=row['high'],
                    low=row['low'],
                    close=row['close'],
                    volume=row['volume']
                )
                prices.append(price)
        
        elif stock_type == StockType.US_SHARE:
            df = ak.stock_us_hist(symbol=ticker, adjust='hfq', period='daily', start_date=start_time, end_date=end_time)
            for index, row in df.iterrows():
                price_date = row['日期']
                price_date = price_date.replace('-', '')
                price = Price(
                    time=price_date,
                    open=row['开盘'],
                    high=row['最高'],
                    low=row['最低'],
                    close=row['收盘'],
                    volume=row['成交量']
                )
                prices.append(price)
        elif stock_type == StockType.HK_SHARE:
            df = ak.stock_hk_hist(symbol=ticker, adjust='hfq', period='daily', start_date=start_time, end_date=end_time)
            for index, row in df.iterrows():
                price_date = row['日期']
                price_date = price_date.replace('-', '')
                price = Price(
                    time=price_date,
                    open=row['开盘'],
                    high=row['最高'],
                    low=row['最低'],
                    close=row['收盘'],
                    volume=row['成交量']
                )
                prices.append(price)    
        else:
            logging.error(f"不支持的股票类型: {stock_type}")
            return
        self.stock_price_db.insert_stock_price(prices, ticker, stock_type)

