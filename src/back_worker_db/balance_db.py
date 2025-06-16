import psycopg2
from psycopg2.extras import DictCursor
from typing import Optional
from pydantic import BaseModel
class BalanceSheetData(BaseModel):
    id: int = None
    ticker: str = None
    report_date: str = None
    current_assets: float = None
    monetary_funds: float = None
    # 资产类字段(按SQL表结构顺序)
    settlement_reserves: float = None
    lending_funds: float = None
    trading_financial_assets: float = None
    bought_sellback_financial_assets: float = None
    derivative_financial_assets: float = None
    notes_accounts_receivable: float = None
    notes_receivable: float = None
    accounts_receivable: float = None
    receivables_financing: float = None
    prepayments: float = None
    dividends_receivable: float = None
    interest_receivable: float = None
    insurance_receivables: float = None
    reinsurance_receivables: float = None
    reinsurance_contract_reserves_receivable: float = None
    export_tax_rebates_receivable: float = None
    subsidies_receivable: float = None
    deposits_receivable: float = None
    internal_receivables: float = None
    other_receivables: float = None
    other_receivables_total: float = None
    inventories: float = None
    assets_held_for_sale: float = None
    deferred_expenses: float = None
    pending_current_asset_gains_losses: float = None
    non_current_assets_due_within_one_year: float = None
    other_current_assets: float = None
    total_current_assets: float = None
    non_current_assets: float = None
    loans_and_advances: float = None
    debt_investments: float = None
    other_debt_investments: float = None
    financial_assets_fvoci: float = None
    financial_assets_amortized_cost: float = None
    available_for_sale_financial_assets: float = None
    long_term_equity_investments: float = None
    investment_properties: float = None
    long_term_receivables: float = None
    other_equity_instruments: float = None
    other_non_current_financial_assets: float = None
    other_long_term_investments: float = None
    fixed_assets_original_value: float = None
    accumulated_depreciation: float = None
    fixed_assets_net_value: float = None
    fixed_assets_impairment_provision: float = None
    construction_in_progress_total: float = None
    construction_in_progress: float = None
    construction_materials: float = None
    fixed_assets_net_amount: float = None
    fixed_assets_disposal: float = None
    fixed_assets_and_disposal_total: float = None
    productive_biological_assets: float = None
    public_welfare_biological_assets: float = None
    oil_and_gas_assets: float = None
    contract_assets: float = None
    right_of_use_assets: float = None
    intangible_assets: float = None
    development_expenditure: float = None
    goodwill: float = None
    long_term_prepaid_expenses: float = None
    equity_split_circulation_rights: float = None
    deferred_tax_assets: float = None
    other_non_current_assets: float = None
    total_non_current_assets: float = None
    total_assets: float = None
    # 负债类字段
    current_liabilities: float = None
    short_term_borrowings: float = None
    borrowings_from_central_bank: float = None
    deposits_from_banks_and_other_institutions: float = None
    borrowings_from_banks: float = None
    trading_financial_liabilities: float = None
    derivative_financial_liabilities: float = None
    notes_accounts_payable: float = None
    notes_payable: float = None
    accounts_payable: float = None
    advance_receipts: float = None
    contract_liabilities: float = None
    sold_buyback_financial_assets: float = None
    commission_and_brokerage_payable: float = None
    employee_benefits_payable: float = None
    taxes_payable: float = None
    interest_payable: float = None
    dividends_payable: float = None
    deposits_payable: float = None
    internal_payables: float = None
    other_payables: float = None
    other_payables_total: float = None
    other_taxes_payable: float = None
    guarantee_liability_compensation_provision: float = None
    reinsurance_payables: float = None
    insurance_contract_reserves: float = None
    securities_trading_agency_payable: float = None
    securities_underwriting_agency_payable: float = None
    international_settlement: float = None
    domestic_settlement: float = None
    accrued_expenses: float = None
    estimated_current_liabilities: float = None
    short_term_bonds_payable: float = None
    liabilities_held_for_sale: float = None
    deferred_income_within_one_year: float = None
    non_current_liabilities_due_within_one_year: float = None
    other_current_liabilities: float = None
    total_current_liabilities: float = None
    non_current_liabilities: float = None
    long_term_borrowings: float = None
    bonds_payable: float = None
    bonds_payable_preferred_shares: float = None
    bonds_payable_perpetual_bonds: float = None
    lease_liabilities: float = None
    long_term_employee_benefits_payable: float = None
    long_term_payables: float = None
    long_term_payables_total: float = None
    special_payables: float = None
    estimated_non_current_liabilities: float = None
    long_term_deferred_income: float = None
    deferred_tax_liabilities: float = None
    other_non_current_liabilities: float = None
    total_non_current_liabilities: float = None
    total_liabilities: float = None
    # 所有者权益类字段
    owners_equity: float = None
    paid_in_capital: float = None
    other_equity_instruments_equity: float = None
    preferred_shares_equity: float = None
    perpetual_bonds_equity: float = None
    capital_reserve: float = None
    treasury_stock: float = None
    other_comprehensive_income: float = None
    special_reserve: float = None
    surplus_reserve: float = None
    general_risk_provision: float = None
    undetermined_investment_losses: float = None
    retained_earnings: float = None
    proposed_cash_dividends: float = None
    foreign_currency_translation_differences: float = None
    total_equity_attributable_to_parent: float = None
    minority_interests: float = None
    total_owners_equity: float = None
    total_liabilities_and_owners_equity: float = None
    # 其他字段
    data_source: str = None
    is_audited: str = None
    announcement_date: str = None
    currency: str = None
    report_type: str = None
    update_date: str = None
    created_at: str = None
    updated_at: str = None
    is_deleted: bool


