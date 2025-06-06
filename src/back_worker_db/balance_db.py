import psycopg2
from pydantic import BaseModel
from psycopg2.extras import DictCursor

class BalanceSheetData(BaseModel):
    id: int
    ticker: str
    report_date: str
    current_assets: float | None
    monetary_funds: float | None
    # 资产类字段(按SQL表结构顺序)
    settlement_reserves: float | None
    lending_funds: float | None
    trading_financial_assets: float | None
    bought_sellback_financial_assets: float | None
    derivative_financial_assets: float | None
    notes_accounts_receivable: float | None
    notes_receivable: float | None
    accounts_receivable: float | None
    receivables_financing: float | None
    prepayments: float | None
    dividends_receivable: float | None
    interest_receivable: float | None
    insurance_receivables: float | None
    reinsurance_receivables: float | None
    reinsurance_contract_reserves_receivable: float | None
    export_tax_rebates_receivable: float | None
    subsidies_receivable: float | None
    deposits_receivable: float | None
    internal_receivables: float | None
    other_receivables: float | None
    other_receivables_total: float | None
    inventories: float | None
    assets_held_for_sale: float | None
    deferred_expenses: float | None
    pending_current_asset_gains_losses: float | None
    non_current_assets_due_within_one_year: float | None
    other_current_assets: float | None
    total_current_assets: float | None
    non_current_assets: float | None
    loans_and_advances: float | None
    debt_investments: float | None
    other_debt_investments: float | None
    financial_assets_fvoci: float | None
    financial_assets_amortized_cost: float | None
    available_for_sale_financial_assets: float | None
    long_term_equity_investments: float | None
    investment_properties: float | None
    long_term_receivables: float | None
    other_equity_instruments: float | None
    other_non_current_financial_assets: float | None
    other_long_term_investments: float | None
    fixed_assets_original_value: float | None
    accumulated_depreciation: float | None
    fixed_assets_net_value: float | None
    fixed_assets_impairment_provision: float | None
    construction_in_progress_total: float | None
    construction_in_progress: float | None
    construction_materials: float | None
    fixed_assets_net_amount: float | None
    fixed_assets_disposal: float | None
    fixed_assets_and_disposal_total: float | None
    productive_biological_assets: float | None
    public_welfare_biological_assets: float | None
    oil_and_gas_assets: float | None
    contract_assets: float | None
    right_of_use_assets: float | None
    intangible_assets: float | None
    development_expenditure: float | None
    goodwill: float | None
    long_term_prepaid_expenses: float | None
    equity_split_circulation_rights: float | None
    deferred_tax_assets: float | None
    other_non_current_assets: float | None
    total_non_current_assets: float | None
    total_assets: float | None
    # 负债类字段
    current_liabilities: float | None
    short_term_borrowings: float | None
    borrowings_from_central_bank: float | None
    deposits_from_banks_and_other_institutions: float | None
    borrowings_from_banks: float | None
    trading_financial_liabilities: float | None
    derivative_financial_liabilities: float | None
    notes_accounts_payable: float | None
    notes_payable: float | None
    accounts_payable: float | None
    advance_receipts: float | None
    contract_liabilities: float | None
    sold_buyback_financial_assets: float | None
    commission_and_brokerage_payable: float | None
    employee_benefits_payable: float | None
    taxes_payable: float | None
    interest_payable: float | None
    dividends_payable: float | None
    deposits_payable: float | None
    internal_payables: float | None
    other_payables: float | None
    other_payables_total: float | None
    other_taxes_payable: float | None
    guarantee_liability_compensation_provision: float | None
    reinsurance_payables: float | None
    insurance_contract_reserves: float | None
    securities_trading_agency_payable: float | None
    securities_underwriting_agency_payable: float | None
    international_settlement: float | None
    domestic_settlement: float | None
    accrued_expenses: float | None
    estimated_current_liabilities: float | None
    short_term_bonds_payable: float | None
    liabilities_held_for_sale: float | None
    deferred_income_within_one_year: float | None
    non_current_liabilities_due_within_one_year: float | None
    other_current_liabilities: float | None
    total_current_liabilities: float | None
    non_current_liabilities: float | None
    long_term_borrowings: float | None
    bonds_payable: float | None
    bonds_payable_preferred_shares: float | None
    bonds_payable_perpetual_bonds: float | None
    lease_liabilities: float | None
    long_term_employee_benefits_payable: float | None
    long_term_payables: float | None
    long_term_payables_total: float | None
    special_payables: float | None
    estimated_non_current_liabilities: float | None
    long_term_deferred_income: float | None
    deferred_tax_liabilities: float | None
    other_non_current_liabilities: float | None
    total_non_current_liabilities: float | None
    total_liabilities: float | None
    # 所有者权益类字段
    owners_equity: float | None
    paid_in_capital: float | None
    other_equity_instruments_equity: float | None
    preferred_shares_equity: float | None
    perpetual_bonds_equity: float | None
    capital_reserve: float | None
    treasury_stock: float | None
    other_comprehensive_income: float | None
    special_reserve: float | None
    surplus_reserve: float | None
    general_risk_provision: float | None
    undetermined_investment_losses: float | None
    retained_earnings: float | None
    proposed_cash_dividends: float | None
    foreign_currency_translation_differences: float | None
    total_equity_attributable_to_parent: float | None
    minority_interests: float | None
    total_owners_equity: float | None
    total_liabilities_and_owners_equity: float | None
    # 其他字段
    data_source: str
    is_audited: str
    announcement_date: str
    currency: str
    report_type: str
    update_date: str
    created_at: str
    updated_at: str
    is_deleted: bool


