from src.back_worker_db.balance_db import BalanceDB, BalanceSheetData
import akshare as ak
import logging
import pandas as pd
from datetime import datetime, timedelta
import time

class BalanceWorker:
    def __init__(self, db: BalanceDB):
        self.db = db

    def download_balance_from_report(ticker: str) -> Boolean:
        try:
            stock_financial_report_sina_df = ak.stock_financial_report_sina(stock=ticker, symbol="资产负债表")
        except Exception as e:
            logging.error(f"Failed to get {ticker} balance from report: {e}")
            return False
        latest_report_date_str = self.db.get_latest_balance_report_date(ticker)
        latest_report_date = datetime.strptime(latest_report_date_str, '%Y%m%d') if latest_report_date_str else datetime(1900, 1, 1)
        for index, row in stock_financial_report_sina_df.iterrows():
            report_period = row['报告日']
            if datetime.strptime(report_period, '%Y%m%d') <= latest_report_date:
                continue
            logging.info(f"Processing {ticker} balance report {report_period}")
            data = BalanceSheetData(
                ticker=ticker,
                report_period=report_period,
                current_assets=row['流动资产'],
                monetary_funds=row['货币资金'],
                data_source=row['数据源'],
                is_audited=row['是否审计'],
                announcement_date=row['公告日期'],
                currency=row['币种'],
                report_type=row['类型'],
                update_date = row['更新日期']
                )
            if not pd.isna(data.settlement_reserves):
                data.settlement_reserves = row['结算备付金']
            if not pd.isna(data.lending_funds):
                data.lending_funds = row['拆出资金']
            if not pd.isna(data.trading_financial_assets):
                data.trading_financial_assets = row['交易性金融资产']
            if not pd.isna(data.bought_sellback_financial_assets):
                data.bought_sellback_financial_assets = row['买入返售金融资产']
            if not pd.isna(data.derivative_financial_assets):
                data.derivative_financial_assets = row['衍生金融资产']
            if not pd.isna(data.notes_accounts_receivable):
                data.notes_accounts_receivable = row['应收票据及应收账款']
            if not pd.isna(data.notes_receivable):
                data.notes_receivable = row['应收票据']
            if not pd.isna(data.accounts_receivable):
                data.accounts_receivable = row['应收账款']
            if not pd.isna(data.receivables_financing):
                data.receivables_financing = row['应收款项融资']
            if not pd.isna(row['预付款项']):
                data.prepayments = row['预付款项']
            if not pd.isna(row['应收股利']):
                data.dividends_receivable = row['应收股利']
            if not pd.isna(row['应收利息']):
                data.interest_receivable = row['应收利息']
            if not pd.isna(row['应收保费']):
                data.insurance_receivables = row['应收保费']
            if not pd.isna(row['应收分保账款']):
                data.reinsurance_receivables = row['应收分保账款']
            if not pd.isna(row['应收分保合同准备金']):
                data.reinsurance_contract_reserves_receivable = row['应收分保合同准备金']
            if not pd.isna(row['应收出口退税']):
                data.export_tax_rebates_receivable = row['应收出口退税']
            if not pd.isna(row['应收补贴款']):
                data.subsidies_receivable = row['应收补贴款']
            if not pd.isna(row['应收保证金']):
                data.deposits_receivable = row['应收保证金']
            if not pd.isna(row['内部应收款']):
                data.internal_receivables = row['内部应收款']
            if not pd.isna(row['其他应收款']):
                data.other_receivables = row['其他应收款']
            if not pd.isna(row['其他应收款(合计)']):
                data.other_receivables_total = row['其他应收款(合计)']
            if not pd.isna(row['存货']):
                data.inventories = row['存货']
            if not pd.isna(row['划分为持有待售的资产']):
                data.assets_held_for_sale = row['划分为持有待售的资产']
            if not pd.isna(row['待摊费用']):
                data.deferred_expenses = row['待摊费用']
            if not pd.isna(row['待处理流动资产损益']):
                data.pending_current_asset_gains_losses = row['待处理流动资产损益']
            if not pd.isna(row['一年内到期的非流动资产']):
                data.non_current_assets_due_within_one_year = row['一年内到期的非流动资产']
            if not pd.isna(row['其他流动资产']):
                data.other_current_assets = row['其他流动资产']
            if not pd.isna(row['流动资产合计']):
                data.total_current_assets = row['流动资产合计']
            if not pd.isna(row['非流动资产']):
                data.non_current_assets = row['非流动资产']
            if not pd.isna(row['发放贷款及垫款']):
                data.loans_and_advances = row['发放贷款及垫款']
            if not pd.isna(row['债权投资']):
                data.debt_investments = row['债权投资']
            if not pd.isna(row['其他债权投资']):
                data.other_debt_investments = row['其他债权投资']
            if not pd.isna(row['以公允价值计量且其变动计入其他综合收益的金融资产']):
                data.financial_assets_fvoci = row['以公允价值计量且其变动计入其他综合收益的金融资产']
            if not pd.isna(row['以摊余成本计量的金融资产']):
                data.financial_assets_amortized_cost = row['以摊余成本计量的金融资产']
            if not pd.isna(row['可供出售金融资产']):
                data.available_for_sale_financial_assets = row['可供出售金融资产']
            if not pd.isna(row['长期股权投资']):
                data.long_term_equity_investments = row['长期股权投资']
            if not pd.isna(row['投资性房地产']):
                data.investment_properties = row['投资性房地产']
            if not pd.isna(row['长期应收款']):
                data.long_term_receivables = row['长期应收款']
            if not pd.isna(row['其他权益工具投资']):
                data.other_equity_instruments = row['其他权益工具投资']
            if not pd.isna(row['其他非流动金融资产']):
                data.other_non_current_financial_assets = row['其他非流动金融资产']
            if not pd.isna(row['其他长期投资']):
                data.other_long_term_investments = row['其他长期投资']
            if not pd.isna(row['固定资产原值']):
                data.fixed_assets_original_value = row['固定资产原值']
            if not pd.isna(row['累计折旧']):
                data.accumulated_depreciation = row['累计折旧']
            if not pd.isna(row['固定资产净值']):
                data.fixed_assets_net_value = row['固定资产净值']
            if not pd.isna(row['固定资产减值准备']):
                data.fixed_assets_impairment_provision = row['固定资产减值准备']
            if not pd.isna(row['在建工程合计']):
                data.construction_in_progress_total = row['在建工程合计']
            if not pd.isna(row['在建工程']):
                data.construction_in_progress = row['在建工程']
            if not pd.isna(row['工程物资']):
                data.construction_materials = row['工程物资']
            if not pd.isna(row['固定资产净额']):
                data.fixed_assets_net_amount = row['固定资产净额']
            if not pd.isna(row['固定资产清理']):
                data.fixed_assets_disposal = row['固定资产清理']
            if not pd.isna(row['固定资产及清理合计']):
                data.fixed_assets_and_disposal_total = row['固定资产及清理合计']
            if not pd.isna(row['生产性生物资产']):
                data.productive_biological_assets = row['生产性生物资产']
            if not pd.isna(row['公益性生物资产']):
                data.public_welfare_biological_assets = row['公益性生物资产']
            if not pd.isna(row['油气资产']):
                data.oil_and_gas_assets = row['油气资产']
            # 为 data 赋值合同资产
            if not pd.isna(row['合同资产']):
                data.contract_assets = row['合同资产']
            # 为 data 赋值使用权资产
            if not pd.isna(row['使用权资产']):
                data.right_of_use_assets = row['使用权资产']
            # 为 data 赋值无形资产
            if not pd.isna(row['无形资产']):
                data.intangible_assets = row['无形资产']
            # 为 data 赋值开发支出
            if not pd.isna(row['开发支出']):
                data.development_expenditure = row['开发支出']
            # 为 data 赋值商誉
            if not pd.isna(row['商誉']):
                data.goodwill = row['商誉']
            # 为 data 赋值长期待摊费用
            if not pd.isna(row['长期待摊费用']):
                data.long_term_prepaid_expenses = row['长期待摊费用']
            # 为 data 赋值股权分置流通权
            if not pd.isna(row['股权分置流通权']):
                data.equity_split_circulation_rights = row['股权分置流通权']
            # 为 data 赋值递延所得税资产
            if not pd.isna(row['递延所得税资产']):
                data.deferred_tax_assets = row['递延所得税资产']
            # 为 data 赋值其他非流动资产
            if not pd.isna(row['其他非流动资产']):
                data.other_non_current_assets = row['其他非流动资产']
            # 为 data 赋值非流动资产合计
            if not pd.isna(row['非流动资产合计']):
                data.total_non_current_assets = row['非流动资产合计']
            # 为 data 赋值资产总计
            if not pd.isna(row['资产总计']):
                data.total_assets = row['资产总计']
            # 为 data 赋值流动负债
            if not pd.isna(row['流动负债']):
                data.current_liabilities = row['流动负债']
            # 为 data 赋值短期借款
            if not pd.isna(row['短期借款']):
                data.short_term_borrowings = row['短期借款']
            # 为 data 赋值向中央银行借款
            if not pd.isna(row['向中央银行借款']):
                data.borrowings_from_central_bank = row['向中央银行借款']
            # 为 data 赋值吸收存款及同业存放
            if not pd.isna(row['吸收存款及同业存放']):
                data.deposits_from_banks_and_other_institutions = row['吸收存款及同业存放']
            # 为 data 赋值拆入资金
            if not pd.isna(row['拆入资金']):
                data.borrowings_from_banks = row['拆入资金']
            # 为 data 赋值交易性金融负债
            if not pd.isna(row['交易性金融负债']):
                data.trading_financial_liabilities = row['交易性金融负债']
            # 为 data 赋值衍生金融负债
            if not pd.isna(row['衍生金融负债']):
                data.derivative_financial_liabilities = row['衍生金融负债']
            # 为 data 赋值应付票据及应付账款
            if not pd.isna(row['应付票据及应付账款']):
                data.notes_accounts_payable = row['应付票据及应付账款']
            # 为 data 赋值应付票据
            if not pd.isna(row['应付票据']):
                data.notes_payable = row['应付票据']
            # 为 data 赋值应付账款
            if not pd.isna(row['应付账款']):
                data.accounts_payable = row['应付账款']
            # 为 data 赋值预收款项
            if not pd.isna(row['预收款项']):
                data.advance_receipts = row['预收款项']
            # 为 data 赋值合同负债
            if not pd.isna(row['合同负债']):
                data.contract_liabilities = row['合同负债']
            # 为 data 赋值卖出回购金融资产款
            if not pd.isna(row['卖出回购金融资产款']):
                data.sold_buyback_financial_assets = row['卖出回购金融资产款']
            # 为 data 赋值应付手续费及佣金
            if not pd.isna(row['应付手续费及佣金']):
                data.commission_and_brokerage_payable = row['应付手续费及佣金']
            # 为 data 赋值应付职工薪酬
            if not pd.isna(row['应付职工薪酬']):
                data.employee_benefits_payable = row['应付职工薪酬']
            # 为 data 赋值应交税费
            if not pd.isna(row['应交税费']):
                data.taxes_payable = row['应交税费']
            # 为 data 赋值应付利息
            if not pd.isna(row['应付利息']):
                data.interest_payable = row['应付利息']
            # 为 data 赋值应付股利
            if not pd.isna(row['应付股利']):
                data.dividends_payable = row['应付股利']
            # 为 data 赋值应付保证金
            if not pd.isna(row['应付保证金']):
                data.deposits_payable = row['应付保证金']
            # 为 data 赋值内部应付款
            if not pd.isna(row['内部应付款']):
                data.internal_payables = row['内部应付款']
            # 为 data 赋值其他应付款
            if not pd.isna(row['其他应付款']):
                data.other_payables = row['其他应付款']
            # 为 data 赋值其他应付款合计
            if not pd.isna(row['其他应付款合计']):
                data.other_payables_total = row['其他应付款合计']
            # 为 data 赋值其他应交款
            if not pd.isna(row['其他应交款']):
                data.other_taxes_payable = row['其他应交款']
            # 为 data 赋值担保责任赔偿准备金
            if not pd.isna(row['担保责任赔偿准备金']):
                data.guarantee_liability_compensation_provision = row['担保责任赔偿准备金']
            # 为 data 赋值应付分保账款
            if not pd.isna(row['应付分保账款']):
                data.reinsurance_payables = row['应付分保账款']
            # 为 data 赋值保险合同准备金
            if not pd.isna(row['保险合同准备金']):
                data.insurance_contract_reserves = row['保险合同准备金']
            # 为 data 赋值代理买卖证券款
            if not pd.isna(row['代理买卖证券款']):
                data.securities_trading_agency_payable = row['代理买卖证券款']
            # 为 data 赋值代理承销证券款
            if not pd.isna(row['代理承销证券款']):
                data.securities_underwriting_agency_payable = row['代理承销证券款']
            # 为 data 赋值国际票证结算
            if not pd.isna(row['国际票证结算']):
                data.international_settlement = row['国际票证结算']
            # 为 data 赋值国内票证结算
            if not pd.isna(row['国内票证结算']):
                data.domestic_settlement = row['国内票证结算']
            # 为 data 赋值预提费用
            if not pd.isna(row['预提费用']):
                data.accrued_expenses = row['预提费用']
            # 为 data 赋值预计流动负债
            if not pd.isna(row['预计流动负债']):
                data.estimated_current_liabilities = row['预计流动负债']
            # 为 data 赋值应付短期债券
            if not pd.isna(row['应付短期债券']):
                data.short_term_bonds_payable = row['应付短期债券']
            # 为 data 赋值划分为持有待售的负债
            if not pd.isna(row['划分为持有待售的负债']):
                data.liabilities_held_for_sale = row['划分为持有待售的负债']
            # 为 data 赋值一年内的递延收益
            if not pd.isna(row['一年内的递延收益']):
                data.deferred_income_within_one_year = row['一年内的递延收益']
            # 为 data 赋值一年内到期的非流动负债
            if not pd.isna(row['一年内到期的非流动负债']):
                data.non_current_liabilities_due_within_one_year = row['一年内到期的非流动负债']
            # 为 data 赋值其他流动负债
            if not pd.isna(row['其他流动负债']):
                data.other_current_liabilities = row['其他流动负债']
            # 为 data 赋值流动负债合计
            if not pd.isna(row['流动负债合计']):
                data.total_current_liabilities = row['流动负债合计']
            # 为 data 赋值非流动负债
            if not pd.isna(row['非流动负债']):
                data.non_current_liabilities = row['非流动负债']
            # 为 data 赋值长期借款
            if not pd.isna(row['长期借款']):
                data.long_term_borrowings = row['长期借款']
            # 为 data 赋值应付债券
            if not pd.isna(row['应付债券']):
                data.bonds_payable = row['应付债券']
            # 为 data 赋值应付债券：优先股
            if not pd.isna(row['应付债券：优先股']):
                data.bonds_payable_preferred_shares = row['应付债券：优先股']
            # 为 data 赋值应付债券：永续债
            if not pd.isna(row['应付债券：永续债']):
                data.bonds_payable_perpetual_bonds = row['应付债券：永续债']
            # 为 data 赋值租赁负债
            if not pd.isna(row['租赁负债']):
                data.lease_liabilities = row['租赁负债']
            # 为 data 赋值长期应付职工薪酬
            if not pd.isna(row['长期应付职工薪酬']):
                data.long_term_employee_benefits_payable = row['长期应付职工薪酬']
            # 为 data 赋值长期应付款
            if not pd.isna(row['长期应付款']):
                data.long_term_payables = row['长期应付款']
            # 为 data 赋值长期应付款合计
            if not pd.isna(row['长期应付款合计']):
                data.long_term_payables_total = row['长期应付款合计']
            # 为 data 赋值专项应付款
            if not pd.isna(row['专项应付款']):
                data.special_payables = row['专项应付款']
            # 为 data 赋值预计非流动负债
            if not pd.isna(row['预计非流动负债']):
                data.estimated_non_current_liabilities = row['预计非流动负债']
            # 为 data 赋值长期递延收益
            if not pd.isna(row['长期递延收益']):
                data.long_term_deferred_income = row['长期递延收益']
            # 为 data 赋值递延所得税负债
            if not pd.isna(row['递延所得税负债']):
                data.deferred_tax_liabilities = row['递延所得税负债']
            # 为 data 赋值其他非流动负债
            if not pd.isna(row['其他非流动负债']):
                data.other_non_current_liabilities = row['其他非流动负债']
            # 为 data 赋值非流动负债合计
            if not pd.isna(row['非流动负债合计']):
                data.total_non_current_liabilities = row['非流动负债合计']
            # 为 data 赋值负债合计
            if not pd.isna(row['负债合计']):
                data.total_liabilities = row['负债合计']
            # 为 data 赋值所有者权益
            if not pd.isna(row['所有者权益']):
                data.owners_equity = row['所有者权益']
            # 为 data 赋值实收资本(或股本)
            if not pd.isna(row['实收资本(或股本)']):
                data.paid_in_capital = row['实收资本(或股本)']
            # 为 data 赋值其他权益工具
            if not pd.isna(row['其他权益工具']):
                data.other_equity_instruments_equity = row['其他权益工具']
            # 为 data 赋值优先股
            if not pd.isna(row['优先股']):
                data.preferred_shares_equity = row['优先股']
            # 为 data 赋值永续债
            if not pd.isna(row['永续债']):
                data.perpetual_bonds_equity = row['永续债']
            # 为 data 赋值资本公积
            if not pd.isna(row['资本公积']):
                data.capital_reserve = row['资本公积']
            # 为 data 赋值减:库存股
            if not pd.isna(row['减:库存股']):
                data.treasury_stock = row['减:库存股']
            # 为 data 赋值其他综合收益
            if not pd.isna(row['其他综合收益']):
                data.other_comprehensive_income = row['其他综合收益']
            # 为 data 赋值专项储备
            if not pd.isna(row['专项储备']):
                data.special_reserve = row['专项储备']
            # 为 data 赋值盈余公积
            if not pd.isna(row['盈余公积']):
                data.surplus_reserve = row['盈余公积']
            # 为 data 赋值一般风险准备
            if not pd.isna(row['一般风险准备']):
                data.general_risk_provision = row['一般风险准备']
            # 为 data 赋值未确定的投资损失
            if not pd.isna(row['未确定的投资损失']):
                data.undetermined_investment_losses = row['未确定的投资损失']
            # 为 data 赋值未分配利润
            if not pd.isna(row['未分配利润']):
                data.retained_earnings = row['未分配利润']
            # 为 data 赋值拟分配现金股利
            if not pd.isna(row['拟分配现金股利']):
                data.proposed_cash_dividends = row['拟分配现金股利']
            # 为 data 赋值外币报表折算差额
            if not pd.isna(row['外币报表折算差额']):
                data.foreign_currency_translation_differences = row['外币报表折算差额']
            # 为 data 赋值归属于母公司股东权益合计
            if not pd.isna(row['归属于母公司股东权益合计']):
                data.total_equity_attributable_to_parent = row['归属于母公司股东权益合计']
            # 为 data 赋值少数股东权益
            if not pd.isna(row['少数股东权益']):
                data.minority_interests = row['少数股东权益']
            # 为 data 赋值所有者权益(或股东权益)合计
            if not pd.isna(row['所有者权益(或股东权益)合计']):
                data.total_owners_equity = row['所有者权益(或股东权益)合计']
            # 为 data 赋值负债和所有者权益(或股东权益)总计
            if not pd.isna(row['负债和所有者权益(或股东权益)总计']):
                data.total_liabilities_and_owners_equity = row['负债和所有者权益(或股东权益)总计']
            
            try:
                self.db.insert_balance_sheet(data)
            except Exception as e:
                logging.error(f"Error inserting balance sheet data for {ticker}_{report_period}: {e}")