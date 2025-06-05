import psycopg2
from pydantic import BaseModel
    
class ProfitData(BaseModel):
    ticker: str
    report_period: str
    total_operating_revenue: float  | None | None
    operating_revenue: float  | None
    interest_income: float  | None  # '利息收入'
    earned_premium: float  | None  # '已赚保费'
    commission_income: float  | None  # '手续费及佣金收入'
    real_estate_sales_revenue: float  | None  # '房地产销售收入'
    other_business_revenue: float  | None  # '其他业务收入'
    total_operating_cost: float  | None  # '营业总成本'
    operating_cost: float  | None  # '营业成本'
    commission_expense: float  | None  # '手续费及佣金支出'
    real_estate_sales_cost: float  | None  # '房地产销售成本'
    surrender_value: float  | None  # '退保金'
    net_compensation_expense: float  | None  # '赔付支出净额'
    net_insurance_contract_reserves: float  | None  # '提取保险合同准备金净额'
    policy_dividend_expense: float  | None  # '保单红利支出'
    reinsurance_expense: float  | None  # '分保费用'
    other_business_cost: float  | None  # '其他业务成本'
    business_tax_and_surcharge: float  | None  # '营业税金及附加'
    rd_expense: float  | None  # '研发费用'
    sales_expense: float  | None  # '销售费用'
    management_expense: float  | None  # '管理费用'
    financial_expense: float  | None  # '财务费用'
    interest_expense: float  | None  # '利息费用'
    interest_expenditure: float  | None  # '利息支出'
    investment_income: float  | None  # '投资收益'
    investment_income_associates: float  | None  # '对联营企业和合营企业的投资收益'
    financial_asset_termination_income: float  | None  # '以摊余成本计量的金融资产终止确认产生的收益'
    exchange_gain: float  | None  # '汇兑收益'
    net_exposure_hedge_income: float  | None  # '净敞口套期收益'
    fair_value_change_income: float  | None  # '公允价值变动收益'
    futures_profit_loss: float  | None  # '期货损益'
    custody_income: float  | None  # '托管收益'
    subsidy_income: float  | None  # '补贴收入'
    other_income: float  | None  # '其他收益'
    asset_impairment_loss: float  | None  # '资产减值损失'
    credit_impairment_loss: float  | None  # '信用减值损失'
    other_business_profit: float  | None  # '其他业务利润'
    asset_disposal_income: float  | None  # '资产处置收益'
    operating_profit: float  | None  # '营业利润'
    non_operating_income: float  | None  # '营业外收入'
    non_current_asset_disposal_gain: float  | None  # '非流动资产处置利得'
    non_operating_expense: float  | None  # '营业外支出'
    non_current_asset_disposal_loss: float  | None  # '非流动资产处置损失'
    total_profit: float  | None  # '利润总额'
    income_tax_expense: float  | None  # '所得税费用'
    unrecognized_investment_loss: float  | None  # '未确认投资损失'
    net_profit: float  | None  # '净利润'
    continuing_operation_net_profit: float  | None  # '持续经营净利润'
    discontinued_operation_net_profit: float  | None  # '终止经营净利润'
    net_profit_parent_company: float  | None  # '归属于母公司所有者的净利润'
    merged_party_net_profit: float  | None  # '被合并方在合并前实现净利润'
    minority_profit_loss: float  | None  # '少数股东损益'
    other_comprehensive_income: float  | None  # '其他综合收益'
    other_comprehensive_income_parent: float  | None  # '归属于母公司所有者的其他综合收益'
    non_reclassifiable_comprehensive_income: float  | None  # '以后不能重分类进损益的其他综合收益'
    benefit_plan_change: float  | None  # '重新计量设定受益计划变动额'
    equity_method_non_reclassifiable: float  | None  # '权益法下不能转损益的其他综合收益'
    equity_instrument_fair_value_change: float  | None  # '其他权益工具投资公允价值变动'
    own_credit_risk_fair_value_change: float  | None  # '企业自身信用风险公允价值变动'
    reclassifiable_comprehensive_income: float  | None  # '以后将重分类进损益的其他综合收益'
    equity_method_reclassifiable: float  | None  # '权益法下可转损益的其他综合收益'
    available_for_sale_fair_value_change: float  | None  # '可供出售金融资产公允价值变动损益'
    debt_investment_fair_value_change: float  | None  # '其他债权投资公允价值变动'
    financial_asset_reclassification: float  | None  # '金融资产重分类计入其他综合收益的金额'
    debt_investment_credit_impairment: float  | None  # '其他债权投资信用减值准备'
    held_to_maturity_reclassification: float  | None  # '持有至到期投资重分类为可供出售金融资产损益'
    cash_flow_hedge_reserve: float  | None  # '现金流量套期储备'
    cash_flow_hedge_effective_portion: float  | None  # '现金流量套期损益的有效部分'
    foreign_currency_translation: float  | None  # '外币财务报表折算差额'
    other_items: float  | None  # '其他'
    minority_other_comprehensive_income: float  | None  # '归属于少数股东的其他综合收益'
    total_comprehensive_income: float  | None  # '综合收益总额'
    total_comprehensive_income_parent: float  | None  # '归属于母公司所有者的综合收益总额'
    minority_comprehensive_income: float  | None  # '归属于少数股东的综合收益总额'
    basic_eps: float  | None  # '基本每股收益'
    diluted_eps: float  | None  # '稀释每股收益'
    data_source: str  # '数据源'
    is_audited: str  # '是否审计'
    announcement_date: str  # '公告日期'
    currency: str  # '币种'
    report_type: str  # '类型'
    update_date: str  # '更新日期'

