from src.back_worker_db.stock_db import StockDB, StockData,StockType
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
            if not self.stock_db.check_stock_exists(ticker, StockType.A_SHARE):
                stock_data = self.generate_stock_data(row, StockType.A_SHARE)
                try:
                    self.stock_db.add_stock(stock_data)
                    logging.info(f"添加股票: {ticker} {name}")
                except Exception as e:
                    logging.error(f"添加A股股票失败: {e}")
                    continue
            else:
                logging.info(f"股票已存在: {ticker} {name}")
            
        logging.info("沪深京A股所有股票信息添加完成")

        try:
            df= ak.stock_zh_b_spot_em()
        except Exception as e:
            logging.error(f"获取股票数据失败: {e}")
            return

        for index, row in df.iterrows():
            ticker = row['代码']
            # 检查股票是否已经存在
            if self.stock_db.check_stock_exists(ticker, StockType.B_SHARE) is None:
                stock_data = self.generate_stock_data(row, StockType.B_SHARE)
                try:
                    self.stock_db.add_stock(stock_data)
                    logging.info(f"添加股票: {ticker} ")
                except Exception as e:
                    logging.error(f"添加A股股票失败: {e}")
                    continue
            else:
                logging.info(f"股票已存在: {ticker} ")
        logging.info("沪深京B股所有股票信息添加完成")

        try:
            df = ak.stock_us_spot_em()
        except Exception as e:
            logging.error(f"获取美股股票数据失败: {e}")
            return
        
        for index, row in df.iterrows():
            ticker = row['代码']
            # 检查股票是否已经存在
            if self.stock_db.check_stock_exists(ticker, StockType.US_STOCK) is None:
                stock_data = self.generate_stock_data(row, StockType.US_STOCK)
                try:
                    self.stock_db.add_stock(stock_data)
                    logging.info(f"添加股票: {ticker} {name}")
                except Exception as e:
                    logging.error(f"添加美股股票失败: {e}")
                    continue
            else:
                logging.info(f"股票已存在: {ticker} {name}")
        logging.info("美股所有股票信息添加完成")

        try:
            df = ak.stock_hk_spot_em()
        except Exception as e:
            logging.error(f"获取港股股票数据失败: {e}")
            return
        for index, row in df.iterrows():
            ticker = row['代码']
            # 检查股票是否已经存在
            if self.stock_db.check_stock_exists(ticker, StockType.HK_STOCK) is None:
                stock_data = self.generate_stock_data(row, StockType.HK_STOCK)
                try:
                    self.stock_db.add_stock(stock_data)
                    logging.info(f"添加股票: {ticker} {name}")
                except Exception as e:
                    logging.error(f"添加港股股票失败: {e}")
                    continue
            else:
                logging.info(f"股票已存在: {ticker} {name}")

        logging.info("港股所有股票信息添加完成")

    def get_A_stocks(self):
        stock_list = self.stock_db.get_all_stocks(StockType.A_SHARE)
        return stock_list
    
    def get_B_stocks(self):
        stock_list = self.stock_db.get_all_stocks(StockType.B_SHARE)
        return stock_list

    def get_US_stocks(self):
        stock_list = self.stock_db.get_all_stocks(StockType.US_STOCK)
        return stock_list

    def get_HK_stocks(self):
        stock_list = self.stock_db.get_all_stocks(StockType.HK_STOCK)
        return stock_list


    def generate_stock_data(self, row, stock_type) -> StockData:
        ticker = row['代码']
        name = row['名称']
        stock_data = StockData.model_construct()
        stock_data.ticker = ticker
        stock_data.ticker_name = name
        stock_data.stock_type = stock_type
        stock_data.serial_number = row['序号']
        return stock_data

