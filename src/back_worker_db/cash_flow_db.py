import psycopg2
from typing import Optional
from datetime import datetime
from pydantic import BaseModel
class CashFlowData(BaseModel):
    id: Optional[int]
    ticker: Optional[str] # 股票代码
    report_date: Optional[str] # 报告日
    operating_cash_flow: Optional[float] # 经营活动产生的现金流量
    cash_from_sales: Optional[float] # 销售商品、提供劳务收到的现金
    net_increase_in_customer_deposits: Optional[float] # 客户存款和同业存放款项净增加额
    net_increase_in_central_bank_borrowing: Optional[float] # 向中央银行借款净增加额
    net_increase_in_interbank_borrowing: Optional[float] # 向其他金融机构拆入资金净增加额
    cash_from_insurance_premiums: Optional[float] #收到原保险合同保费取得的现金
    net_cash_from_reinsurance: Optional[float] # 收到再保险业务现金净额
    net_increase_in_policyholder_deposits: Optional[float] # 保户储金及投资款净增加额
    net_increase_in_trading_securities: Optional[float] # 处置交易性金融资产净增加额
    cash_from_interest_fees_commissions: Optional[float] #收取利息、手续费及佣金的现金
    net_increase_in_borrowed_funds: Optional[float] #拆入资金净增加额
    net_increase_in_repurchase_funds: Optional[float] #回购业务资金净增加额
    tax_refunds_received: Optional[float] #收到的税费返还
    other_operating_cash_inflows: Optional[float] #收到的其他与经营活动有关的现金
    total_operating_cash_inflows: Optional[float] # 经营活动现金流入小计
    cash_paid_for_goods_services: Optional[float] #购买商品、接受劳务支付的现金
    net_increase_in_customer_loans: Optional[float] #客户贷款及垫款净增加额
    net_increase_in_central_bank_deposits: Optional[float] #存放中央银行和同业款项净增加额
    cash_paid_for_insurance_claims: Optional[float] #支付原保险合同赔付款项的现金
    cash_paid_for_interest_fees_commissions: Optional[float] #支付利息、手续费及佣金的现金
    cash_paid_for_policy_dividends: Optional[float] # 支付保单红利的现金
    cash_paid_to_employees: Optional[float] # 支付给职工以及为职工支付的现金
    taxes_paid: Optional[float] #支付的各项税费
    other_operating_cash_outflows: Optional[float] #支付的其他与经营活动有关的现金
    total_operating_cash_outflows: Optional[float] #经营活动现金流出小计
    net_operating_cash_flow: Optional[float] #经营活动产生的现金流量净额
    investing_cash_flow: Optional[float] #投资活动产生的现金流量
    cash_from_investment_recovery: Optional[float] #收回投资所收到的现金
    cash_from_investment_returns: Optional[float] #取得投资收益收到的现金
    cash_from_asset_disposal: Optional[float] #处置固定资产、无形资产和其他长期资产所收回的现金净额
    cash_from_subsidiary_disposal: Optional[float] #处置子公司及其他营业单位收到的现金净额
    other_investing_cash_inflows: Optional[float] #收到的其他与投资活动有关的现金
    cash_from_reduced_deposits: Optional[float] #减少质押和定期存款所收到的现金
    net_increase_in_available_for_sale_securities: Optional[float] #处置可供出售金融资产净增加额
    total_investing_cash_inflows: Optional[float] #投资活动现金流入小计
    cash_paid_for_assets: Optional[float] #购建固定资产、无形资产和其他长期资产所支付的现金
    cash_paid_for_investments: Optional[float] #投资所支付的现金
    net_increase_in_pledged_loans: Optional[float] #质押贷款净增加额
    cash_paid_for_subsidiary_acquisition: Optional[float] #取得子公司及其他营业单位支付的现金净额
    cash_paid_for_increased_deposits: Optional[float] #增加质押和定期存款所支付的现金
    other_investing_cash_outflows: Optional[float] #支付的其他与投资活动有关的现金
    total_investing_cash_outflows: Optional[float] #投资活动现金流出小计
    net_investing_cash_flow: Optional[float] #投资活动产生的现金流量净额
    financing_cash_flow: Optional[float] #筹资活动产生的现金流量
    cash_from_equity_financing: Optional[float] #吸收投资收到的现金
    cash_from_minority_investment: Optional[float] #子公司吸收少数股东投资收到的现金
    cash_from_borrowing: Optional[float] #取得借款收到的现金
    cash_from_bond_issuance: Optional[float] #发行债券收到的现金
    other_financing_cash_inflows: Optional[float] #收到其他与筹资活动有关的现金
    total_financing_cash_inflows: Optional[float] #筹资活动现金流入小计
    cash_paid_for_debt_repayment: Optional[float]  #偿还债务支付的现金
    cash_paid_for_dividends_interest: Optional[float] #分配股利、利润或偿付利息所支付的现金
    cash_paid_to_minority_shareholders: Optional[float] #子公司支付给少数股东的股利、利润
    other_financing_cash_outflows: Optional[float] #支付其他与筹资活动有关的现金
    total_financing_cash_outflows: Optional[float] #筹资活动现金流出小计
    net_financing_cash_flow: Optional[float] #筹资活动产生的现金流量净额
    exchange_rate_effect: Optional[float] #汇率变动对现金及现金等价物的影响
    net_cash_increase: Optional[float] #现金及现金等价物净增加额
    beginning_cash_balance: Optional[float] #期初现金及现金等价物余额
    ending_cash_balance_cash: Optional[float] #现金的期末余额
    beginning_cash_balance_cash: Optional[float] #现金的期初余额
    ending_cash_equivalents_balance: Optional[float] #现金等价物的期末余额
    beginning_cash_equivalents_balance: Optional[float] #现金等价物的期初余额
    ending_total_cash_balance: Optional[float] #期末现金及现金等价物余额
    data_source: Optional[str] #数据源
    is_audited: Optional[str] #是否审计
    announcement_date: Optional[str] #公告日期
    currency: Optional[str] #币种
    report_type: Optional[str] #类型
    update_date: Optional[str] #更新日期
    created_at: Optional[datetime] 
    update_at: Optional[datetime]
    is_deleted: bool


