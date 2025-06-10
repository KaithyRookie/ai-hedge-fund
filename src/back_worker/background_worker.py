from src.back_worker.balance import BalanceWorker
from src.back_worker.cash import CashWorker
from src.back_worker.profit import ProfitWorker
from src.back_worker.stock import StockWorker
from src.back_worker_db.balance_db import BalanceDB
from src.back_worker_db.cash_flow_db import CashFlowDB
from src.back_worker_db.profit_db import ProfitDB
from src.back_worker_db.database import get_db_connection
import logging

class BackgroundWorker:
    def __init__(self, balance_worker: BalanceWorker, cash_flow_worker: CashWorker, profit_worker: ProfitWorker, stock_worker: StockWorker):
        self.balance_worker = balance_worker
        self.cash_flow_worker = cash_flow_worker
        self.profit_worker = profit_worker
        self.stock_worker = stock_worker

    def main_process(self):
        self.stock_worker.get_all_a_stocks()
        stock_list = self.stock_worker.get_A_stocks()
        for stock in stock_list:
            ticker = stock.ticker
            success = self.start_task(ticker)
            if not success:
                logging.error(f"任务失败: {ticker}")
                return False
        return True


    def start_task(self, ticker: str):
        # 启动任务
        success = self.balance_worker.download_balance_from_report(ticker)
        if not success:
            return False
        success = self.cash_flow_worker.download_cash_flow(ticker)
        if not success:
            return False
        success = self.profit_worker.download_profit_from_report(ticker)    
        if not success:
            return False
        return True

if __name__ == '__main__':
    # postgresql connection inf
    host="localhost"
    user="ai_hedge_fund"
    password="dnuf_egdeh_ia"
    database="db_ai_hedge_fund"
    conn = get_db_connection(host, user, password, database)
    balance_db = BalanceDB(conn)
    cash_db = CashFlowDB(conn)
    profit_db = ProfitDB(conn)
    balance_worker = BalanceWorker(balance_db)
    cash_worker = CashWorker(cash_db)
    profit_worker = ProfitWorker(profit_db)
    worker = BackgroundWorker(balance_worker, cash_worker, profit_worker)
    worker.start_task('600004')

