from src.back_worker_db.profit_db import ProfitDB, ProfitData
import akshare as ak
import logging
import pandas as pd
from datetime import datetime, timedelta
import time

class ProfitWorker:
    def __init__(self, profit_db: ProfitDB):
        self.profit_db = profit_db
    
    def download_profit_from_report(self, ticker:str)->bool:
        """
        从报告中下载利润数据
        :param ticker: 股票代码
        :return: 是否成功
        """
        try:
            stock_financial_report_sina_df = ak.stock_financial_report_sina(stock=ticker, symbol="利润表")
        except Exception as e:
            logging.error(f"Failed to get {ticker} profit from report: {e}")
            return False
        latest_report_date_str = self.profit_db.get_latest_profit_report_date(ticker)
        latest_report_date = datetime.strptime(latest_report_date_str, '%Y%m%d') if latest_report_date_str else datetime(1900, 1, 1)
        
        for index, row in stock_financial_report_sina_df.iterrows():
            report_date_str = row['报告日']
            report_date = datetime.strptime(report_date_str, '%Y%m%d')
            if report_date <= latest_report_date:
                continue
            logging.info(f"Downloading {ticker} profit from report: {report_date_str}")
            profit_data = ProfitData.model_construct()
            profit_data.ticker = ticker
            profit_data.report_date = report_date_str
            profit_data.data_source = row['数据源']
            profit_data.is_audited = row['是否审计']
            profit_data.announcement_date = row['公告日期']
            profit_data.currency = row['币种']
            profit_data.report_type = row['类型']
            profit_data.update_date = row['更新日期']
            if not pd.isna(row['营业总收入']):
                profit_data.total_operating_revenue = row['营业总收入']
            if not pd.isna(row['营业收入']):
                profit_data.operating_revenue = row['营业收入']
            if not pd.isna(row['利息收入']):
                profit_data.interest_income = row['利息收入']
            if not pd.isna(row['已赚保费']):
                profit_data.earned_premium = row['已赚保费']
            if not pd.isna(row['手续费及佣金收入']):
                profit_data.commission_income = row['手续费及佣金收入']
            if not pd.isna(row['房地产销售收入']):
                profit_data.real_estate_sales_revenue = row['房地产销售收入']
            if not pd.isna(row['其他业务收入']):
                profit_data.other_business_revenue = row['其他业务收入']
            if not pd.isna(row['营业总成本']):
                profit_data.total_operating_cost = row['营业总成本']
            if not pd.isna(row['营业成本']):
                profit_data.operating_cost = row['营业成本']
            if not pd.isna(row['手续费及佣金支出']):
                profit_data.commission_expense = row['手续费及佣金支出']
            if not pd.isna(row['房地产销售成本']):
                profit_data.real_estate_sales_cost = row['房地产销售成本']
            if not pd.isna(row['退保金']):
                profit_data.surrender_value = row['退保金']
            if not pd.isna(row['赔付支出净额']):
                profit_data.net_compensation_expense = row['赔付支出净额']
            if not pd.isna(row['提取保险合同准备金净额']):
                profit_data.net_insurance_contract_reserves = row['提取保险合同准备金净额']
            if not pd.isna(row['保单红利支出']):
                profit_data.policy_dividend_expense = row['保单红利支出']
            if not pd.isna(row['分保费用']):
                profit_data.reinsurance_expense = row['分保费用']
            if not pd.isna(row['其他业务成本']):
                profit_data.other_business_cost = row['其他业务成本']
            if not pd.isna(row['营业税金及附加']):
                profit_data.business_tax_and_surcharge = row['营业税金及附加']
            if not pd.isna(row['研发费用']):
                profit_data.rd_expense = row['研发费用']
            if not pd.isna(row['销售费用']):
                profit_data.sales_expense = row['销售费用']
            if not pd.isna(row['管理费用']):
                profit_data.management_expense = row['管理费用']
            if not pd.isna(row['财务费用']):
                profit_data.financial_expense = row['财务费用']
            if not pd.isna(row['利息费用']):
                profit_data.interest_expense = row['利息费用']
            if not pd.isna(row['利息支出']):
                profit_data.interest_expenditure = row['利息支出']
            if not pd.isna(row['投资收益']):
                profit_data.investment_income = row['投资收益']
            if not pd.isna(row['对联营企业和合营企业的投资收益']):
                profit_data.investment_income_associates = row['对联营企业和合营企业的投资收益']
            if not pd.isna(row['以摊余成本计量的金融资产终止确认产生的收益']):
                profit_data.financial_asset_termination_income = row['以摊余成本计量的金融资产终止确认产生的收益']
            if not pd.isna(row['汇兑收益']):
                profit_data.exchange_gain = row['汇兑收益']
            if not pd.isna(row['净敞口套期收益']):
                profit_data.net_exposure_hedge_income = row['净敞口套期收益']
            if not pd.isna(row['公允价值变动收益']):
                profit_data.fair_value_change_income = row['公允价值变动收益']
            if not pd.isna(row['期货损益']):
                profit_data.futures_profit_loss = row['期货损益']
            if not pd.isna(row['托管收益']):
                profit_data.custody_income = row['托管收益']
            if not pd.isna(row['补贴收入']):
                profit_data.subsidy_income = row['补贴收入']
            if not pd.isna(row['其他收益']):
                profit_data.other_income = row['其他收益']
            if not pd.isna(row['资产减值损失']):
                profit_data.asset_impairment_loss = row['资产减值损失']
            if not pd.isna(row['信用减值损失']):
                profit_data.credit_impairment_loss = row['信用减值损失']
            if not pd.isna(row['其他业务利润']):
                profit_data.other_business_profit = row['其他业务利润']
            if not pd.isna(row['资产处置收益']):
                profit_data.asset_disposal_income = row['资产处置收益']
            if not pd.isna(row['营业利润']):
                profit_data.operating_profit = row['营业利润']
            if not pd.isna(row['营业外收入']):
                profit_data.non_operating_income = row['营业外收入']
            if not pd.isna(row['非流动资产处置利得']):
                profit_data.non_current_asset_disposal_gain = row['非流动资产处置利得']
            if not pd.isna(row['营业外支出']):
                profit_data.non_operating_expense = row['营业外支出']
            if not pd.isna(row['非流动资产处置损失']):
                profit_data.non_current_asset_disposal_loss = row['非流动资产处置损失']
            if not pd.isna(row['利润总额']):
                profit_data.total_profit = row['利润总额']
            if not pd.isna(row['所得税费用']):
                profit_data.income_tax_expense = row['所得税费用']
            if not pd.isna(row['未确认投资损失']):
                profit_data.unrecognized_investment_loss = row['未确认投资损失']
            if not pd.isna(row['净利润']):
                profit_data.net_profit = row['净利润']
            if not pd.isna(row['持续经营净利润']):
                profit_data.continuing_operation_net_profit = row['持续经营净利润']
            if not pd.isna(row['终止经营净利润']):
                profit_data.discontinued_operation_net_profit = row['终止经营净利润']
            if not pd.isna(row['归属于母公司所有者的净利润']):
                profit_data.net_profit_parent_company = row['归属于母公司所有者的净利润']
            if not pd.isna(row['被合并方在合并前实现净利润']):
                profit_data.merged_party_net_profit = row['被合并方在合并前实现净利润']
            if not pd.isna(row['少数股东损益']):
                profit_data.minority_profit_loss = row['少数股东损益']
            if not pd.isna(row['其他综合收益']):
                profit_data.other_comprehensive_income = row['其他综合收益']
            if not pd.isna(row['归属于母公司所有者的其他综合收益']):
                profit_data.other_comprehensive_income_parent = row['归属于母公司所有者的其他综合收益']
            if not pd.isna(row['（一）以后不能重分类进损益的其他综合收益']):
                profit_data.non_reclassifiable_comprehensive_income = row['（一）以后不能重分类进损益的其他综合收益']
            if not pd.isna(row['重新计量设定受益计划变动额']):
                profit_data.benefit_plan_change = row['重新计量设定受益计划变动额']
            if not pd.isna(row['权益法下不能转损益的其他综合收益']):
                profit_data.equity_method_non_reclassifiable = row['权益法下不能转损益的其他综合收益']
            if not pd.isna(row['其他权益工具投资公允价值变动']):
                profit_data.equity_instrument_fair_value_change = row['其他权益工具投资公允价值变动']
            if not pd.isna(row['企业自身信用风险公允价值变动']):
                profit_data.own_credit_risk_fair_value_change = row['企业自身信用风险公允价值变动']
            if not pd.isna(row['（二）以后将重分类进损益的其他综合收益']):
                profit_data.reclassifiable_comprehensive_income = row['（二）以后将重分类进损益的其他综合收益']
            if not pd.isna(row['权益法下可转损益的其他综合收益']):
                profit_data.equity_method_reclassifiable = row['权益法下可转损益的其他综合收益']
            if not pd.isna(row['可供出售金融资产公允价值变动损益']):
                profit_data.available_for_sale_fair_value_change = row['可供出售金融资产公允价值变动损益']
            if not pd.isna(row['其他债权投资公允价值变动']):
                profit_data.debt_investment_fair_value_change = row['其他债权投资公允价值变动']
            if not pd.isna(row['金融资产重分类计入其他综合收益的金额']):
                profit_data.financial_asset_reclassification = row['金融资产重分类计入其他综合收益的金额']
            if not pd.isna(row['其他债权投资信用减值准备']):
                profit_data.debt_investment_credit_impairment = row['其他债权投资信用减值准备']
            if not pd.isna(row['持有至到期投资重分类为可供出售金融资产损益']):
                profit_data.held_to_maturity_reclassification = row['持有至到期投资重分类为可供出售金融资产损益']
            if not pd.isna(row['现金流量套期储备']):
                profit_data.cash_flow_hedge_reserve = row['现金流量套期储备']
            if not pd.isna(row['现金流量套期损益的有效部分']):
                profit_data.cash_flow_hedge_effective_portion = row['现金流量套期损益的有效部分']
            if not pd.isna(row['外币财务报表折算差额']):
                profit_data.foreign_currency_translation = row['外币财务报表折算差额']
            if not pd.isna(row['其他']):
                profit_data.other_items = row['其他']
            if not pd.isna(row['归属于少数股东的其他综合收益']):
                profit_data.minority_other_comprehensive_income = row['归属于少数股东的其他综合收益']
            if not pd.isna(row['综合收益总额']):
                profit_data.total_comprehensive_income = row['综合收益总额']
            if not pd.isna(row['归属于母公司所有者的综合收益总额']):
                profit_data.total_comprehensive_income_parent = row['归属于母公司所有者的综合收益总额']
            if not pd.isna(row['归属于少数股东的综合收益总额']):
                profit_data.minority_comprehensive_income = row['归属于少数股东的综合收益总额']
            if not pd.isna(row['基本每股收益']):
                profit_data.basic_eps = row['基本每股收益']
            if not pd.isna(row['稀释每股收益']):
                profit_data.diluted_eps = row['稀释每股收益']
            try:
                self.profit_db.insert_profit(profit_data)
            except Exception as e:
                logging.error(f"Failed to insert {ticker} profit data: {e}")
                return False
        return True
