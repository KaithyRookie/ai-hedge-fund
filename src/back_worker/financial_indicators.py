from src.back_worker_db.company_facts_db import CompanyFactDB
from src.back_worker_db.financial_indicators_db import FinancialIndicatorsDB, FinancialIndicatorsData
import akshare as ak
import logging
from datetime import datetime

class FinancialIndicatorsWorker:
    def __init__(self, db: FinancialIndicatorsDB):
        self.db = db

    def download_financial_indicators_from_report(self, ticker:str) -> bool:
        latest_date = self.db.get_latest_date(ticker)
        start_year = '1900'
        if latest_date:
            start_year = latest_date.year + 1

        stock_financial_analysis_indicator_df = ak.stock_financial_analysis_indicator(symbol=ticker, start_year=start_year)

        if stock_financial_analysis_indicator_df is None:
            return False
        for index, row in stock_financial_analysis_indicator_df.iterrows():
            # row 转 dict
            row_dict = row.to_dict()
            date = row['日期']
            if latest_date and latest_date >= date:
                continue
            financial_indicators_data = FinancialIndicatorsData.from_raw_data(raw_data=row_dict, ticker=ticker, report_date=date)
            try:
                self.db.create(financial_indicators_data)
                logging.info(f'create financial indicators data for {ticker} {date} success')
            except Exception as e:
                logging.error(f'create financial indicators data for {ticker} {date} failed, error: {e}')
                return False
        return True