class ProfitDB:
    def __init__(self, host: str, user: str, password: str, database: str):
        """初始化数据库连接"""
        self.conn = psycopg2.connect(
            host=host,
            user=user,
            password=password,
            database=database
        )
    
    def __del__(self):
        """析构函数，关闭数据库连接"""
        if hasattr(self, 'conn'):
            self.conn.close()

    def insert_profit(self, ticker: str, report_period, **kwargs):
        """插入单条利润表数据"""
        columns = ', '.join(['ticker', 'report_period'] + list(kwargs.keys()))
        placeholders = ', '.join(['%s'] * (len(kwargs) + 2))
        values = [ticker, report_period] + list(kwargs.values())

        with self.conn.cursor() as cur:
            cur.execute(f"""
                INSERT INTO tb_profit ({columns})
                VALUES ({placeholders})
            """, values)
            self.conn.commit()

    def get_profit(self, ticker: str, start_date: str = None, end_date: str = None) -> list:
        """查询利润表数据"""
        with self.conn.cursor() as cur:
            if start_date and end_date:
                cur.execute("""
                    SELECT *
                    FROM tb_profit
                    WHERE ticker = %s AND report_period BETWEEN %s AND %s
                    ORDER BY report_period
                """, (ticker, start_date, end_date))
            else:
                cur.execute("""
                    SELECT *
                    FROM tb_profit
                    WHERE ticker = %s
                    ORDER BY report_period
                """, (ticker,))
            
            return cur.fetchall()

    def delete_profit(self, ticker: str, start_date: str = None, end_date: str = None):
        """删除利润表数据"""
        with self.conn.cursor() as cur:
            if start_date and end_date:
                cur.execute("""
                    DELETE FROM tb_profit
                    WHERE ticker = %s AND report_period BETWEEN %s AND %s
                """, (ticker, start_date, end_date))
            else:
                cur.execute("DELETE FROM tb_profit WHERE ticker = %s", (ticker,))
            self.conn.commit()

    def update_profit(self, ticker: str, report_period, **kwargs):
        """更新单条利润表数据"""
        set_clause = ', '.join([f"{key} = %s" for key in kwargs.keys()])
        values = list(kwargs.values()) + [ticker, report_period]

        with self.conn.cursor() as cur:
            cur.execute(f"""
                UPDATE tb_profit
                SET {set_clause}
                WHERE ticker = %s AND report_period = %s
            """, values)
            self.conn.commit()
