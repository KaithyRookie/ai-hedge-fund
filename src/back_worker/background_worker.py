import time

from src.back_worker.balance import BalanceWorker
from src.back_worker.cash import CashWorker
from src.back_worker.company_news_worker import CompanyNewsWorker
from src.back_worker.financial_indicators import FinancialIndicatorsWorker
from src.back_worker.financial_metrics import FinancialMetricsManager
from src.back_worker.inside_trade import InsideTradeWorker
from src.back_worker.key_metrics import KeyMetricsWorker
from src.back_worker.profit import ProfitWorker
from src.back_worker.stock import StockWorker
from src.back_worker.stock_valuation import StockValuationWorker
from src.back_worker_db import stock_db
from src.back_worker_db.balance_db import BalanceDB
from src.back_worker_db.cash_flow_db import CashFlowDB
from src.back_worker_db.company_facts_db import CompanyFactDB
from src.back_worker_db.company_news_db import CompanyNewsDB
from src.back_worker_db.financial_indicators_db import FinancialIndicatorsDB
from src.back_worker_db.financial_metrics_db import FinancialMetricsDB
from src.back_worker_db.inside_trade_db import InsideTradeDB
from src.back_worker_db.key_metrics_db import KeyMetricsDB
from src.back_worker_db.profit_db import ProfitDB
from src.back_worker_db.database import get_db_connection
import logging



from src.back_worker_db.stock_db import StockDB, StockType
from src.back_worker_db.stock_valuation_db import StockValuationDB



class BackgroundWorker:
    def __init__(self, balance_worker: BalanceWorker, cash_flow_worker: CashWorker, profit_worker: ProfitWorker, stock_worker: StockWorker,
                 company_news_worker: CompanyNewsWorker, financial_indicators_worker: FinancialIndicatorsWorker, financial_metric_manager: FinancialMetricsManager,
                 inside_trade_worker: InsideTradeWorker, key_metric_worker: KeyMetricsWorker, stock_valuation_worker: StockValuationWorker,):
        self.balance_worker = balance_worker
        self.cash_flow_worker = cash_flow_worker
        self.profit_worker = profit_worker
        self.stock_worker = stock_worker
        self.company_news_worker = company_news_worker
        self.financial_indicators_worker = financial_indicators_worker
        self.financial_metric_manager = financial_metric_manager
        self.inside_trade_worker = inside_trade_worker
        self.key_metric_worker = key_metric_worker
        self.stock_valuation_worker = stock_valuation_worker

    def main_process(self):
        self.stock_worker.get_all_a_stocks()
        success = self.inside_trade_worker.download_inside_trade()
        if not success:
            logging.error("")
        stock_list = self.stock_worker.get_A_stocks()
        for stock in stock_list:
            ticker = stock.ticker
            ticker_name = stock.ticker_name
            success = self.start_task(ticker)
            if not success:
                logging.error(f"任务失败: {ticker}")
                return False

            success = self.financial_metric_manager.generate_A_stock_financial_metrics(ticker)
            if not success:
                logging.error(f"财务指标生成失败: {ticker}, {ticker_name}")
                return False
            time.sleep(5)
            success = self.company_news_worker.download_company_news(ticker, ticker_name)
            if not success:
                logging.error(f"公司新闻下载失败: {ticker}, {ticker_name}")
                return False

        return True


    def start_task(self, ticker: str, stock_type: str = 'A'):
        # 启动任务
        logging.info(f"start download stock balance sheet: {ticker}")
        success = self.balance_worker.download_balance_from_report(ticker)
        if not success:
            return False
        time.sleep(5)
        logging.info(f"start download stock cash flow sheet: {ticker}")
        success = self.cash_flow_worker.download_cash_flow(ticker)
        if not success:
            return False
        time.sleep(5)
        logging.info(f"start download stock profit sheet: {ticker}")
        success = self.profit_worker.download_profit_from_report(ticker)    
        if not success:
            return False
        time.sleep(5)
        logging.info(f"start download stock financial indicators: {ticker}")
        success = self.financial_indicators_worker.download_financial_indicators_from_report(ticker, stock_type)
        if not success:
            return False
        time.sleep(5)
        logging.info(f"start download stock metrics: {ticker}")
        success = self.key_metric_worker.download_key_metrics(ticker)
        if not success:
            return False
        time.sleep(5)
        logging.info(f"start download stock stock valuation: {ticker}")
        success = self.stock_valuation_worker.download_stock_valuation(ticker)
        return success

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    # 配置输出控制台
    # console_handler = logging.StreamHandler()
    # console_handler.setLevel(logging.INFO)
    # console_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    # console_handler.setFormatter(console_formatter)
    # logging.getLogger().addHandler(console_handler)
    logging.info("开始执行任务...")
    # postgresql connection inf
    host="localhost"
    user="ai_hedge_fund"
    password="dnuf_egdeh_ia"
    database="db_ai_hedge_fund"
    conn = get_db_connection(host, user, password, database)
    balance_db = BalanceDB(conn)
    cash_db = CashFlowDB(conn)
    profit_db = ProfitDB(conn)
    stock_db = StockDB(conn)
    company_fact_db = CompanyFactDB(conn)
    company_news_db = CompanyNewsDB(conn)

    balance_worker = BalanceWorker(balance_db)
    cash_worker = CashWorker(cash_db)
    profit_worker = ProfitWorker(profit_db)

    financial_indicators_db = FinancialIndicatorsDB(conn)
    inside_trade_db = InsideTradeDB(conn)

    stock_worker = StockWorker(stock_db, company_fact_db)
    company_news_worker = CompanyNewsWorker(company_news_db)
    financial_indicators_worker = FinancialIndicatorsWorker(financial_indicators_db)

    inside_trade_worker = InsideTradeWorker(inside_trade_db, stock_db)

    key_metric_db = KeyMetricsDB(conn)
    key_metric_worker = KeyMetricsWorker(key_metric_db)

    stock_valuation_db = StockValuationDB(conn)
    stock_valuation_worker = StockValuationWorker(stock_valuation_db)

    financial_metric_db = FinancialMetricsDB(conn)
    financial_metric_manager = FinancialMetricsManager(financial_metric_db, balance_db, cash_db, profit_db, key_metric_db, financial_indicators_db, stock_valuation_db)

    worker = BackgroundWorker(balance_worker, cash_worker, profit_worker, stock_worker, company_news_worker,financial_indicators_worker, financial_metric_manager, inside_trade_worker, key_metric_worker, stock_valuation_worker)
    try:
        # worker.main_process()
        # financial_indicators_worker.download_financial_indicators_from_report('838227')
        # success = key_metric_worker.download_key_metrics('838227')

        stock_valuation_worker.download_stock_valuation('838227')
    except Exception as e:
        logging.error(f"任务执行出错: {e}")
    finally:
        conn.close()

