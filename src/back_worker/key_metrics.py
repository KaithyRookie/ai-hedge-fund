
import logging
from src.back_worker_db.key_metrics_db import KeyMetricsDB, KeyMetricsData
import akshare as ak

class KeyMetricsWorker:
    def __init__(self, db:KeyMetricsDB):
        self.db = db
    
    def download_key_metrics(self, ticker:str):
        stock_financial_abstract_df = ak.stock_financial_abstract(symbol=ticker)
        # 获取所有列名
        columns = stock_financial_abstract_df.columns.tolist()

        # dataframe 删除第一列，然后将行列互换
        stock_financial_abstract_df = stock_financial_abstract_df.drop(columns[0], axis=1)
        stock_financial_abstract_df = stock_financial_abstract_df.transpose()
        # 第一行作为列名
        stock_financial_abstract_df.columns = stock_financial_abstract_df.iloc[0]
        stock_financial_abstract_df = stock_financial_abstract_df.drop(stock_financial_abstract_df.index[0])

        # 遍历所有行
        for index, row in stock_financial_abstract_df.iterrows():
            data = KeyMetricsData.model_construct()
            # 判断 归母净利润 是否是 nan，如果不是则赋值
            if not pd.isna(row['归母净利润']):
                data.parent_company_net_profit = row['归母净利润']
            # 判断 营业总收入 是否是 nan，如果不是则赋值
            if not pd.isna(row['营业总收入']):
                data.total_operating_revenue = row['营业总收入']
            # 营业成本
            if not pd.isna(row['营业成本']):
                data.operating_cost = row['营业成本']
            # 净利润
            if not pd.isna(row['净利润']):
                data.net_profit = row['净利润']
            # 判断扣非净利润是否是 nan，如果不是则赋值
            if not pd.isna(row['扣非净利润']):
                data.non_recurring_profit = row['扣非净利润']
            # 判断股东权益合计(净资产)是否是 nan，如果不是则赋值
            if not pd.isna(row['股东权益合计(净资产)']):
                data.total_shareholders_equity = row['股东权益合计(净资产)']
            # 判断商誉是否是 nan，如果不是则赋值
            if not pd.isna(row['商誉']):
                data.goodwill = row['商誉']
            # 判断经营现金流量净额是否是 nan，如果不是则赋值
            if not pd.isna(row['经营现金流量净额']):
                data.net_operating_cash_flow = row['经营现金流量净额']
            # 判断基本每股收益是否是 nan，如果不是则赋值
            if not pd.isna(row['基本每股收益']):
                data.basic_eps = row['基本每股收益']
            # 判断每股净资产是否是 nan，如果不是则赋值
            if not pd.isna(row['每股净资产']):
                data.net_assets_per_share = row['每股净资产']
            # 判断每股现金流是否是 nan，如果不是则赋值
            if not pd.isna(row['每股现金流']):
                data.cash_flow_per_share = row['每股现金流']
            # 判断稀释每股收益是否是 nan，如果不是则赋值
            if not pd.isna(row['稀释每股收益']):
                data.diluted_eps = row['稀释每股收益']
            # 判断摊薄每股净资产_期末股数是否是 nan，如果不是则赋值
            if not pd.isna(row['摊薄每股净资产_期末股数']):
                data.diluted_net_assets_per_share = row['摊薄每股净资产_期末股数']
            # 判断调整每股净资产_期末股数是否是 nan，如果不是则赋值
            if not pd.isna(row['调整每股净资产_期末股数']):
                data.adjusted_net_assets_per_share = row['调整每股净资产_期末股数']
            # 判断每股净资产_最新股数是否是 nan，如果不是则赋值
            if not pd.isna(row['每股净资产_最新股数']):
                data.net_assets_per_share_new = row['每股净资产_最新股数']
            # 判断每股经营现金流是否是 nan，如果不是则赋值
            if not pd.isna(row['每股经营现金流']):
                data.operating_cash_flow_per_share = row['每股经营现金流']
            # 判断每股现金流量净额是否是 nan，如果不是则赋值
            if not pd.isna(row['每股现金流量净额']):
                data.net_cash_flow_per_share = row['每股现金流量净额']
            # 判断每股企业自由现金流量是否是 nan，如果不是则赋值
            if not pd.isna(row['每股企业自由现金流量']):
                data.enterprise_fcf_per_share = row['每股企业自由现金流量']
            # 判断每股股东自由现金流量是否是 nan，如果不是则赋值
            if not pd.isna(row['每股股东自由现金流量']):
                data.shareholder_fcf_per_share = row['每股股东自由现金流量']
            # 判断每股未分配利润是否是 nan，如果不是则赋值
            if not pd.isna(row['每股未分配利润']):
                data.undistributed_profit_per_share = row['每股未分配利润']
            # 判断每股资本公积金是否是 nan，如果不是则赋值
            if not pd.isna(row['每股资本公积金']):
                data.capital_reserve_per_share = row['每股资本公积金']
            # 判断每股盈余公积金是否是 nan，如果不是则赋值
            if not pd.isna(row['每股盈余公积金']):
                data.surplus_reserve_per_share = row['每股盈余公积金']
            # 判断每股留存收益是否是 nan，如果不是则赋值
            if not pd.isna(row['每股留存收益']):
                data.retained_earnings_per_share = row['每股留存收益']
            # 判断每股营业收入是否是 nan，如果不是则赋值
            if not pd.isna(row['每股营业收入']):
                data.operating_revenue_per_share = row['每股营业收入']
            # 判断每股营业总收入是否是 nan，如果不是则赋值
            if not pd.isna(row['每股营业总收入']):
                data.total_operating_revenue_per_share = row['每股营业总收入']
            # 判断每股息税前利润是否是 nan，如果不是则赋值
            if not pd.isna(row['每股息税前利润']):
                data.ebit_per_share = row['每股息税前利润']
            # 定义一个映射字典，将 description 中的描述与 data 的属性名对应起来
            metric_mapping = {
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
            for desc, attr in metric_mapping.items():
                if desc in row and not pd.isna(row[desc]):
                    setattr(data, attr, row[desc])

            try:
                self.db.insert_key_metrics(data)
            except Exception as e:
                logging.error(f"insert key metrics error: {e}")
                return False
        
        return True


