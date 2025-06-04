from src.back_worker_db.stock_db import StockDB,StockType
import akshare as ak
import logging

class StockWorker:
    def __init__(self, stock_db: StockDB):
        self.stock_db = stock_db
    
    def get_all_a_stocks(self):
        """获取沪深京A股所有股票信息，将股票信息添加到数据库中
        """
        try:    
            df = ak.stock_zh_a_spot_em()
        except Exception as e:
            logging.error(f"获取股票数据失败: {e}")
            return

        for index, row in df.iterrows():
            ticker = row['代码']
            name = row['名称']
            # 检查股票是否已经存在
            try:
                if self.stock_db.get_stock_by_ticker(ticker) is None:
                    self.stock_db.add_stock(ticker, name, StockType.A_SHARE)
                    logging.info(f"添加股票: {ticker} {name}")
                else:
                    logging.info(f"股票已存在: {ticker} {name}")
            except Exception as e:
                logging.error(f"添加A股股票失败: {e}")
        logging.info("沪深京A股所有股票信息添加完成")

        try:
            df= ak.stock_zh_b_spot_em()
        except Exception as e:
            logging.error(f"获取股票数据失败: {e}")
            return

        for index, row in df.iterrows():
            ticker = row['代码']
            name = row['名称']
            # 检查股票是否已经存在
            try:
                if self.stock_db.get_stock_by_ticker(ticker) is None:
                    self.stock_db.add_stock(ticker, name, StockType.B_SHARE)
                    logging.info(f"添加股票: {ticker} {name}")
                else:
                    logging.info(f"股票已存在: {ticker} {name}")
            except Exception as e:
                logging.error(f"添加B股股票失败: {e}")
        logging.info("沪深京B股所有股票信息添加完成")

        try:
            df = ak.stock_us_spot_em()
        except Exception as e:
            logging.error(f"获取美股股票数据失败: {e}")
            return
        
        for index, row in df.iterrows():
            ticker = row['代码']
            name = row['名称']
            # 检查股票是否已经存在
            try:
                if self.stock_db.get_stock_by_ticker(ticker) is None:
                    self.stock_db.add_stock(ticker, name, StockType.US_SHARE)
                    logging.info(f"添加股票: {ticker} {name}")
                else:
                    logging.info(f"股票已存在: {ticker} {name}")
            except Exception as e:
                logging.error(f"添加美股股票失败: {e}")
        logging.info("美股所有股票信息添加完成")

        try:
            df = ak.stock_hk_spot_em()
        except Exception as e:
            logging.error(f"获取港股股票数据失败: {e}")
            return
        
        for index, row in df.iterrows():
            ticker = row['代码']
            name = row['名称']
            # 检查股票是否已经存在
            try:
                if self.stock_db.get_stock_by_ticker(ticker) is None:
                    self.stock_db.add_stock(ticker, name, StockType.HK_SHARE)
                    logging.info(f"添加股票: {ticker} {name}")  
                else:
                    logging.info(f"股票已存在: {ticker} {name}")    
            except Exception as e:
                logging.error(f"添加港股股票失败: {e}")
        logging.info("港股所有股票信息添加完成")







