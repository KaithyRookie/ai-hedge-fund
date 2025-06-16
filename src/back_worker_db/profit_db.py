import psycopg2
from typing import Optional
from pydantic import BaseModel
class ProfitData(BaseModel):
    id: int
    ticker: Optional[str]
    report_date: Optional[str]
    total_operating_revenue: Optional[float] # 营业总收入
    operating_revenue: Optional[float] #营业收入
    interest_income: Optional[float]  # '利息收入'
    earned_premium: Optional[float]  # '已赚保费'
    commission_income: Optional[float]  # '手续费及佣金收入'
    real_estate_sales_revenue: Optional[float]  # '房地产销售收入'
    other_business_revenue: Optional[float]  # '其他业务收入'
    total_operating_cost: Optional[float]  # '营业总成本'
    operating_cost: Optional[float]  # '营业成本'
    commission_expense: Optional[float]  # '手续费及佣金支出'
    real_estate_sales_cost: Optional[float]  # '房地产销售成本'
    surrender_value: Optional[float]  # '退保金'
    net_compensation_expense: Optional[float]  # '赔付支出净额'
    net_insurance_contract_reserves: Optional[float]  # '提取保险合同准备金净额'
    policy_dividend_expense: Optional[float]  # '保单红利支出'
    reinsurance_expense: Optional[float]  # '分保费用'
    other_business_cost: Optional[float]  # '其他业务成本'
    business_tax_and_surcharge: Optional[float]  # '营业税金及附加'
    rd_expense: Optional[float]  # '研发费用'
    sales_expense: Optional[float]  # '销售费用'
    management_expense: Optional[float]  # '管理费用'
    financial_expense: Optional[float]  # '财务费用'
    interest_expense: Optional[float]  # '利息费用'
    interest_expenditure: Optional[float]  # '利息支出'
    investment_income: Optional[float]  # '投资收益'
    investment_income_associates: Optional[float]  # '对联营企业和合营企业的投资收益'
    financial_asset_termination_income: Optional[float]  # '以摊余成本计量的金融资产终止确认产生的收益'
    exchange_gain: Optional[float]  # '汇兑收益'
    net_exposure_hedge_income: Optional[float]  # '净敞口套期收益'
    fair_value_change_income: Optional[float]  # '公允价值变动收益'
    futures_profit_loss: Optional[float]  # '期货损益'
    custody_income: Optional[float]  # '托管收益'
    subsidy_income: Optional[float]  # '补贴收入'
    other_income: Optional[float]  # '其他收益'
    asset_impairment_loss: Optional[float]  # '资产减值损失'
    credit_impairment_loss: Optional[float]  # '信用减值损失'
    other_business_profit: Optional[float]  # '其他业务利润'
    asset_disposal_income: Optional[float]  # '资产处置收益'
    operating_profit: Optional[float]  # '营业利润'
    non_operating_income: Optional[float]  # '营业外收入'
    non_current_asset_disposal_gain: Optional[float]  # '非流动资产处置利得'
    non_operating_expense: Optional[float]  # '营业外支出'
    non_current_asset_disposal_loss: Optional[float]  # '非流动资产处置损失'
    total_profit: Optional[float]  # '利润总额'
    income_tax_expense: Optional[float]  # '所得税费用'
    unrecognized_investment_loss: Optional[float]  # '未确认投资损失'
    net_profit: Optional[float]  # '净利润'
    continuing_operation_net_profit: Optional[float]  # '持续经营净利润'
    discontinued_operation_net_profit: Optional[float]  # '终止经营净利润'
    net_profit_parent_company: Optional[float]  # '归属于母公司所有者的净利润'
    merged_party_net_profit: Optional[float]  # '被合并方在合并前实现净利润'
    minority_profit_loss: Optional[float]  # '少数股东损益'
    other_comprehensive_income: Optional[float]  # '其他综合收益'
    other_comprehensive_income_parent: Optional[float]  # '归属于母公司所有者的其他综合收益'
    non_reclassifiable_comprehensive_income: Optional[float]  # '以后不能重分类进损益的其他综合收益'
    benefit_plan_change: Optional[float]  # '重新计量设定受益计划变动额'
    equity_method_non_reclassifiable: Optional[float]  # '权益法下不能转损益的其他综合收益'
    equity_instrument_fair_value_change: Optional[float]  # '其他权益工具投资公允价值变动'
    own_credit_risk_fair_value_change: Optional[float]  # '企业自身信用风险公允价值变动'
    reclassifiable_comprehensive_income: Optional[float]  # '以后将重分类进损益的其他综合收益'
    equity_method_reclassifiable: Optional[float]  # '权益法下可转损益的其他综合收益'
    available_for_sale_fair_value_change: Optional[float]  # '可供出售金融资产公允价值变动损益'
    debt_investment_fair_value_change: Optional[float]  # '其他债权投资公允价值变动'
    financial_asset_reclassification: Optional[float]  # '金融资产重分类计入其他综合收益的金额'
    debt_investment_credit_impairment: Optional[float]  # '其他债权投资信用减值准备'
    held_to_maturity_reclassification: Optional[float]  # '持有至到期投资重分类为可供出售金融资产损益'
    cash_flow_hedge_reserve: Optional[float]  # '现金流量套期储备'
    cash_flow_hedge_effective_portion: Optional[float]  # '现金流量套期损益的有效部分'
    foreign_currency_translation: Optional[float]  # '外币财务报表折算差额'
    other_items: Optional[float]  # '其他'
    minority_other_comprehensive_income: Optional[float]  # '归属于少数股东的其他综合收益'
    total_comprehensive_income: Optional[float]  # '综合收益总额'
    total_comprehensive_income_parent: Optional[float]  # '归属于母公司所有者的综合收益总额'
    minority_comprehensive_income: Optional[float]  # '归属于少数股东的综合收益总额'
    basic_eps: Optional[float]  # '基本每股收益'
    diluted_eps: Optional[float]  # '稀释每股收益'
    data_source: Optional[str] # '数据源'
    is_audited: Optional[str]  # '是否审计'
    announcement_date: Optional[str] # '公告日期'
    currency: Optional[str] # '币种'
    report_type: Optional[str] # '类型'
    update_date: Optional[str] # '更新日期'
    created_at: Optional[str]
    updated_at: Optional[str]
    is_deleted: bool

