
import logging
import pandas as pd
from src.back_worker_db.inside_trade_db import InsideTradeDB,InsideTradeData
import akshare as ak

class InsideTradeWorker:
    def __init__(self, db:InsideTradeDB):
        self.db = db
    
    def download_inside_trade(self):
        stock_inner_trade_xq_df = ak.stock_inner_trade_xq()
        for index, row in stock_inner_trade_xq_df.iterrows():
            data = InsideTradeData.model_construct()
            data.stock_code = row['股票代码']
            data.stock_name = row['股票名称']
            data.change_date = row['变动日期']
            data.change_person = row['变动人']
            data.change_shares = row['变动股数']
            data.avg_price = row['成交均价']
            data.shares_after_change = row['变动后持股数']
            if not pd.isna(row['与董监高关系']):
                data.relation_to_executive = row['与董监高关系']
            data.executive_position = row['董监高职务']

            try:
                self.db.insert(data)
            except Exception as e:
                logging.error(f"insert data {data} error {e}")
                return False
        
        return True
            
            
