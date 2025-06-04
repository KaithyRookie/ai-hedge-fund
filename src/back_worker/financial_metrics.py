import logging
from src.back_worker_db.stock_db import StockType
from src.back_worker_db.financial_metrics_db import FinancialMetricsDB
import akshare as ak
from datetime import datetime, timedelta
from src.data.models import FinancialMetrics

class FinancialMetricsWorker:
    def __init__(self, financial_metrics_db: FinancialMetricsDB):
        self.financial_metrics_db = financial_metrics_db

    def get_financial_metrics(self, ticker: str, stock_type: StockType):
        if stock_type == StockType.HK:
            stock_financial_metric_dict, financial_report_date_list = self.get_stock_hk_financial_metrics(ticker)
        elif stock_type == StockType.A:
            stock_financial_metric_dict, financial_report_date_list = self.get_stock_A_financial_metrics(ticker)
        
        for report_date, financial_metric in stock_financial_metric_dict.items():
            financial_metrics = FinancialMetrics(
                ticker=ticker,
                period=report_date,
                market_cap=financial_metric['market_cap'],
                enterprise_value=financial_metric['enterprise_value'],
                price_to_earnings_ratio=financial_metric['pe_ratio'],
                price_to_book_ratio=financial_metric['pb_ratio'],
                price_to_sales_ratio=financial_metric['ps_ratio'],
                enterprise_value_to_ebitda_ratio=financial_metric['enterprise_value_to_ebitda_ratio'],
                enterprise_value_to_revenue_ratio=financial_metric['enterprise_value_to_revenue_ratio'],
                free_cash_flow_yield=financial_metric['free_cash_flow_yield'],
                peg_ratio=financial_metric['peg_ratio'],
                gross_margin=financial_metric['gross_margin'],
                operating_margin=financial_metric['operating_margin'],
                net_margin=financial_metric['net_margin'],
                return_on_equity=financial_metric['return_on_equity'],
                return_on_assets=financial_metric['return_on_assets'],
                return_on_invested_capital=financial_metric['return_on_invested_capital'],
                asset_turnover=financial_metric['asset_turnover'],
                inventory_turnover=financial_metric['inventory_turnover'],
                receivables_turnover=financial_metric['receivables_turnover'],
                days_sales_outstanding=financial_metric['days_sales_outstanding'],
                operating_cycle=financial_metric['operating_cycle'],
                working_capital_turnover=financial_metric['working_capital_turnover'],
                current_ratio=financial_metric['current_ratio'],
                quick_ratio=financial_metric['quick_ratio'],
                cash_ratio=financial_metric['cash_ratio'],
                operating_cash_flow_ratio=financial_metric['operating_cash_flow_ratio'],
                debt_to_equity=financial_metric['debt_to_equity'],
                debt_to_assets=financial_metric['debt_to_assets'],
                interest_coverage=financial_metric['interest_coverage'],
                revenue_growth=financial_metric['revenue_growth'],
                earnings_growth=financial_metric['earnings_growth'],
                book_value_growth=financial_metric['book_value_growth'],
                earnings_per_share_growth=financial_metric['earnings_per_share_growth'],
                free_cash_flow_growth=financial_metric['free_cash_flow_growth'],
                operating_income_growth=financial_metric['operating_income_growth'],
                ebitda_growth=financial_metric['ebitda_growth'],
                payout_ratio=financial_metric['payout_ratio'],
                earnings_per_share=financial_metric['earnings_per_share'],
                book_value_per_share=financial_metric['book_value_per_share'],
                fcff_per_share=financial_metric['fcff_per_share'],
                fcfe_per_share=financial_metric['fcfe_per_share']
            )
            self.financial_metrics_db.insert_financial_metrics(financial_metrics, ticker)
    
    def get_stock_hk_financial_metrics(self, ticker: str):
    
    def get_stock_hk_financial_report(self, ticker: str):
        stock_financial_metric_dict = {}
        financial_report_date_list = []
        stock_financial_hk_analysis_indicator_em_df = ak.stock_financial_hk_analysis_indicator_em(symbol=ticker, indicator="报告期")
        for index, row in stock_financial_hk_analysis_indicator_em_df.iterrows():
            report_date = row['STD_REPORT_DATE']

        stock_financial_hk_debt_df = ak.stock_financial_hk_report_em(stock=ticker, symbol="资产负债表", indicator="报告期")
        for index, row in stock_financial_hk_debt_df.iterrows():
            data_date = row['STD_REPORT_DATE']
            financial_report_date_list.append(datetime.strptime(data_date, '%Y-%m-%d'))
            liquid_assets = row['流动资产合计']
            fixed_assets = row['非流动资产合计']
            total_assets = row['资产总计']
            current_liabilities = row['流动负债合计']
            non_current_liabilities = row['非流动负债合计']
            total_liabilities = row['负债合计']
            # 归属于母公司股东权益合计
            belong_to_parent_company_equity = row['归属于母公司股东权益合计']
            # 所有者权益(或股东权益)合计
            total_equity = row['所有者权益(或股东权益)合计']
            # 短期借款
            short_term_loan = row['短期借款']
            # 一年内到期的非流动负债（有息部分）
            non_current_liabilities_due_in_one_year = row['一年内到期的非流动负债']
            # 长期借款
            long_term_loan = row['长期借款']
            # 应付债券
            bonds_payable = row['应付债券']
            # 应收票据及应收账款
            accounts_receivable_and_notes_receivable = row['应收票据及应收账款']
            # 租赁负债
            lease_liabilities = row['租赁负债']

            # 货币资金
            monetary_funds = row['货币资金']
            # 交易性金融资产
            trading_financial_assets = row['交易性金融资产']
            # 其他应收款(合计)
            other_receivables = row['其他应收款(合计)']

            # 存货
            inventory = row['存货']
            # 应收账款
            accounts_receivable = row['应收账款']
            # 预付账款
            prepaid_accounts = row['预付账款']

            # 交易性金融资产
            trading_financial_assets = row['交易性金融资产']

            # 总债务
            total_debt = short_term_loan + non_current_liabilities_due_in_one_year + long_term_loan + bonds_payable + lease_liabilities

            # 现金及现金等价物
            cash_and_cash_equivalents = monetary_funds + trading_financial_assets

            # 速动资产
            quick_assets = liquid_assets - inventory - prepaid_accounts

            # 投资资本 = 股东权益+有息负债
            investment_capital = total_equity + short_term_loan + non_current_liabilities_due_in_one_year + long_term_loan + bonds_payable

            # 营运资金
            working_capital = liquid_assets - current_liabilities

            # 流动比率
            current_ratio = liquid_assets / current_liabilities

            # 速动比率
            quick_ratio = quick_assets / current_liabilities

            # 现金比率
            cash_ratio = cash_and_cash_equivalents / current_liabilities

            # 债务权益比
            debt_to_equity_ratio = total_debt / total_equity

            # 总债务除以总资产
            debt_to_assets_ratio = total_debt / total_assets

            stock_financial_metric_dict[data_date] = {
                'liquid_assets': liquid_assets,
                'fixed_assets': fixed_assets,
                'total_assets': total_assets,
                'current_liabilities': current_liabilities,
                'non_current_liabilities': non_current_liabilities,
                'total_liabilities': total_liabilities,
                'total_equity': total_equity,
                'belong_to_parent_company_equity': belong_to_parent_company_equity,
                'investment_capital': investment_capital,
                'inventory': inventory,
                'accounts_receivable': accounts_receivable,
                'accounts_receivable_and_notes_receivable': accounts_receivable_and_notes_receivable,
                'working_capital': working_capital,
                'current_ratio': current_ratio,
                'quick_ratio': quick_ratio,
                'cash_ratio': cash_ratio,
                'debt_to_equity_ratio': debt_to_equity_ratio,
                'debt_to_assets_ratio': debt_to_assets_ratio
            }
        stock_financial_hk_profit_df = ak.stock_financial_hk_report_em(stock=ticker, symbol="利润表", indicator="报告期")
        for index, row in stock_financial_hk_profit_df.iterrows():
            data_date = row['STD_REPORT_DATE']
            revenue = row['营业总收入']
            operating_revenue = row['营业利润']
            operating_income = row['营业收入']
            cost_of_goods_sold_total = row['营业总成本']
            # 营业成本
            cost_of_goods_sold = row['营业成本']

            net_profit = row['净利润']
            # 利息支出
            interest_expense = row['利息支出']
            # 所得税费用
            tax_expense = row['所得税费用']

            # 利润总额
            profit_total = row['利润总额']

            # 基本每股收益
            basic_eps = net_profit / stock_financial_metric_dict[data_date]['total_share']

            # 实际税率(未参考财报附注调整)
            actual_tax_rate = tax_expense / profit_total

            # 毛利
            gross_profit = revenue - cost_of_goods_sold
            # 毛利率
            gross_profit_margin = gross_profit / revenue

            operating_margin = operating_income / revenue

            # 净利率
            net_profit_margin = net_profit / revenue

            # NOPAT
            nopat = operating_revenue / (1 - actual_tax_rate)
            

            stock_financial_metric_dict[data_date]['revenue'] = revenue
            stock_financial_metric_dict[data_date]['operating_income'] = operating_income
            stock_financial_metric_dict[data_date]['net_profit'] = net_profit   
            stock_financial_metric_dict[data_date]['cost_of_goods_sold'] = cost_of_goods_sold
            stock_financial_metric_dict[data_date]['cost_of_goods_sold_total'] = cost_of_goods_sold_total
            stock_financial_metric_dict[data_date]['interest_expense'] = interest_expense
            stock_financial_metric_dict[data_date]['tax_expense'] = tax_expense
            stock_financial_metric_dict[data_date]['gross_profit'] = gross_profit
            stock_financial_metric_dict[data_date]['gross_profit_margin'] = gross_profit_margin
            stock_financial_metric_dict[data_date]['operating_margin'] = operating_margin
            stock_financial_metric_dict[data_date]['net_profit_margin'] = net_profit_margin
            stock_financial_metric_dict[data_date]['nopat'] = nopat
            stock_financial_metric_dict[data_date]['basic_eps'] = basic_eps

        stock_financial_hk_cash_df = ak.stock_financial_hk_report_em(stock=ticker, symbol="现金流量表", indicator="报告期")
        for index, row in stock_financial_hk_cash_df.iterrows():
            data_date = row['STD_REPORT_DATE']
            operating_cash_flow = row['经营活动产生的现金流量净额']
            cash_and_cash_equivalents_begin = row['期初现金及现金等价物余额']
            cash_and_cash_equivalents_end = row['期末现金及现金等价物余额']
            cash_and_cash_equivalents_change = row['现金及现金等价物净增加额']
            # 购建固定资产、无形资产和其他长期资产所支付的现金
            purchase_fixed_assets = row['购建固定资产、无形资产和其他长期资产所支付的现金']
            # 折旧及摊销
            depreciation_and_amortization = row['折旧及摊销']

            stock_financial_metric_dict[data_date]['operating_cash_flow'] = operating_cash_flow
            stock_financial_metric_dict[data_date]['cash_and_cash_equivalents_begin'] = cash_and_cash_equivalents_begin
            stock_financial_metric_dict[data_date]['cash_and_cash_equivalents_end'] = cash_and_cash_equivalents_end
            stock_financial_metric_dict[data_date]['cash_and_cash_equivalents_change'] = cash_and_cash_equivalents_change
            stock_financial_metric_dict[data_date]['purchase_fixed_assets'] = purchase_fixed_assets
            fcf = operating_cash_flow - purchase_fixed_assets
            stock_financial_metric_dict[data_date]['fcf'] = fcf
            stock_financial_metric_dict[data_date]['depreciation_and_amortization'] = depreciation_and_amortization
        return stock_financial_metric_dict, financial_report_date_list
    
    def get_stock_A_financial_metrics(self, ticker: str):
        stock_A_value_em = self.get_stock_A_value_em(ticker)
        stock_A_financial_report, financial_report_date_list = self.get_stock_A_financial_report(ticker)
        stock_A_financial_metrics = []
        for value_em in stock_A_value_em:
            data_date = value_em['data_date']
            report_date = None
            # 遍历financial_report_date_list，找到与data_date最接近的报告日期
            for financial_report_date in financial_report_date_list:
                if financial_report_date <= data_date:
                    report_date = financial_report_date
                    break
            if report_date is not None:
                market_cap = value_em['market_cap']
                current_report_data = current_report_data
                # 企业价值
                enterprise_value = market_cap + current_report_data['total_liabilities'] - current_report_data['cash_and_cash_equivalents_end']
                value_em['enterprise_value'] = enterprise_value

                # EBITDA
                ebitda = current_report_data['ebitda']
                # 企业价值与 EBITDA 比率
                enterprise_value_to_ebitda_ratio = enterprise_value / ebitda
                value_em['enterprise_value_to_ebitda_ratio'] = enterprise_value_to_ebitda_ratio if enterprise_value_to_ebitda_ratio != 0 else None

                # 企业价值收入比
                revenue = current_report_data['revenue']
                enterprise_value_to_revenue_ratio = enterprise_value / revenue
                value_em['enterprise_value_to_revenue_ratio'] = enterprise_value_to_revenue_ratio

                # 自由现金流收益率
                fcf = current_report_data['fcf']
                fcf_yield = fcf / enterprise_value
                value_em['fcf_yield'] = fcf_yield

                # 毛利率
                value_em['gross_margin'] = current_report_data['gross_profit_margin']

                # 营业利润率    
                value_em['operating_margin'] = current_report_data['operating_margin']

                # 净利率
                value_em['net_profit_margin'] = current_report_data['net_profit_margin']

                # ROE
                value_em['roe'] = current_report_data['net_profit'] / current_report_data['total_equity']

                # ROA
                value_em['roa'] = current_report_data['net_profit'] / current_report_data['total_assets']

                # ROIC
                value_em['roic'] = current_report_data['nopat'] / current_report_data['investment_capital']

                # 总资产周转率
                value_em['total_assets_turnover'] = current_report_data['operating_income'] / current_report_data['total_assets']

                # 库存周转率
                value_em['inventory_turnover'] = current_report_data['cost_of_goods_sold'] / current_report_data['inventory']

                # 应收账款周转率
                value_em['accounts_receivable_turnover'] = current_report_data['operating_income'] / current_report_data['accounts_receivable_and_notes_receivable']

                # 应收账款占收入比例
                value_em['days_sales_outstanding'] = current_report_data['accounts_receivable_and_notes_receivable'] / current_report_data['operating_income']

                value_em['operating_cycle'] =value_em['inventory_turnover'] + value_em['accounts_receivable_turnover']

                value_em['working_capital_turnover'] = current_report_data['operating_income'] / current_report_data['working_capital']
                value_em['current_ratio'] = current_report_data['current_ratio']
                value_em['quick_ratio'] = current_report_data['quick_ratio']
                value_em['cash_ratio'] = current_report_data['cash_ratio']

                # operating_cash_flow_ratio
                value_em['operating_cash_flow_ratio'] = current_report_data['operating_cash_flow'] / current_report_data['current_liabilities']
                
                value_em['debt_to_equity'] = current_report_data['debt_to_equity_ratio']
                value_em['debt_to_assets'] = current_report_data['debt_to_assets_ratio']

                # 利息保障倍数
                value_em['interest_coverage'] = current_report_data['operating_income'] / current_report_data['interest_expense']
                
                # 同比增长，根据当前报告的日期，先获取上一年的日期，然后获取上一年的数据，然后计算同比增长
                last_year_date = datetime.strptime(report_date, '%Y%m%d') - timedelta(days=365)
                last_year_date_str = last_year_date.strftime('%Y%m%d')
                last_year_data = stock_A_financial_report[last_year_date_str]

                # 收入同比增长
                revenue_growth = (current_report_data['revenue'] - last_year_data['revenue']) / last_year_data['revenue']
                value_em['revenue_growth'] = revenue_growth

                # 收益同比增长
                operating_income_growth = (current_report_data['operating_income'] - last_year_data['operating_income']) / last_year_data['operating_income']
                value_em['earnings_growth'] = operating_income_growth

                # 账面价值同比增长
                book_value_growth = (current_report_data['total_equity'] - last_year_data['total_equity']) / last_year_data['total_equity']
                value_em['book_value_growth'] = book_value_growth

                # 在此期间每股收益增长
                eps_growth = (current_report_data['basic_eps'] - last_year_data['basic_eps']) / last_year_data['basic_eps']
                value_em['earnings_per_share_growth'] = eps_growth

                # 自由现金流同比增长
                free_cash_flow_growth = (current_report_data['fcf'] - last_year_data['fcf']) / last_year_data['fcf']
                value_em['free_cash_flow_growth'] = free_cash_flow_growth

                # 在此期间营业收入增长
                operating_income_growth = (current_report_data['operating_income'] - last_year_data['operating_income']) / last_year_data['operating_income']
                value_em['operating_income_growth'] = operating_income_growth

                # 在此期间营业利润增长
                operating_profit_growth = (current_report_data['operating_profit'] - last_year_data['operating_profit']) / last_year_data['operating_profit']
                value_em['operating_profit_growth'] = operating_profit_growth

                # EBITDA 增长
                ebitda_growth = (current_report_data['ebitda'] - last_year_data['ebitda']) / last_year_data['ebitda']
                value_em['ebitda_growth'] = ebitda_growth   

                # 支付的股息占净收入的百分比
                dividend_payout_ratio = current_report_data['dividend_payout_ratio']
                value_em['payout_ratio'] = dividend_payout_ratio

                # 净收入除以加权平均流通股
                earnings_per_share = current_report_data['basic_eps']
                value_em['earnings_per_share'] = earnings_per_share

                # 股东权益除以已发行股份
                book_value_per_share = current_report_data['book_value']
                value_em['book_value_per_share'] = book_value_per_share

                # 企业自由现金流除以已发行股票
                fcff_per_share = current_report_data['fcff_per_share']
                value_em['fcff_per_share'] = fcff_per_share

                # 股东自由现金流除以已发行股票
                fcfe_per_share = current_report_data['fcfe_per_share']
                value_em['fcfe_per_share'] = fcfe_per_share
                stock_A_financial_metrics.append(value_em)
            else:
                value_em['enterprise_value'] = None
        return stock_A_financial_metrics
    
    
    def get_stock_A_financial_report(self, ticker: str):
        stock_financial_debt_df = ak.stock_financial_report_sina(stock=ticker, symbol="资产负债表")
        stock_financial_metric_dict = {}
        financial_report_date_list = [] # 记录报告的时间，时间类型为datetime
        for index, row in stock_financial_debt_df.iterrows():
            data_date = row['报告日']
            financial_report_date_list.append(datetime.strptime(data_date, '%Y%m%d'))
            liquid_assets = row['流动资产合计']
            fixed_assets = row['非流动资产合计']
            total_assets = row['资产总计']
            current_liabilities = row['流动负债合计']
            non_current_liabilities = row['非流动负债合计']
            total_liabilities = row['负债合计']
            # 归属于母公司股东权益合计
            belong_to_parent_company_equity = row['归属于母公司股东权益合计']
            # 所有者权益(或股东权益)合计
            total_equity = row['所有者权益(或股东权益)合计']
            # 短期借款
            short_term_loan = row['短期借款']
            # 一年内到期的非流动负债（有息部分）
            non_current_liabilities_due_in_one_year = row['一年内到期的非流动负债']
            # 长期借款
            long_term_loan = row['长期借款']
            # 应付债券
            bonds_payable = row['应付债券']
            # 应收票据及应收账款
            accounts_receivable_and_notes_receivable = row['应收票据及应收账款']
            # 租赁负债
            lease_liabilities = row['租赁负债']

            # 货币资金
            monetary_funds = row['货币资金']
            # 交易性金融资产
            trading_financial_assets = row['交易性金融资产']
            # 其他应收款(合计)
            other_receivables = row['其他应收款(合计)']

            # 存货
            inventory = row['存货']
            # 应收账款
            accounts_receivable = row['应收账款']
            # 预付账款
            prepaid_accounts = row['预付账款']

            # 交易性金融资产
            trading_financial_assets = row['交易性金融资产']

            # 总债务
            total_debt = short_term_loan + non_current_liabilities_due_in_one_year + long_term_loan + bonds_payable + lease_liabilities

            # 现金及现金等价物
            cash_and_cash_equivalents = monetary_funds + trading_financial_assets

            # 速动资产
            quick_assets = liquid_assets - inventory - prepaid_accounts

            # 投资资本 = 股东权益+有息负债
            investment_capital = total_equity + short_term_loan + non_current_liabilities_due_in_one_year + long_term_loan + bonds_payable

            # 营运资金
            working_capital = liquid_assets - current_liabilities

            # 流动比率
            current_ratio = liquid_assets / current_liabilities

            # 速动比率
            quick_ratio = quick_assets / current_liabilities

            # 现金比率
            cash_ratio = cash_and_cash_equivalents / current_liabilities

            # 债务权益比
            debt_to_equity_ratio = total_debt / total_equity

            # 总债务除以总资产
            debt_to_assets_ratio = total_debt / total_assets

            stock_financial_metric_dict[data_date] = {
                'liquid_assets': liquid_assets,
                'fixed_assets': fixed_assets,
                'total_assets': total_assets,
                'current_liabilities': current_liabilities,
                'non_current_liabilities': non_current_liabilities,
                'total_liabilities': total_liabilities,
                'total_equity': total_equity,
                'belong_to_parent_company_equity': belong_to_parent_company_equity,
                'investment_capital': investment_capital,
                'inventory': inventory,
                'accounts_receivable': accounts_receivable,
                'accounts_receivable_and_notes_receivable': accounts_receivable_and_notes_receivable,
                'working_capital': working_capital,
                'current_ratio': current_ratio,
                'quick_ratio': quick_ratio,
                'cash_ratio': cash_ratio,
                'debt_to_equity_ratio': debt_to_equity_ratio,
                'debt_to_assets_ratio': debt_to_assets_ratio
            }
        stock_financial_profit_df = ak.stock_financial_report_sina(stock=ticker, symbol="利润表")
        for index, row in stock_financial_profit_df.iterrows():
            data_date = row['报告日']
            revenue = row['营业总收入']
            operating_revenue = row['营业利润']
            operating_income = row['营业收入']
            cost_of_goods_sold_total = row['营业总成本']
            # 营业成本
            cost_of_goods_sold = row['营业成本']

            net_profit = row['净利润']
            # 利息支出
            interest_expense = row['利息支出']
            # 所得税费用
            tax_expense = row['所得税费用']

            # 利润总额
            profit_total = row['利润总额']

            # 基本每股收益
            basic_eps = net_profit / stock_financial_metric_dict[data_date]['total_share']

            # 实际税率(未参考财报附注调整)
            actual_tax_rate = tax_expense / profit_total

            # 毛利
            gross_profit = revenue - cost_of_goods_sold
            # 毛利率
            gross_profit_margin = gross_profit / revenue

            operating_margin = operating_income / revenue

            # 净利率
            net_profit_margin = net_profit / revenue

            # NOPAT
            nopat = operating_revenue / (1 - actual_tax_rate)
            

            stock_financial_metric_dict[data_date]['revenue'] = revenue
            stock_financial_metric_dict[data_date]['operating_income'] = operating_income
            stock_financial_metric_dict[data_date]['net_profit'] = net_profit   
            stock_financial_metric_dict[data_date]['cost_of_goods_sold'] = cost_of_goods_sold
            stock_financial_metric_dict[data_date]['cost_of_goods_sold_total'] = cost_of_goods_sold_total
            stock_financial_metric_dict[data_date]['interest_expense'] = interest_expense
            stock_financial_metric_dict[data_date]['tax_expense'] = tax_expense
            stock_financial_metric_dict[data_date]['gross_profit'] = gross_profit
            stock_financial_metric_dict[data_date]['gross_profit_margin'] = gross_profit_margin
            stock_financial_metric_dict[data_date]['operating_margin'] = operating_margin
            stock_financial_metric_dict[data_date]['net_profit_margin'] = net_profit_margin
            stock_financial_metric_dict[data_date]['nopat'] = nopat
            stock_financial_metric_dict[data_date]['basic_eps'] = basic_eps

        stock_financial_cash_df = ak.stock_financial_report_sina(stock=ticker, symbol="现金流量表")
        for index, row in stock_financial_cash_df.iterrows():
            data_date = row['报告日']
            operating_cash_flow = row['经营活动产生的现金流量净额']
            cash_and_cash_equivalents_begin = row['期初现金及现金等价物余额']
            cash_and_cash_equivalents_end = row['期末现金及现金等价物余额']
            cash_and_cash_equivalents_change = row['现金及现金等价物净增加额']
            # 购建固定资产、无形资产和其他长期资产所支付的现金
            purchase_fixed_assets = row['购建固定资产、无形资产和其他长期资产所支付的现金']
            stock_financial_metric_dict[data_date]['operating_cash_flow'] = operating_cash_flow
            stock_financial_metric_dict[data_date]['cash_and_cash_equivalents_begin'] = cash_and_cash_equivalents_begin
            stock_financial_metric_dict[data_date]['cash_and_cash_equivalents_end'] = cash_and_cash_equivalents_end
            stock_financial_metric_dict[data_date]['cash_and_cash_equivalents_change'] = cash_and_cash_equivalents_change
            stock_financial_metric_dict[data_date]['purchase_fixed_assets'] = purchase_fixed_assets
            fcf = operating_cash_flow - purchase_fixed_assets
            stock_financial_metric_dict[data_date]['fcf'] = fcf

        ebitda_dict = {}
        stock_profit_sheet_by_report_em_df = ak.stock_profit_sheet_by_report_em(symbol=ticker)
        for index, row in stock_profit_sheet_by_report_em_df.iterrows():
            data_date = row['报告日']
            # 利息费用
            interest_expense = row['利息费用']
            # 利润总额
            profit_total = row['利润总额']
            ebitda = profit_total + interest_expense
            ebitda_dict[data_date] = ebitda

        stock_cash_flow_sheet_by_report_em_df = ak.stock_cash_flow_sheet_by_report_em(symbol=ticker)
        for index, row in stock_cash_flow_sheet_by_report_em_df.iterrows():
            data_date = row['报告日']
            # 固定资产和投资性房地产折旧
            depreciation_and_amortization = row['固定资产和投资性房地产折旧']
            # 无形资产摊销
            amortization = row['无形资产摊销']
            # 长期待摊费用摊销
            long_term_prepaid_expenses = row['长期待摊费用摊销']

            # EBITBD
            ebitda = ebitda_dict[data_date]
            ebitda_dict[data_date] = ebitda + depreciation_and_amortization + amortization + long_term_prepaid_expenses

        stock_financial_abstract_df = ak.stock_financial_abstract(symbol=ticker)
        for index, row in stock_financial_abstract_df.iterrows():
            data_date = row['报告日']
            # 基本每股收益
            basic_eps = row['基本每股收益']
            stock_financial_metric_dict[data_date]['basic_eps'] = basic_eps

            # 每股净资产
            stock_financial_metric_dict[data_date]['book_value'] = row['每股净资产']
            # 每股企业自由现金流量
            stock_financial_metric_dict[data_date]['fcff_per_share'] = row['每股企业自由现金流量']
            # 每股股东自由现金流量
            stock_financial_metric_dict[data_date]['fcfe_per_share'] = row['每股股东自由现金流量']


        financial_report_date_list.sort()  # 将报告日期列表按时间升序排序
        stock_financial_analysis_indicator_df = ak.stock_financial_analysis_indicator(symbol=ticker, start_year=financial_report_date_list[0].year)
        for index, row in stock_financial_analysis_indicator_df.iterrows():
            data_date = row['日期']
            stock_financial_metric_dict[data_date]['dividend_payout_ratio'] = row['股息发放率(%)']
            stock_financial_metric_dict[data_date]['ebitda'] = ebitda_dict[data_date]
        return stock_financial_metric_dict, financial_report_date_list  


    def get_stock_A_value_em(self, ticker: str):
        stock_value_em_df = ak.stock_value_em(symbol=ticker)
        value_em_list = []

        for index, row in stock_value_em_df.iterrows():
            value_em = {}
            value_date = row['数据日期']
            data_date = value_date.replace('-', '')
            closing_price = row['当日收盘价']
            market_cap = row['总市值']
            flow_market_cap = row['流通市值']
            total_share = row['总股本']
            float_share = row['流通股本']
            pe_ttm_ratio = row['PE(TTM)']
            pe_static_ratio = row['PE(静)']
            pb_ratio = row['市净率']
            peg_ratio = row['PEG值']
            ps_ratio = row['市销率']
            pc_ratio = row['市现率']
            value_em['data_date'] = data_date
            value_em['closing_price'] = closing_price
            value_em['market_cap'] = market_cap
            value_em['flow_market_cap'] = flow_market_cap
            value_em['total_share'] = total_share
            value_em['float_share'] = float_share
            value_em['pe_ttm_ratio'] = pe_ttm_ratio
            value_em['pe_static_ratio'] = pe_static_ratio
            value_em['pb_ratio'] = pb_ratio
            value_em['peg_ratio'] = peg_ratio
            value_em['ps_ratio'] = ps_ratio
            value_em['pc_ratio'] = pc_ratio
            value_em_list.append(value_em)
        return value_em_list

    def get_A_key_indicators(self, ticker: str, indicator:str):

        stock_financial_abstract_ths_df = ak.stock_financial_abstract_ths(symbol=ticker, indicator=indicator)


