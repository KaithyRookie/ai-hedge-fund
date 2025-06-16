from src.back_worker_db.financial_indicators_db import FinancialIndicatorsDB, FinancialIndicatorsData
import akshare as ak
import logging
import datetime

class FinancialIndicatorsWorker:
    def __init__(self, db: FinancialIndicatorsDB):
        self.db = db
    
    def download_financial_indicators_from_report(self, ticker:str):
        latest_date = self.db.get_latest_date(ticker)
        start_year = '1700'
        if latest_date:
            start_year = latest_date.year
        
        stock_financial_analysis_indicator_df = ak.stock_financial_analysis_indicator(symbol=ticker, start_year=start_year)

        if stock_financial_analysis_indicator_df is None:
            return
        for index, row in stock_financial_analysis_indicator_df.iterrows():
            # row 转 dict
            row_dict = row.to_dict()
            # 转换为 datetime.date 类型
            date = datetime.datetime.strptime(row['日期'], '%Y-%m-%d').date()
            financial_indicators_data = FinancialIndicatorsData.from_raw_data(raw_data=row_dict, ticker=ticker, report_date=date)
            try:
                data = self.db.create(financial_indicators_data)            
                logging.info(f'create financial indicators data for {ticker} {date} success, id: {data.id}')
            except Exception as e:
                logging.error(f'create financial indicators data for {ticker} {date} failed, error: {e}')
                return False
        return True