class CashFlowDB:
    def __init__(self, conn: psycopg2.connect):
        self.conn = conn
    
    def __del__(self):
        """
        析构函数，关闭数据库连接
        """
        if hasattr(self, 'conn'):
            self.conn.close()

    def insert_cash_flow(self, data: CashFlowData):
        """
        插入单条现金流量表数据
        :param ticker: 股票代码
        :param report_date: 报告期
        :param kwargs: 其他现金流量表字段及对应值
        """
        ticker = data.ticker
        report_date = data.report_date
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
                INSERT INTO tb_cash_sina ({columns_str})
                VALUES ({placeholders})
            """, values)
            self.conn.commit()
    def get_latest_cash_flow_report_date(self, ticker: str) -> str:
        """
        获取最新现金流量表的报告期
        :param ticker: 股票代码
        :return: 最新报告期，如果没有数据则返回None
        """
        with self.conn.cursor() as cur:
            cur.execute("""
                SELECT report_date
                FROM tb_cash_sina
                WHERE ticker = %s
                ORDER BY report_date DESC
                LIMIT 1
            """, (ticker,))
            result = cur.fetchone()
            if result:
                return result[0]
            else:
                return None
    def get_cash_flow(self, ticker: str, start_date: str = None, end_date: str = None) -> list[CashFlowData]:
        """
        查询现金流量表数据
        :param ticker: 股票代码
        :param start_date: 开始日期
        :param end_date: 结束日期
        :return: 现金流量表数据列表
        """
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
            FROM tb_cash_sina
            WHERE {params_str}
            ORDER BY id ASC
        """
        with self.conn.cursor() as cur:
            cur.execute(sql, values)
            data_list = []
            for row in cur.fetchall():
                data = CashFlowData.model_construct()
                for key, value in row.items():
                    if value is None:
                        continue  # 跳过None值，避免TypeError: Object of type NoneType is not JSON serializable
                    if key == 'created_at' or key == 'update_at':
                        value = datetime.strptime(value, '%Y-%m-%d %H:%M:%S')
                    setattr(data, key, value)
                data_list.append(data)
            return data_list
    def delete_cash_flow(self, ticker: str, start_date: str = None, end_date: str = None):
        """
        删除现金流量表数据
        :param ticker: 股票代码
        :param start_date: 开始日期
        :param end_date: 结束日期
        """
        with self.conn.cursor() as cur:
            if start_date and end_date:
                cur.execute("""
                    DELETE FROM tb_cash_sina
                    WHERE ticker = %s AND report_date BETWEEN %s AND %s
                """, (ticker, start_date, end_date))
            else:
                cur.execute("DELETE FROM tb_cash_sina WHERE ticker = %s", (ticker,))
            self.conn.commit()

    def update_cash_flow(self, ticker: str, report_date: str, **kwargs):
        """
        更新单条现金流量表数据
        :param ticker: 股票代码
        :param report_date: 报告期
        :param kwargs: 要更新的字段及对应值
        """
        if not kwargs:
            return
        
        set_clauses = ', '.join([f"{key} = %s" for key in kwargs.keys()])
        values = list(kwargs.values()) + [ticker, report_date]
        
        with self.conn.cursor() as cur:
            cur.execute(f"""
                UPDATE tb_cash_sina
                SET {set_clauses}
                WHERE ticker = %s AND report_date = %s
            """, values)
            self.conn.commit()
