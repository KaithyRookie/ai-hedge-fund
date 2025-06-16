import logging
from src.back_worker_db.balance_db import BalanceDB
from src.back_worker_db.cash_flow_db import CashFlowDB
from src.back_worker_db.financial_indicators_db import FinancialIndicatorsDB
from src.back_worker_db.key_metrics_db import KeyMetricsDB
from src.back_worker_db.profit_db import ProfitDB
from src.back_worker_db.stock_db import StockType
from src.back_worker_db.financial_metrics_db import FinancialMetricsDB
import akshare as ak
from datetime import datetime, timedelta
from src.back_worker_db.stock_valuation_db import StockValuationDB
from src.data.models import FinancialMetrics

class FinancialMetricsManager:
    def __init__(self, financial_metrics_db: FinancialMetricsDB, balance_db: BalanceDB, cash_db: CashFlowDB, profit_db: ProfitDB, key_metrics_db: KeyMetricsDB, financial_indicators_db: FinancialIndicatorsDB, stock_value_db: StockValuationDB):
        self.financial_metrics_db = financial_metrics_db
        self.balance_db = balance_db
        self.cash_db = cash_db
        self.profit_db = profit_db
        self.key_metrics_db = key_metrics_db
        self.financial_indicators_db = financial_indicators_db
        self.stock_value_db = stock_value_db

    def get_financial_metrics(self, ticker: str, stock_type: StockType):
        if stock_type == StockType.HK:
            # stock_financial_metric_dict, financial_report_date_list = self.get_stock_hk_financial_metrics(ticker)
            pass
        elif stock_type == StockType.A:
            return self.generate_A_stock_financial_metrics(ticker=ticker)
    
    def generate_A_stock_financial_metrics(self, ticker: str, end_date: str=None):
        report_date_list = []
        balance_dict = {}
        balance_list = self.balance_db.get_balance_sheet(ticker=ticker, end_date=end_date)
        for balance_item in balance_list:
            balance_dict[balance_item.report_date] = balance_item
            # 字符串转时间
            report_date_list.append(datetime.strptime(balance_item.report_date, '%Y-%m-%d')) # 时间戳用于后续按时间排序
        
        # 按时间升序排序
        report_date_list.sort()
        profit_list = self.profit_db.get_profit(ticker=ticker, end_date=end_date)
        profit_dict = {}
        for profit_data in profit_list:
            profit_dict[profit_data.report_date] = profit_data
        cash_list = self.cash_db.get_cash_flow(ticker=ticker, end_date=end_date)
        cash_dict = {}
        for cash_data in cash_list:
            cash_dict[cash_data.report_date] = cash_data
        key_metric_list = self.key_metrics_db.query_key_metrics(ticker=ticker, end_date=end_date)
        key_metric_dict = {}
        for key_metric_data in key_metric_list:
            key_metric_dict[key_metric_data.report_date] = key_metric_data
        financial_indicator_list = self.financial_indicators_db.get_by_date_range(ticker=ticker, end_date=end_date)
        financial_indicator_dict = {}
        for item in financial_indicator_list:
            financial_indicator_dict[item.report_date] = item
        
        stock_value_list = self.stock_value_db.query_stock_valuation(ticker=ticker, end_date=end_date)

        for item in stock_value_list:
            # 遍历找到最近的报告时间
            item_date = datetime.strptime(item.data_date, '%Y-%m-%d')
            report_date = ''
            last_year_report_date = ''
            for date in report_date_list:
                if date <= item_date:
                    year = date.year - 1
                    month = date.month
                    day = date.day
                    last_year_report_date = f"{year}-{month:02d}-{day:02d}"
                    # 时间转字符串
                    report_date = date.strftime('%Y-%m-%d')
                    break

            metric_item = FinancialMetrics.model_construct()
            metric_item.ticker = ticker
            metric_item.period = report_date
            metric_item.roe = item.roe
            metric_item.roa = item.roa

            stock_balance = balance_dict.get(report_date, None)
            if stock_balance:
                total_assets = stock_balance.total_assets
                inventory = stock_balance.inventories
                current_liabilities = stock_balance.total_current_liabilities
                accounts_receivable_and_notes_receivable = stock_balance.notes_accounts_receivable
                # 总债务
                total_debt = stock_balance.short_term_borrowings + stock_balance.non_current_liabilities_due_within_one_year + stock_balance.long_term_borrowings + stock_balance.bonds_payable + stock_balance.lease_liabilities
                # 现金及现金等价物
                cash_and_cash_equivalents = stock_balance.monetary_funds + stock_balance.trading_financial_assets
                # 速动资产
                quick_assets = stock_balance.total_current_assets - stock_balance.inventories - stock_balance.prepayments
                # 投资资本
                investment_capital = stock_balance.total_owners_equity + stock_balance.short_term_borrowings + stock_balance.non_current_liabilities_due_within_one_year + stock_balance.long_term_borrowings + stock_balance.bonds_payable
                # 营运资金
                working_capital = stock_balance.total_current_assets - stock_balance.total_current_liabilities
                # 流动比率
                current_ratio = stock_balance.total_current_assets / stock_balance.total_current_liabilities if stock_balance.total_current_liabilities != 0 else None
                if current_ratio:
                    metric_item.current_ratio = current_ratio
                # 速动比率
                quick_ratio = quick_assets / stock_balance.total_current_liabilities if stock_balance.total_current_liabilities != 0 else None
                if quick_ratio:
                    metric_item.quick_ratio = quick_ratio
                # 现金比率
                cash_ratio = cash_and_cash_equivalents / stock_balance.total_current_liabilities if stock_balance.total_current_liabilities != 0 else None
                if cash_ratio:
                    metric_item.cash_ratio = cash_ratio
                # 债务权益比
                debt_to_equity_ratio = total_debt / stock_balance.total_liabilities_and_owners_equity if stock_balance.total_liabilities_and_owners_equity != 0 else None
                if debt_to_equity_ratio:
                    metric_item.debt_to_equity = debt_to_equity_ratio
                # 总债务除以总资产
                debt_to_total_assets_ratio = total_debt / stock_balance.total_assets if stock_balance.total_assets != 0 else None
                if debt_to_total_assets_ratio:
                    metric_item.debt_to_assets = debt_to_total_assets_ratio
                
                enterprise_value = item.market_cap + stock_balance.total_liabilities

                last_year_stock_balance = balance_dict.get(last_year_report_date, None)
                if last_year_stock_balance:
                    # 账面价值同比增长
                    last_year_total_owners_equity = last_year_stock_balance.total_owners_equity
                    if last_year_total_owners_equity:
                        metric_item.book_value_growth = (stock_balance.total_owners_equity - last_year_total_owners_equity) / last_year_total_owners_equity

            stock_profit = profit_dict.get(report_date, None)    
            if stock_profit:
                revenue = stock_profit.total_operating_revenue
                if enterprise_value and revenue:
                    # 企业价值收入比
                    metric_item.enterprise_value_to_revenue_ratio = enterprise_value / revenue
                operating_income = stock_profit.operating_revenue
                interest_expense = stock_profit.interest_expenditure
                if operating_income:
                    if total_assets:
                        # 总资产周转率
                        metric_item.total_assets_turnover = operating_income / total_assets
                    if accounts_receivable_and_notes_receivable:
                        # 应收账款周转率
                        metric_item.accounts_receivable_turnover = operating_income / accounts_receivable_and_notes_receivable
                        metric_item.days_sales_outstanding = accounts_receivable_and_notes_receivable / operating_income
                    if working_capital:
                        metric_item.working_capital_turnover = operating_income / working_capital
                    if interest_expense:
                        # 利息保障倍数
                        metric_item.interest_coverage = operating_income / interest_expense
                operating_revenue = stock_profit.operating_profit
                net_profit = stock_profit.net_profit
                cost_of_goods_sold = stock_profit.operating_cost
                if inventory:
                    metric_item.inventory_turnover = cost_of_goods_sold / inventory

                if metric_item.inventory_turnover and metric_item.accounts_receivable_turnover:
                    metric_item.operating_cycle = metric_item.inventory_turnover + metric_item.accounts_receivable_turnover
                # 实际税率(未参考财报附注调整)
                actual_tax_rate = stock_profit.income_tax_expense / stock_profit.total_profit
                # 毛利
                gross_profit = stock_profit.total_operating_revenue - stock_profit.operating_cost
                # 毛利率
                gross_profit_margin = gross_profit / stock_profit.total_operating_revenue
                if gross_profit_margin:
                    metric_item.gross_margin = gross_profit_margin
                operating_margin = stock_profit.operating_revenue / stock_profit.total_operating_revenue
                if operating_margin:
                    metric_item.operating_margin = operating_margin
                # 净利率
                net_profit_margin = stock_profit.net_profit / stock_profit.total_operating_revenue
                if net_profit_margin:
                    metric_item.net_profit_margin = net_profit_margin
                # NOPAT
                nopat = operating_profit / (1 - actual_tax_rate)
                if nopat and investment_capital:
                    metric_item.roic = nopat / investment_capital
                
                last_year_stock_profit = profit_dict.get(last_year_report_date, None) 
                if last_year_stock_profit:
                    # 收入同比增长
                    last_year_revenue = last_year_stock_profit.total_operating_revenue
                    if last_year_revenue:
                        metric_item.revenue_growth = (revenue - last_year_revenue) / last_year_revenue
                    # 收益同比增长
                    last_year_operating_income = last_year_stock_profit.operating_revenue
                    if last_year_operating_income:
                        metric_item.operating_income_growth = (operating_income - last_year_operating_income) / last_year_operating_income

                    last_year_net_profit = last_year_stock_profit.net_profit
                    if last_year_net_profit:
                        metric_item.earnings_growth = (net_profit - last_year_net_profit) / last_year_net_profit
                    
                    last_year_operating_revenue = last_year_stock_profit.operating_profit
                    if last_year_operating_revenue:
                        metric_item.operating_profit_growth = (operating_revenue - last_year_operating_revenue) / last_year_operating_revenue

                    
            stock_cash = cash_dict.get(report_date, None)
            if stock_cash:
                operating_cash_flow = stock_cash.net_operating_cash_flow
                if current_liabilities:
                    metric_item.operating_cash_flow_ratio = operating_cash_flow / current_liabilities
                cash_and_cash_equivalents_end = stock_cash.ending_total_cash_balance
                # fcf
                fcf = stock_cash.net_operating_cash_flow - stock_cash.cash_paid_for_assets
                if enterprise_value :
                    if cash_and_cash_equivalents_end:
                        metric_item.enterprise_value = enterprise_value - cash_and_cash_equivalents_end
                    if fcf:
                        metric_item.fcf_yield = fcf / enterprise_value
                
                last_year_stock_cash = cash_dict.get(last_year_report_date, None)
                if last_year_stock_cash:
                    last_year_fcf = last_year_stock_cash.net_operating_cash_flow - last_year_stock_cash.cash_paid_for_assets
                    # 自由现金流同比增长
                    if last_year_fcf:
                        metric_item.free_cash_flow_growth = (fcf - last_year_fcf) / last_year_fcf


            stock_key_metric = key_metric_dict.get(report_date, None)
            if stock_key_metric:
                book_value = stock_key_metric.net_assets_per_share
                metric_item.free_cash_flow_per_share = stock_key_metric.enterprise_fcf_per_share
                metric_item.fcfe_per_share = stock_key_metric.shareholder_fcf_per_share
                metric_item.earnings_per_share = stock_key_metric.basic_eps
                metric_item.book_value_per_share = stock_key_metric.net_assets_per_share
                if stock_key_metric.ebitda and enterprise_value:
                    # 企业价值与 EBITDA 比率
                    metric_item.enterprise_value_to_ebitda_ratio = enterprise_value / stock_key_metric.ebitda
                last_year_stock_key_metric = key_metric_dict.get(last_year_report_date, None)
                if last_year_stock_key_metric:
                    # 在此期间每股收益增长
                    last_year_basic_eps = last_year_stock_key_metric.basic_eps
                    if last_year_basic_eps:
                        metric_item.earnings_per_share_growth = (basic_eps - last_year_basic_eps) / last_year_basic_eps
                    # EBITDA 增长
                    last_year_ebitda = last_year_stock_key_metric.ebitda
                    if last_year_ebitda:
                        metric_item.ebitda_growth = (ebitda - last_year_ebitda) / last_year_ebitda
            stock_financial_indicator = financial_indicator_dict.get(report_date, None)
            if stock_financial_indicator:
               metric_item.payout_ratio = stock_financial_indicator.dividend_payout_ratio
            
            try:
                self.financial_metrics_db.insert_financial_metrics(metric_item)
            except Exception as e:
                logging.error(f"Error insert financial metrics: {e}")
                return False
        return True