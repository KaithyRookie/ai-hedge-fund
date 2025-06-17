
import logging
import pandas as pd
from src.back_worker_db.inside_trade_db import InsideTradeDB,InsideTradeData
import akshare as ak

from src.back_worker_db.stock_db import StockDB


class InsideTradeWorker:
    def __init__(self, db:InsideTradeDB, stock_db: StockDB):
        self.db = db
        self.stock_db = stock_db
    
    def download_inside_trade(self):
        stock_inner_trade_xq_df = ak.stock_inner_trade_xq()
        for index, row in stock_inner_trade_xq_df.iterrows():
            data = InsideTradeData.model_construct()
            data.stock_name = row['股票名称']
            if not pd.isna(row['股票代码']):
                data.stock_code = row['股票代码']
            elif data.stock_name != "":
                stock = self.stock_db.get_stock_by_ticker_name(data.stock_name)
                if stock:
                    data.stock_code = stock.ticker
                else:
                    logging.error(f"stock name: {data.stock_name} not found")
                    continue
            data.change_date = row['变动日期']
            data.change_person = row['变动人']
            data.change_shares = row['变动股数']
            data.avg_price = row['成交均价']
            data.shares_after_change = row['变动后持股数']
            if not pd.isna(row['与董监高关系']):
                data.relation_to_executive = row['与董监高关系']
            data.executive_position = row['董监高职务']

            try:
                if not self.db.check_record_exists(data.stock_code, data.change_date, data.change_person):
                    self.db.insert(data)
            except Exception as e:
                logging.error(f"insert data {data} error {e}")
                return False
        
        return True
            
            
