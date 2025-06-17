
import logging
from datetime import datetime

from src.back_worker_db.key_metrics_db import KeyMetricsDB, KeyMetricsData
import akshare as ak
import pandas as pd

class KeyMetricsWorker:
    def __init__(self, db:KeyMetricsDB):
        self.db = db
    
    def download_key_metrics(self, ticker:str):
        stock_financial_abstract_df = ak.stock_financial_abstract(symbol=ticker)
        # 获取所有列名
        columns = stock_financial_abstract_df.columns.tolist()

        # dataframe 删除第一列，然后将行列互换
        adjusted_df = stock_financial_abstract_df.drop(columns[0], axis=1)
        adjusted_df = adjusted_df.transpose()
        # 第一行作为列名
        adjusted_df.columns = adjusted_df.iloc[0]
        adjusted_df = adjusted_df.drop(adjusted_df.index[0])

        latest_report_date = self.db.get_latest_report_date(ticker)
        # 转换为 datetime 对象
        latest_report_date = datetime(latest_report_date.year, latest_report_date.month, latest_report_date.day) if latest_report_date else datetime(1900, 1, 1)

        # 定义一个映射字典，将 description 中的描述与 data 的属性名对应起来
        metric_mapping = {
            '归母净利润': 'parent_company_net_profit',
            '营业总收入': 'total_operating_revenue',
            '营业成本': 'operating_cost',
            '净利润': 'net_profit',
            '扣非净利润': 'non_recurring_profit',
            '股东权益合计(净资产)': 'total_shareholders_equity',
            '商誉': 'goodwill',
            '经营现金流量净额': 'net_operating_cash_flow',
            '基本每股收益': 'basic_eps',
            '每股净资产': 'net_assets_per_share',
            '每股现金流': 'cash_flow_per_share',
            '稀释每股收益': 'diluted_eps',
            '摊薄每股净资产_期末股数': 'diluted_net_assets_per_share',
            '调整每股净资产_期末股数': 'adjusted_net_assets_per_share',
            '每股净资产_最新股数': 'net_assets_per_share_new',
            '每股经营现金流': 'operating_cash_flow_per_share',
            '每股现金流量净额': 'net_cash_flow_per_share',
            '每股企业自由现金流量': 'enterprise_fcf_per_share',
            '每股股东自由现金流量': 'shareholder_fcf_per_share',
            '每股未分配利润': 'undistributed_profit_per_share',
            '每股资本公积金': 'capital_reserve_per_share',
            '每股盈余公积金': 'surplus_reserve_per_share',
            '每股留存收益': 'retained_earnings_per_share',
            '每股营业收入': 'operating_revenue_per_share',
            '每股营业总收入': 'total_operating_revenue_per_share',
            '每股息税前利润': 'ebit_per_share',
            "净资产收益率(ROE)": "roe",
            "总资产报酬率(ROA)": "roa",
            "毛利率": "gross_margin",
            "销售净利率": "net_profit_margin",
            "期间费用率": "period_expense_ratio",
            "摊薄净资产收益率": "diluted_roe",
            "净资产收益率_平均": "average_roe",
            "净资产收益率_平均_扣除非经常损益": "average_roe_non_recurring",
            "摊薄净资产收益率_扣除非经常损益": "diluted_roe_non_recurring",
            "息税前利润率": "ebit_margin",
            "总资本回报率": "total_capital_return",
            "投入资本回报率": "invested_capital_return",
            "息前税后总资产报酬率_平均": "after_tax_roa",
            "成本费用利润率": "cost_profit_ratio",
            "营业利润率": "operating_profit_margin",
            "总资产净利率_平均": "average_asset_net_profit_rate",
            "总资产净利率_平均(含少数股东损益)": "average_asset_net_profit_rate_minority",
            "营业总收入增长率": "operating_revenue_growth_rate",
            "归属母公司净利润增长率": "parent_company_net_profit_growth_rate",
            "经营活动净现金/销售收入": "operating_cash_sales_ratio",
            "经营性现金净流量/营业总收入": "operating_cash_total_revenue_ratio",
            "成本费用率": "cost_expense_ratio",
            "销售成本率": "sales_cost_ratio",
            "经营活动净现金/归属母公司的净利润": "operating_cash_parent_profit_ratio",
            "所得税/利润总额": "income_tax_profit_ratio",
            "资产负债率": "asset_liability_ratio",
            "流动比率": "current_ratio",
            "速动比率": "quick_ratio",
            "保守速动比率": "conservative_quick_ratio",
            "权益乘数": "equity_multiplier",
            "权益乘数(含少数股权的净资产)": "equity_multiplier_minority",
            "产权比率": "equity_debt_ratio",
            "现金比率": "cash_ratio",
            "应收账款周转率": "accounts_receivable_turnover",
            "应收账款周转天数": "accounts_receivable_days",
            "存货周转率": "inventory_turnover",
            "存货周转天数": "inventory_days",
            "总资产周转率": "total_asset_turnover",
            "总资产周转天数": "total_asset_days",
            "流动资产周转率": "current_asset_turnover",
            "流动资产周转天数": "current_asset_days",
            "应付账款周转率": "accounts_payable_turnover",
            "应付账款周转天数": "accounts_payable_days"
        }
        # 遍历所有行
        for index, row in adjusted_df.iterrows():
            data = KeyMetricsData.model_construct()
            data.ticker = ticker
            current_report_date = datetime.strptime(str(index), '%Y%m%d')
            current_report_date_str = current_report_date.strftime('%Y-%m-%d')
            data.report_date = datetime.strptime(current_report_date_str, '%Y-%m-%d')

            # 判断 report_date 是否大于 latest_report_date，如果小于等于则跳过
            if  data.report_date <= latest_report_date:
                continue
            for desc, attr in metric_mapping.items():
                if desc in row:
                    value = row[desc]
                    if isinstance(value, pd.Series):
                        value = value.iloc[0]
                    if not pd.isna(value):
                        setattr(data, attr, value)
            try:
                self.db.insert_key_metrics(data)
            except Exception as e:
                logging.error(f"insert key metrics error: {e}")
                return False
        
        return self.calculate_ticker_ebitbd(ticker)

    def calculate_ticker_ebitbd(self, ticker:str):
        """
        计算 ticker 的 ebitda 指标
        """
        ebitda_dict = {}
        stock_profit_sheet_by_report_em_df = ak.stock_profit_sheet_by_report_em(symbol=ticker)
        for index, row in stock_profit_sheet_by_report_em_df.iterrows():
            data_date = row['REPORT_DATE']
            # 利息费用
            interest_expense = row['FE_INTEREST_EXPENSE']
            # 利润总额
            profit_total = row['TOTAL_PROFIT']
            ebitda = profit_total + interest_expense
            ebitda_dict[data_date] = ebitda
        stock_cash_flow_sheet_by_report_em_df = ak.stock_cash_flow_sheet_by_report_em(symbol=ticker)
        for index, row in stock_cash_flow_sheet_by_report_em_df.iterrows():
            data_date = row['REPORT_DATE']
            # 固定资产和投资性房地产折旧
            depreciation_and_amortization = row['FA_IR_DEPR']
            # 无形资产摊销
            amortization = row['IA_AMORTIZE']
            # 长期待摊费用摊销
            long_term_prepaid_expenses = row['LPE_AMORTIZE']

            # EBITBD
            ebitda = ebitda_dict[data_date]
            ebitda_dict[data_date] = ebitda + depreciation_and_amortization + amortization + long_term_prepaid_expenses
        
        for report_date, ebitbd in ebitda_dict.items():
            update_dict = {
                'ebitbd': ebitbd
            }
            # 将 report_date 格式化为yyyy-mm-dd
            try:
                self.db.update_key_metrics(ticker, report_date, update_dict)
            except Exception as e:
                logging.error(f"update key metrics error: {e}")
                return False
        return True
