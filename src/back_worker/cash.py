from src.back_worker_db.cash_flow_db import CashFlowDB, CashFlowData
import akshare as ak
import logging
import pandas as pd
from datetime import datetime, timedelta
import time

class CashWorker:
    def __init__(self, cash_db: CashFlowDB):
        self.cash_db = cash_db
    
    def download_cash_flow(self, ticker:str):
        try:
            stock_financial_report_sina_df = ak.stock_financial_report_sina(stock=ticker, symbol="现金流量表")
        except Exception as e:
            logging.error(f"Failed to get {ticker} cash flow from report: {e}")
            return False
        
        latest_report_date_str = self.cash_db.get_latest_cash_flow_report_date(ticker)
        latest_report_date = datetime.strptime(latest_report_date_str, '%Y%m%d') if latest_report_date_str else datetime(1900, 1, 1)
        for index, row in stock_financial_report_sina_df.iterrows():
            report_date = datetime.strptime(row['报告日'], '%Y%m%d')
            if report_date <= latest_report_date:
                continue
            logging.info(f"Downloading {ticker} cash flow report: {row['报告日']}")
            cash_flow_data = CashFlowData.model_construct()
            cash_flow_data.ticker = ticker
            cash_flow_data.report_date = row['报告日']
            cash_flow_data.data_source = row['数据源']
            cash_flow_data.is_audited = row['是否审计']
            cash_flow_data.announcement_date = row['公告日期']
            cash_flow_data.currency = row['币种']
            cash_flow_data.report_type = row['类型']
            cash_flow_data.update_date = row['更新日期']

            if not pd.isna(row['经营活动产生的现金流量']):
                cash_flow_data.operating_cash_flow = float(row['经营活动产生的现金流量'])
            if not pd.isna(row['销售商品、提供劳务收到的现金']):
                cash_flow_data.cash_from_sales = float(row['销售商品、提供劳务收到的现金'])
            if not pd.isna(row['客户存款和同业存放款项净增加额']):
                cash_flow_data.net_increase_in_customer_deposits = float(row['客户存款和同业存放款项净增加额'])
            if not pd.isna(row['向中央银行借款净增加额']):
                cash_flow_data.net_increase_in_central_bank_borrowing = float(row['向中央银行借款净增加额'])
            if not pd.isna(row['向其他金融机构拆入资金净增加额']):
                cash_flow_data.net_increase_in_interbank_borrowing = float(row['向其他金融机构拆入资金净增加额'])
            if not pd.isna(row['收到原保险合同保费取得的现金']):
                cash_flow_data.cash_from_insurance_premiums = float(row['收到原保险合同保费取得的现金'])
            if not pd.isna(row['收到再保险业务现金净额']):
                cash_flow_data.net_cash_from_reinsurance = float(row['收到再保险业务现金净额'])
            if not pd.isna(row['保户储金及投资款净增加额']):
                cash_flow_data.net_increase_in_policyholder_deposits = float(row['保户储金及投资款净增加额'])
            if not pd.isna(row['处置交易性金融资产净增加额']):
                cash_flow_data.net_increase_in_trading_securities = float(row['处置交易性金融资产净增加额'])
            if not pd.isna(row['收取利息、手续费及佣金的现金']):
                cash_flow_data.cash_from_interest_fees_commissions = float(row['收取利息、手续费及佣金的现金'])
            if not pd.isna(row['拆入资金净增加额']):
                cash_flow_data.net_increase_in_borrowed_funds = float(row['拆入资金净增加额'])
            if not pd.isna(row['回购业务资金净增加额']):
                cash_flow_data.net_increase_in_repurchase_funds = float(row['回购业务资金净增加额'])
            if not pd.isna(row['收到的税费返还']):
                cash_flow_data.tax_refunds_received = float(row['收到的税费返还'])
            if not pd.isna(row['收到的其他与经营活动有关的现金']):
                cash_flow_data.other_operating_cash_inflows = float(row['收到的其他与经营活动有关的现金'])
            if not pd.isna(row['经营活动现金流入小计']):
                cash_flow_data.total_operating_cash_inflows = float(row['经营活动现金流入小计'])
            if not pd.isna(row['购买商品、接受劳务支付的现金']):
                cash_flow_data.cash_paid_for_goods_services = float(row['购买商品、接受劳务支付的现金'])
            if not pd.isna(row['客户贷款及垫款净增加额']):
                cash_flow_data.net_increase_in_customer_loans = float(row['客户贷款及垫款净增加额'])
            if not pd.isna(row['存放中央银行和同业款项净增加额']):
                cash_flow_data.net_increase_in_central_bank_deposits = float(row['存放中央银行和同业款项净增加额'])
            if not pd.isna(row['支付原保险合同赔付款项的现金']):
                cash_flow_data.cash_paid_for_insurance_claims = float(row['支付原保险合同赔付款项的现金'])
            if not pd.isna(row['支付利息、手续费及佣金的现金']):
                cash_flow_data.cash_paid_for_interest_fees_commissions = float(row['支付利息、手续费及佣金的现金'])
            if not pd.isna(row['支付保单红利的现金']):
                cash_flow_data.cash_paid_for_policy_dividends = float(row['支付保单红利的现金'])
            if not pd.isna(row['支付给职工以及为职工支付的现金']):
                cash_flow_data.cash_paid_to_employees = float(row['支付给职工以及为职工支付的现金'])
            if not pd.isna(row['支付的各项税费']):
                cash_flow_data.taxes_paid = float(row['支付的各项税费'])
            if not pd.isna(row['支付的其他与经营活动有关的现金']):
                cash_flow_data.other_operating_cash_outflows = float(row['支付的其他与经营活动有关的现金'])
            if not pd.isna(row['经营活动现金流出小计']):
                cash_flow_data.total_operating_cash_outflows = float(row['经营活动现金流出小计'])
            if not pd.isna(row['经营活动产生的现金流量净额']):
                cash_flow_data.net_operating_cash_flow = float(row['经营活动产生的现金流量净额'])
            if not pd.isna(row['投资活动产生的现金流量']):
                cash_flow_data.investing_cash_flow = float(row['投资活动产生的现金流量'])
            if not pd.isna(row['收回投资所收到的现金']):
                cash_flow_data.cash_from_investment_recovery = float(row['收回投资所收到的现金'])
            if not pd.isna(row['取得投资收益收到的现金']):
                cash_flow_data.cash_from_investment_returns = float(row['取得投资收益收到的现金'])
            if not pd.isna(row['处置固定资产、无形资产和其他长期资产所收回的现金净额']):
                cash_flow_data.cash_from_asset_disposal = float(row['处置固定资产、无形资产和其他长期资产所收回的现金净额'])
            if not pd.isna(row['处置子公司及其他营业单位收到的现金净额']):
                cash_flow_data.cash_from_subsidiary_disposal = float(row['处置子公司及其他营业单位收到的现金净额'])
            if not pd.isna(row['收到的其他与投资活动有关的现金']):
                cash_flow_data.other_investing_cash_inflows = float(row['收到的其他与投资活动有关的现金'])
            if not pd.isna(row['减少质押和定期存款所收到的现金']):
                cash_flow_data.cash_from_reduced_deposits = float(row['减少质押和定期存款所收到的现金'])
            if not pd.isna(row['处置可供出售金融资产净增加额']):
                cash_flow_data.net_increase_in_available_for_sale_securities = float(row['处置可供出售金融资产净增加额'])
            if not pd.isna(row['投资活动现金流入小计']):
                cash_flow_data.total_investing_cash_inflows = float(row['投资活动现金流入小计'])
            if not pd.isna(row['购建固定资产、无形资产和其他长期资产所支付的现金']):
                cash_flow_data.cash_paid_for_assets = float(row['购建固定资产、无形资产和其他长期资产所支付的现金'])
            if not pd.isna(row['投资所支付的现金']):
                cash_flow_data.cash_paid_for_investments = float(row['投资所支付的现金'])
            if not pd.isna(row['质押贷款净增加额']):
                cash_flow_data.net_increase_in_pledged_loans = float(row['质押贷款净增加额'])
            if not pd.isna(row['取得子公司及其他营业单位支付的现金净额']):
                cash_flow_data.cash_paid_for_subsidiary_acquisition = float(row['取得子公司及其他营业单位支付的现金净额'])
            if not pd.isna(row['增加质押和定期存款所支付的现金']):
                cash_flow_data.cash_paid_for_increased_deposits = float(row['增加质押和定期存款所支付的现金'])
            if not pd.isna(row['支付的其他与投资活动有关的现金']):
                cash_flow_data.other_investing_cash_outflows = float(row['支付的其他与投资活动有关的现金'])
            if not pd.isna(row['投资活动现金流出小计']):
                cash_flow_data.total_investing_cash_outflows = float(row['投资活动现金流出小计'])
            if not pd.isna(row['投资活动产生的现金流量净额']):
                cash_flow_data.net_investing_cash_flow = float(row['投资活动产生的现金流量净额'])
            if not pd.isna(row['筹资活动产生的现金流量']):
                cash_flow_data.financing_cash_flow = float(row['筹资活动产生的现金流量'])
            if not pd.isna(row['吸收投资收到的现金']):
                cash_flow_data.cash_from_equity_financing = float(row['吸收投资收到的现金'])
            if not pd.isna(row['子公司吸收少数股东投资收到的现金']):
                cash_flow_data.cash_from_minority_investment = float(row['子公司吸收少数股东投资收到的现金'])
            if not pd.isna(row['取得借款收到的现金']):
                cash_flow_data.cash_from_borrowing = float(row['取得借款收到的现金'])
            if not pd.isna(row['发行债券收到的现金']):
                cash_flow_data.cash_from_bond_issuance = float(row['发行债券收到的现金'])
            if not pd.isna(row['收到其他与筹资活动有关的现金']):
                cash_flow_data.other_financing_cash_inflows = float(row['收到其他与筹资活动有关的现金'])
            if not pd.isna(row['筹资活动现金流入小计']):
                cash_flow_data.total_financing_cash_inflows = float(row['筹资活动现金流入小计'])
            if not pd.isna(row['偿还债务支付的现金']):
                cash_flow_data.cash_paid_for_debt_repayment = float(row['偿还债务支付的现金'])
            if not pd.isna(row['分配股利、利润或偿付利息所支付的现金']):
                cash_flow_data.cash_paid_for_dividends_interest = float(row['分配股利、利润或偿付利息所支付的现金'])
            if not pd.isna(row['子公司支付给少数股东的股利、利润']):
                cash_flow_data.cash_paid_to_minority_shareholders = float(row['子公司支付给少数股东的股利、利润'])
            if not pd.isna(row['支付其他与筹资活动有关的现金']):
                cash_flow_data.other_financing_cash_outflows = float(row['支付其他与筹资活动有关的现金'])
            if not pd.isna(row['筹资活动现金流出小计']):
                cash_flow_data.total_financing_cash_outflows = float(row['筹资活动现金流出小计'])
            if not pd.isna(row['筹资活动产生的现金流量净额']):
                cash_flow_data.net_financing_cash_flow = float(row['筹资活动产生的现金流量净额'])
            if not pd.isna(row['汇率变动对现金及现金等价物的影响']):
                cash_flow_data.exchange_rate_effect = float(row['汇率变动对现金及现金等价物的影响'])
            if not pd.isna(row['现金及现金等价物净增加额']):
                cash_flow_data.net_cash_increase = float(row['现金及现金等价物净增加额'])
            if not pd.isna(row['期初现金及现金等价物余额']):
                cash_flow_data.beginning_cash_balance = float(row['期初现金及现金等价物余额'])
            if not pd.isna(row['现金的期末余额']):
                cash_flow_data.ending_cash_balance_cash = float(row['现金的期末余额'])
            if not pd.isna(row['现金的期初余额']):
                cash_flow_data.beginning_cash_balance_cash = float(row['现金的期初余额'])
            if not pd.isna(row['现金等价物的期末余额']):
                cash_flow_data.ending_cash_equivalents_balance = float(row['现金等价物的期末余额'])
            if not pd.isna(row['现金等价物的期初余额']):
                cash_flow_data.beginning_cash_equivalents_balance = float(row['现金等价物的期初余额'])
            if not pd.isna(row['期末现金及现金等价物余额']):
                cash_flow_data.ending_total_cash_balance = float(row['期末现金及现金等价物余额'])
            try:
                self.cash_db.insert_cash_flow(cash_flow_data)
            except Exception as e:
                logging.error(f"Failed to insert {ticker} cash flow report: {e}")
                return False
        return True