class BalanceDB:
    def __init__(self, conn: psycopg2.connect):
        self.conn = conn

    def __del__(self):
        if hasattr(self, 'conn'):
            self.conn.close()

    def get_latest_balance_report_date(self, ticker: str) -> str:
        """获取最新的资产负债表报告日期"""
        with self.conn.cursor() as cur:
            cur.execute("""
                SELECT report_date
                FROM tb_balance_sina
                WHERE ticker = %s
                ORDER BY report_date DESC
                LIMIT 1
            """, (ticker,)) 
            result = cur.fetchone()
            return result[0] if result else None

    def insert_balance_sheet(self, data: BalanceSheetData):
        """插入单条资产负债表数据"""
        with self.conn.cursor() as cur:
            columns = []
            values = []
            kwargs = data.model_dump(exclude={'id', 'created_at', 'update_at', 'is_deleted'})
            for key, value in kwargs.items():
                if value is None:
                    continue
                columns.append(key)
                values.append(value)
            columns_str = ', '.join(columns)
            placeholders = ', '.join(['%s'] * len(values))
            cur.execute(f"""
                INSERT INTO tb_balance_sina ({columns_str})
                VALUES ({placeholders})
            """, values)
            self.conn.commit()

    def get_balance_sheet(self, ticker: str, start_date: str=None,  end_date: str = None) -> list[BalanceSheetData]:
        """查询资产负债表数据"""
        params = ['ticker = %s']
        values = [ticker]
        if start_date is not None:
            params.append('report_date >= %s')
            values.append(start_date)

        if end_date is not None:
            params.append('report_date <= %s')
            values.append(end_date)
        params_str = ' AND '.join(params)
        sql = f"""
            SELECT *
            FROM tb_balance_sina
            WHERE {params_str}
            ORDER BY report_date DESC
        """
        with self.conn.cursor(cursor_factory=DictCursor) as cur:
            cur.execute(sql, values)
            data_list = []
            for row in cur.fetchall():
                data = BalanceSheetData()
                for key, value in row.items():
                    if value is None:
                        continue  # 跳过None值，避免TypeError: Object of type NoneType is not JSON serializable
                    if key == 'created_at' or key == 'update_at':
                        value = datetime.strptime(value, '%Y-%m-%d %H:%M:%S')
                    setattr(data, key, value)
                data_list.append(data)
            return data_list


    def delete_balance_sheet(self, ticker: str, start_date: str,  end_date: str = None):
        """删除资产负债表数据"""
        with self.conn.cursor() as cur:
            if start_date and end_date:
                cur.execute("""
                    DELETE FROM tb_balance_sina
                    WHERE ticker = %s AND report_period BETWEEN %s AND %s
                """, (ticker, start_date, end_date))
            else:
                cur.execute("DELETE FROM tb_balance_sina WHERE ticker = %s", (ticker,))
            self.conn.commit()
    def update_balance_by_dict(self, ticker: str, data_dict: dict):
        """根据字典更新资产负债表数据"""
        with self.conn.cursor() as cur:
            # 构建 SET 子句
            set_clause = ', '.join([f"{key} = %s" for key in data_dict.keys()])
            # 构建完整的 SQL 语句
            sql = f"""
                UPDATE tb_balance_sina
                SET {set_clause}
                WHERE ticker = %s """
            # 构建参数列表
            params = list(data_dict.values()) + [ticker]
            # 执行 SQL 语句
            cur.execute(sql, params)
            self.conn.commit()


