from src.back_worker_db.stock_valuation_db import StockValuationDB, StockValuationData
import akshare as ak
import pandas as pd
import logging
from datetime import datetime

class StockValuationWorker:
    def __init__(self, db: StockValuationDB):
        self.db = stock_valuation_db

    def download_stock_valuation(self, ticker: str):
        """
        下载股票估值数据并保存到数据库中
        """
        latest_data_date_str = self.db.get_latest_stock_valuation_date(ticker)
        if latest_data_date_str is None:
            latest_data_date_str = '1970-01-01'  # 如果没有数据，从1970-01-01开始下载
            # 如果没有数据，从1970-01-01开始下载
        latest_data_date = datetime.strptime(latest_data_date_str, '%Y-%m-%d').date()
        stock_value_em_df = ak.stock_value_em(symbol=ticker)
        for index, row in stock_value_em_df.iterrows():
            value_date_str = row['数据日期']
            value_date = datetime.strptime(value_date_str, '%Y-%m-%d').date()
            if value_date < latest_data_date:  # 跳过已经下载的数据
                continue
            data = StockValuationData.model_construct()
            data.ticker = ticker
            data.data_date = value_date
            if not pd.isna(row['当日收盘价']):  
                data.closing_price = row['当日收盘价']
            if not pd.isna(row['当日涨跌幅']):
                data.daily_change = row['当日涨跌幅']
            if not pd.isna(row['总市值']):
                data.market_cap = row['总市值']
            if not pd.isna(row['流通市值']):
                data.flow_market_cap = row['流通市值']
            if not pd.isna(row['总股本']):
                data.total_share = row['总股本']
            if not pd.isna(row['流通股本']):
                data.float_share = row['流通股本']
            if not pd.isna(row['PE(TTM)']):
                data.pe_ttm_ratio = row['PE(TTM)']
            if not pd.isna(row['PE(静)']):
                data.pe_static_ratio = row['PE(静)']
            #市净率
            if not pd.isna(row['市净率']):
                data.pb_ratio = row['市净率']
            #PEG值
            if not pd.isna(row['PEG值']):
                data.peg_ratio = row['PEG值']
            #市现率
            if not pd.isna(row['市现率']):
                data.pc_ratio = row['市现率']
            #市销率
            if not pd.isna(row['市销率']):
                data.ps_ratio = row['市销率']
            
            try:
                self.db.add_stock_valuation(data)
                logging.info(f"添加股票估值数据: {ticker} {value_date}")
            except Exception as e:
                logging.error(f"添加股票估值数据失败: {e}")
                return False    
        return True

