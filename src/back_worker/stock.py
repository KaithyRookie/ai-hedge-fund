from src.back_worker_db.stock_db import StockDB, StockData,StockType
from src.back_worker_db.company_facts_db import CompanyFactDB, CompanyFactData
import akshare as ak
import logging

class StockWorker:
    def __init__(self, stock_db: StockDB, fact_db: CompanyFactDB):
        self.stock_db = stock_db
        self.fact_db = fact_db


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
                if not self.download_company_facts(ticker):
                    logging.error(f"下载公司facts失败: {ticker}")
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
    
    def download_company_facts(self, ticker:str):
        stock_profile_cninfo_df = ak.stock_profile_cninfo(symbol=ticker)
        for index, row in stock_profile_cninfo_df.iterrows():
            company_fact_data = CompanyFactData.model_construct()
            company_fact_data.company_name = row.get("公司名称")
            company_fact_data.company_name_en = row.get("英文名称")
            company_fact_data.former_short_name = row.get("曾用简称")
            company_fact_data.a_share_code = row.get("A股代码")
            company_fact_data.a_share_name = row.get("A股简称")
            company_fact_data.b_share_code = row.get("B股代码")
            company_fact_data.b_share_name = row.get("B股简称")
            company_fact_data.h_share_code = row.get("H股代码")
            company_fact_data.h_share_name = row.get("H股简称")
            company_fact_data.selected_indices = row.get("入选指数")
            company_fact_data.market_category = row.get("所属市场")
            company_fact_data.industry_category = row.get("所属行业")
            company_fact_data.legal_representative = row.get("法人代表")
            company_fact_data.registered_capital = row.get("注册资金")
            company_fact_data.establishment_date = row.get("成立日期")
            company_fact_data.listing_date = row.get("上市日期")
            company_fact_data.official_website = row.get("官方网站")
            company_fact_data.email = row.get("电子邮箱")
            company_fact_data.contact_phone = row.get("联系电话")
            company_fact_data.fax = row.get("传真")
            company_fact_data.registered_address = row.get("注册地址")
            company_fact_data.office_address = row.get("办公地址")
            company_fact_data.postal_code = row.get("邮政编码")
            company_fact_data.main_business = row.get("主营业务")
            company_fact_data.business_scope = row.get("经营范围")
            company_fact_data.company_profile = row.get("机构简介")
            try:
                self.fact_db.create(company_fact_data)
            except Exception as e:
                print(f"Error creating company fact data for ticker {ticker}: {e}")
                return False
        return True