class ProfitDB:
    def __init__(self, conn: psycopg2.connect):
        self.conn = conn
    
    def __del__(self):
        """析构函数，关闭数据库连接"""
        if hasattr(self, 'conn'):
            self.conn.close()

    def insert_profit(self, data: ProfitData):
        """插入单条利润表数据"""
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

        with self.conn.cursor() as cur:
            cur.execute(f"""
                INSERT INTO tb_profit_sina ({columns_str})
                VALUES ({placeholders})
            """, values)
            self.conn.commit()
            
    def get_latest_profit_report_date(self, ticker: str) -> str:
        """获取最新利润表的报告期"""
        with self.conn.cursor() as cur:
            cur.execute("""
                SELECT report_date
                FROM tb_profit_sina
                WHERE ticker = %s
                ORDER BY report_date DESC
                LIMIT 1
            """, (ticker,))
            result = cur.fetchone()
            return result[0] if result else None

    def get_profit(self, ticker: str, start_date: str = None, end_date: str = None) -> list[ProfitData]:
        """查询利润表数据"""
        params = ['ticker = %s ']
        values = [ticker]
        if start_date:
            params.append('report_date >= %s')
            values.append(start_date)
        if end_date:
            params.append('report_date <= %s')
            values.append(end_date)
        params_str = ' AND '.join(params)
        sql = f"""
            SELECT *
            FROM tb_profit_sina
            WHERE {params_str}
            ORDER BY id desc
        """
        with self.conn.cursor() as cur:
            cur.execute(sql, values)
            data_list = []
            for row in cur.fetchall():
                data = ProfitData()
                for key, value in row.items():
                    if value is None:
                        continue  # 跳过None值，避免TypeError: Object of type NoneType is not JSON serializable
                    if key == 'created_at' or key == 'update_at':
                        value = datetime.strptime(value, '%Y-%m-%d %H:%M:%S')
                    setattr(data, key, value)
                data_list.append(data)
            return data_list

    def delete_profit(self, ticker: str, start_date: str = None, end_date: str = None):
        """删除利润表数据"""
        with self.conn.cursor() as cur:
            if start_date and end_date:
                cur.execute("""
                    DELETE FROM tb_profit_sina
                    WHERE ticker = %s AND report_date BETWEEN %s AND %s
                """, (ticker, start_date, end_date))
            else:
                cur.execute("DELETE FROM tb_profit_sina WHERE ticker = %s", (ticker,))
            self.conn.commit()

    def update_profit(self, ticker: str, report_period, **kwargs):
        """更新单条利润表数据"""
        set_clause = ', '.join([f"{key} = %s" for key in kwargs.keys()])
        values = list(kwargs.values()) + [ticker, report_period]

        with self.conn.cursor() as cur:
            cur.execute(f"""
                UPDATE tb_profit_sina
                SET {set_clause}
                WHERE ticker = %s AND report_date = %s
            """, values)
            self.conn.commit()