class BalanceDB:
    def __init__(self, host: str, user: str, password: str, database: str):
        self.conn = psycopg2.connect(
            host=host,
            user=user,
            password=password,
            database=database
        )

    def __del__(self):
        if hasattr(self, 'conn'):
            self.conn.close()

    def get_latest_balance_report_date(self, ticker: str) -> str | None:
        """获取最新的资产负债表报告日期"""
        with self.conn.cursor() as cur:
            cur.execute("""
                SELECT report_date
                FROM tb_balance_sina
                WHERE ticker = %s
                ORDER BY id DESC
                LIMIT 1
            """, (ticker,)) 
            result = cur.fetchone()
            return result[0] if result else None

    def insert_balance_sheet(self, ticker: str, data: BalanceSheetData):
        """插入单条资产负债表数据"""
        with self.conn.cursor() as cur:
            cur.execute(f"""
                INSERT INTO tb_balance_sina (
                ticker, report_date, current_assets, monetary_funds, settlement_reserves, lending_funds, trading_financial_assets, bought_sellback_financial_assets, 
                derivative_financial_assets, notes_accounts_receivable, notes_receivable, accounts_receivable, receivables_financing, prepayments, dividends_receivable, 
                interest_receivable, insurance_receivables, reinsurance_receivables, reinsurance_contract_reserves_receivable, export_tax_rebates_receivable, subsidies_receivable, 
                deposits_receivable, internal_receivables, other_receivables, other_receivables_total, inventories, assets_held_for_sale, deferred_expenses, pending_current_asset_gains_losses, 
                non_current_assets_due_within_one_year, other_current_assets, total_current_assets, non_current_assets, loans_and_advances, debt_investments, other_debt_investments, 
                financial_assets_fvoci, financial_assets_amortized_cost, available_for_sale_financial_assets, long_term_equity_investments, investment_properties, long_term_receivables, 
                other_equity_instruments, other_non_current_financial_assets, other_long_term_investments, fixed_assets_original_value, accumulated_depreciation, fixed_assets_net_value, 
                fixed_assets_impairment_provision, construction_in_progress_total, construction_in_progress, construction_materials, fixed_assets_net_amount, fixed_assets_disposal, 
                fixed_assets_and_disposal_total, productive_biological_assets, public_welfare_biological_assets, oil_and_gas_assets, contract_assets, right_of_use_assets, intangible_assets, 
                development_expenditure, goodwill, long_term_prepaid_expenses, equity_split_circulation_rights, deferred_tax_assets, other_non_current_assets, total_non_current_assets, total_assets, 
                current_liabilities, short_term_borrowings, borrowings_from_central_bank, deposits_from_banks_and_other_institutions, borrowings_from_banks, trading_financial_liabilities, 
                derivative_financial_liabilities, notes_accounts_payable, notes_payable, accounts_payable, advance_receipts, contract_liabilities, sold_buyback_financial_assets, 
                commission_and_brokerage_payable, employee_benefits_payable, taxes_payable, interest_payable, dividends_payable, deposits_payable, internal_payables, other_payables, 
                other_payables_total, other_taxes_payable, guarantee_liability_compensation_provision, reinsurance_payables, insurance_contract_reserves, securities_trading_agency_payable, 
                securities_underwriting_agency_payable, international_settlement, domestic_settlement, accrued_expenses, estimated_current_liabilities, short_term_bonds_payable, 
                liabilities_held_for_sale, deferred_income_within_one_year, non_current_liabilities_due_within_one_year, other_current_liabilities, total_current_liabilities, non_current_liabilities, 
                long_term_borrowings, bonds_payable, bonds_payable_preferred_shares, bonds_payable_perpetual_bonds, lease_liabilities, long_term_employee_benefits_payable, long_term_payables, 
                long_term_payables_total, special_payables, estimated_non_current_liabilities, long_term_deferred_income, deferred_tax_liabilities, other_non_current_liabilities, 
                total_non_current_liabilities, total_liabilities, owners_equity, paid_in_capital, other_equity_instruments_equity, preferred_shares_equity, perpetual_bonds_equity, capital_reserve, 
                treasury_stock, other_comprehensive_income, special_reserve, surplus_reserve, general_risk_provision, undetermined_investment_losses, retained_earnings, proposed_cash_dividends, 
                foreign_currency_translation_differences, total_equity_attributable_to_parent, minority_interests, total_owners_equity, total_liabilities_and_owners_equity, data_source, is_audited, 
                announcement_date, currency, report_type, update_date
                   
                ) VALUES (
                    {ticker}, {data.report_date}, {data.current_assets}, {data.monetary_funds}, {data.settlement_reserves}, {data.lending_funds}, {data.trading_financial_assets}, {data.bought_sellback_financial_assets},
                    {data.derivative_financial_assets}, {data.notes_accounts_receivable}, {data.notes_receivable}, {data.accounts_receivable}, {data.receivables_financing}, {data.prepayments}, {data.dividends_receivable},
                    {data.interest_receivable}, {data.insurance_receivables}, {data.reinsurance_receivables}, {data.reinsurance_contract_reserves_receivable}, {data.export_tax_rebates_receivable}, {data.subsidies_receivable},
                    {data.deposits_receivable}, {data.internal_receivables}, {data.other_receivables}, {data.other_receivables_total}, {data.inventories}, {data.assets_held_for_sale}, {data.deferred_expenses}, {data.pending_current_asset_gains_losses},
                    {data.non_current_assets_due_within_one_year}, {data.other_current_assets}, {data.total_current_assets}, {data.non_current_assets}, {data.loans_and_advances}, {data.debt_investments}, {data.other_debt_investments},
                    {data.financial_assets_fvoci}, {data.financial_assets_amortized_cost}, {data.available_for_sale_financial_assets}, {data.long_term_equity_investments}, {data.investment_properties}, {data.long_term_receivables},
                    {data.other_equity_instruments}, {data.other_non_current_financial_assets}, {data.other_long_term_investments}, {data.fixed_assets_original_value}, {data.accumulated_depreciation}, {data.fixed_assets_net_value},
                    {data.fixed_assets_impairment_provision}, {data.construction_in_progress_total}, {data.construction_in_progress}, {data.construction_materials}, {data.fixed_assets_net_amount}, {data.fixed_assets_disposal},
                    {data.fixed_assets_and_disposal_total}, {data.productive_biological_assets}, {data.public_welfare_biological_assets}, {data.oil_and_gas_assets}, {data.contract_assets}, {data.right_of_use_assets}, {data.intangible_assets},
                    {data.development_expenditure}, {data.goodwill}, {data.long_term_prepaid_expenses}, {data.equity_split_circulation_rights}, {data.deferred_tax_assets}, {data.other_non_current_assets}, {data.total_non_current_assets}, {data.total_assets},
                    {data.current_liabilities}, {data.short_term_borrowings}, {data.borrowings_from_central_bank}, {data.deposits_from_banks_and_other_institutions}, {data.borrowings_from_banks}, {data.trading_financial_liabilities},
                    {data.derivative_financial_liabilities}, {data.notes_accounts_payable}, {data.notes_payable}, {data.accounts_payable}, {data.advance_receipts}, {data.contract_liabilities}, {data.sold_buyback_financial_assets},
                    {data.commission_and_brokerage_payable}, {data.employee_benefits_payable}, {data.taxes_payable}, {data.interest_payable}, {data.dividends_payable}, {data.deposits_payable}, {data.internal_payables}, {data.other_payables},
                    {data.other_payables_total}, {data.other_taxes_payable}, {data.guarantee_liability_compensation_provision}, {data.reinsurance_payables}, {data.insurance_contract_reserves}, {data.securities_trading_agency_payable},
                    {data.securities_underwriting_agency_payable}, {data.international_settlement}, {data.domestic_settlement}, {data.accrued_expenses}, {data.estimated_current_liabilities}, {data.short_term_bonds_payable},
                    {data.liabilities_held_for_sale}, {data.deferred_income_within_one_year}, {data.non_current_liabilities_due_within_one_year}, {data.other_current_liabilities}, {data.total_current_liabilities}, {data.non_current_liabilities},
                    {data.long_term_borrowings}, {data.bonds_payable}, {data.bonds_payable_preferred_shares}, {data.bonds_payable_perpetual_bonds}, {data.lease_liabilities}, {data.long_term_employee_benefits_payable}, {data.long_term_payables},
                    {data.long_term_payables_total}, {data.special_payables}, {data.estimated_non_current_liabilities}, {data.long_term_deferred_income}, {data.deferred_tax_liabilities}, {data.other_non_current_liabilities},
                    {data.total_non_current_liabilities}, {data.total_liabilities}, {data.owners_equity}, {data.paid_in_capital}, {data.other_equity_instruments_equity}, {data.preferred_shares_equity}, {data.perpetual_bonds_equity}, {data.capital_reserve},
                    {data.treasury_stock}, {data.other_comprehensive_income}, {data.special_reserve}, {data.surplus_reserve}, {data.general_risk_provision}, {data.undetermined_investment_losses}, {data.retained_earnings}, {data.proposed_cash_dividends},
                    {data.foreign_currency_translation_differences}, {data.total_equity_attributable_to_parent}, {data.minority_interests}, {data.total_owners_equity}, {data.total_liabilities_and_owners_equity}, {data.data_source}, {data.is_audited},
                    {data.announcement_date}, {data.currency}, {data.report_type}, {data.update_date}
                )
            """)
            self.conn.commit()

    def get_balance_sheet(self, ticker: str, start_date: str,  end_date: str = None) -> list[BalanceSheetData]:
        """查询资产负债表数据"""
        with self.conn.cursor(cursor_factory=DictCursor) as cur:
            if start_date and end_date:
                cur.execute("""
                    SELECT id, ticker, report_date, current_assets, monetary_funds, settlement_reserves, lending_funds, trading_financial_assets, bought_sellback_financial_assets, derivative_financial_assets, notes_accounts_receivable, notes_receivable, accounts_receivable, receivables_financing, prepayments, dividends_receivable, interest_receivable, insurance_receivables, reinsurance_receivables, reinsurance_contract_reserves_receivable, export_tax_rebates_receivable, subsidies_receivable, deposits_receivable, internal_receivables, other_receivables, other_receivables_total, inventories, assets_held_for_sale, deferred_expenses, pending_current_asset_gains_losses, non_current_assets_due_within_one_year, other_current_assets, total_current_assets, non_current_assets, loans_and_advances, debt_investments, other_debt_investments, financial_assets_fvoci, financial_assets_amortized_cost, available_for_sale_financial_assets, long_term_equity_investments, investment_properties, long_term_receivables, other_equity_instruments, other_non_current_financial_assets, other_long_term_investments, fixed_assets_original_value, accumulated_depreciation, fixed_assets_net_value, fixed_assets_impairment_provision, construction_in_progress_total, construction_in_progress, construction_materials, fixed_assets_net_amount, fixed_assets_disposal, fixed_assets_and_disposal_total, productive_biological_assets, public_welfare_biological_assets, oil_and_gas_assets, contract_assets, right_of_use_assets, intangible_assets, development_expenditure, goodwill, long_term_prepaid_expenses, equity_split_circulation_rights, deferred_tax_assets, other_non_current_assets, total_non_current_assets, total_assets, current_liabilities, short_term_borrowings, borrowings_from_central_bank, deposits_from_banks_and_other_institutions, borrowings_from_banks, trading_financial_liabilities, derivative_financial_liabilities, notes_accounts_payable, notes_payable, accounts_payable, advance_receipts, contract_liabilities, sold_buyback_financial_assets, commission_and_brokerage_payable, employee_benefits_payable, taxes_payable, interest_payable, dividends_payable, deposits_payable, internal_payables, other_payables, other_payables_total, other_taxes_payable, guarantee_liability_compensation_provision, reinsurance_payables, insurance_contract_reserves, securities_trading_agency_payable, securities_underwriting_agency_payable, international_settlement, domestic_settlement, accrued_expenses, estimated_current_liabilities, short_term_bonds_payable, liabilities_held_for_sale, deferred_income_within_one_year, non_current_liabilities_due_within_one_year, other_current_liabilities, total_current_liabilities, non_current_liabilities, long_term_borrowings, bonds_payable, bonds_payable_preferred_shares, bonds_payable_perpetual_bonds, lease_liabilities, long_term_employee_benefits_payable, long_term_payables, long_term_payables_total, special_payables, estimated_non_current_liabilities, long_term_deferred_income, deferred_tax_liabilities, other_non_current_liabilities, total_non_current_liabilities, total_liabilities, owners_equity, paid_in_capital, other_equity_instruments_equity, preferred_shares_equity, perpetual_bonds_equity, capital_reserve, treasury_stock, other_comprehensive_income, special_reserve, surplus_reserve, general_risk_provision, undetermined_investment_losses, retained_earnings, proposed_cash_dividends, foreign_currency_translation_differences, total_equity_attributable_to_parent, minority_interests, total_owners_equity, total_liabilities_and_owners_equity, data_source, is_audited, announcement_date, currency, report_type, update_date, created_at, update_at, is_deleted
                    FROM tb_balance_sheet
                    WHERE ticker = %s AND report_date BETWEEN %s AND %s
                    ORDER BY id DESC
                """, (ticker, start_date, end_date))
            else:
                cur.execute("""
                    SELECT id, ticker, report_date, current_assets, monetary_funds, settlement_reserves, lending_funds, trading_financial_assets, bought_sellback_financial_assets, derivative_financial_assets, notes_accounts_receivable, notes_receivable, accounts_receivable, receivables_financing, prepayments, dividends_receivable, interest_receivable, insurance_receivables, reinsurance_receivables, reinsurance_contract_reserves_receivable, export_tax_rebates_receivable, subsidies_receivable, deposits_receivable, internal_receivables, other_receivables, other_receivables_total, inventories, assets_held_for_sale, deferred_expenses, pending_current_asset_gains_losses, non_current_assets_due_within_one_year, other_current_assets, total_current_assets, non_current_assets, loans_and_advances, debt_investments, other_debt_investments, financial_assets_fvoci, financial_assets_amortized_cost, available_for_sale_financial_assets, long_term_equity_investments, investment_properties, long_term_receivables, other_equity_instruments, other_non_current_financial_assets, other_long_term_investments, fixed_assets_original_value, accumulated_depreciation, fixed_assets_net_value, fixed_assets_impairment_provision, construction_in_progress_total, construction_in_progress, construction_materials, fixed_assets_net_amount, fixed_assets_disposal, fixed_assets_and_disposal_total, productive_biological_assets, public_welfare_biological_assets, oil_and_gas_assets, contract_assets, right_of_use_assets, intangible_assets, development_expenditure, goodwill, long_term_prepaid_expenses, equity_split_circulation_rights, deferred_tax_assets, other_non_current_assets, total_non_current_assets, total_assets, current_liabilities, short_term_borrowings, borrowings_from_central_bank, deposits_from_banks_and_other_institutions, borrowings_from_banks, trading_financial_liabilities, derivative_financial_liabilities, notes_accounts_payable, notes_payable, accounts_payable, advance_receipts, contract_liabilities, sold_buyback_financial_assets, commission_and_brokerage_payable, employee_benefits_payable, taxes_payable, interest_payable, dividends_payable, deposits_payable, internal_payables, other_payables, other_payables_total, other_taxes_payable, guarantee_liability_compensation_provision, reinsurance_payables, insurance_contract_reserves, securities_trading_agency_payable, securities_underwriting_agency_payable, international_settlement, domestic_settlement, accrued_expenses, estimated_current_liabilities, short_term_bonds_payable, liabilities_held_for_sale, deferred_income_within_one_year, non_current_liabilities_due_within_one_year, other_current_liabilities, total_current_liabilities, non_current_liabilities, long_term_borrowings, bonds_payable, bonds_payable_preferred_shares, bonds_payable_perpetual_bonds, lease_liabilities, long_term_employee_benefits_payable, long_term_payables, long_term_payables_total, special_payables, estimated_non_current_liabilities, long_term_deferred_income, deferred_tax_liabilities, other_non_current_liabilities, total_non_current_liabilities, total_liabilities, owners_equity, paid_in_capital, other_equity_instruments_equity, preferred_shares_equity, perpetual_bonds_equity, capital_reserve, treasury_stock, other_comprehensive_income, special_reserve, surplus_reserve, general_risk_provision, undetermined_investment_losses, retained_earnings, proposed_cash_dividends, foreign_currency_translation_differences, total_equity_attributable_to_parent, minority_interests, total_owners_equity, total_liabilities_and_owners_equity, data_source, is_audited, announcement_date, currency, report_type, update_date, created_at, update_at, is_deleted
                    FROM tb_balance_sheet
                    WHERE ticker = %s
                    ORDER BY id DESC
                """, (ticker,))

            data_list = []
            for row in cur.fetchall():
                data = BalanceSheetData()
                for key, value in row.items():
                    setattr(data, key, value)
                data_list.append(data)
            return data_list

    def delete_balance_sheet(self, ticker: str, start_date: str,  end_date: str = None):
        """删除资产负债表数据"""
        with self.conn.cursor() as cur:
            if start_date and end_date:
                cur.execute("""
                    DELETE FROM tb_balance_sheet
                    WHERE ticker = %s AND report_period BETWEEN %s AND %s
                """, (ticker, start_date, end_date))
            else:
                cur.execute("DELETE FROM tb_balance_sheet WHERE ticker = %s", (ticker,))
            self.conn.commit()
    def update_balance_by_dict(self, ticker: str, data_dict: dict):
        """根据字典更新资产负债表数据"""
        with self.conn.cursor() as cur:
            # 构建 SET 子句
            set_clause = ', '.join([f"{key} = %s" for key in data_dict.keys()])
            # 构建完整的 SQL 语句
            sql = f"""
                UPDATE tb_balance_sheet
                SET {set_clause}
                WHERE ticker = %s """
            # 构建参数列表
            params = list(data_dict.values()) + [ticker]
            # 执行 SQL 语句
            cur.execute(sql, params)
            self.conn.commit()

   