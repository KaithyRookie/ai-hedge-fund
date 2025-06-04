from src.back_worker_db.database import get_db_connection
from src.data.models import FinancialMetrics
import psycopg2

class FinancialMetricsDB:
    def __init__(self, host: str, user: str, password: str, database: str):
        self.conn = get_db_connection(host, user, password, database)

    def __del__(self):  
        if hasattr(self, 'conn'):
            self.conn.close()

    def insert_financial_metrics(self, metrics: FinancialMetrics, ticker: str):
        """插入单条财务指标数据"""
        with self.conn.cursor() as cur:
            cur.execute(f"""
                INSERT INTO tb_financial_metrics (
                    ticker, report_period, period, currency, market_cap, enterprise_value,
                    pe_ratio, pb_ratio, ps_ratio, enterprise_value_to_ebitda_ratio,
                    enterprise_value_to_revenue_ratio, free_cash_flow_yield, peg_ratio,
                    gross_margin, operating_margin, net_margin, return_on_equity,
                    return_on_assets, return_on_invested_capital, asset_turnover,
                    inventory_turnover, receivables_turnover, days_sales_outstanding,
                    operating_cycle, working_capital_turnover, current_ratio, quick_ratio,
                    cash_ratio, operating_cash_flow_ratio, debt_to_equity, debt_to_assets,
                    interest_coverage, revenue_growth, earnings_growth, book_value_growth,
                    earnings_per_share_growth, free_cash_flow_growth, operating_income_growth,
                    ebitda_growth, payout_ratio, earnings_per_share, book_value_per_share,
                    fcff_per_share, fcfe_per_share
                ) VALUES (
                   {ticker}, {metrics.report_period}, {metrics.period}, {metrics.currency},
                   {metrics.market_cap}, {metrics.enterprise_value}, {metrics.pe_ratio},
                   {metrics.pb_ratio}, {metrics.ps_ratio}, {metrics.enterprise_value_to_ebitda_ratio},
                   {metrics.enterprise_value_to_revenue_ratio}, {metrics.free_cash_flow_yield},
                   {metrics.peg_ratio}, {metrics.gross_margin}, {metrics.operating_margin},
                   {metrics.net_margin}, {metrics.return_on_equity}, {metrics.return_on_assets},
                   {metrics.return_on_invested_capital}, {metrics.asset_turnover},
                   {metrics.inventory_turnover}, {metrics.receivables_turnover},
                   {metrics.days_sales_outstanding}, {metrics.operating_cycle},
                   {metrics.working_capital_turnover}, {metrics.current_ratio},
                   {metrics.quick_ratio}, {metrics.cash_ratio}, {metrics.operating_cash_flow_ratio},
                   {metrics.debt_to_equity}, {metrics.debt_to_assets}, {metrics.interest_coverage},
                   {metrics.revenue_growth}, {metrics.earnings_growth}, {metrics.book_value_growth},
                   {metrics.earnings_per_share_growth}, {metrics.free_cash_flow_growth},
                   {metrics.operating_income_growth}, {metrics.ebitda_growth}, {metrics.payout_ratio},
                   {metrics.earnings_per_share}, {metrics.book_value_per_share},
                   {metrics.fcff_per_share}, {metrics.fcfe_per_share}
                )
            """)
            self.conn.commit()


    def get_financial_metrics(self, ticker: str, start_date: str = None, end_date: str = None) -> list[FinancialMetrics]:
        """查询财务指标数据"""
        with self.conn.cursor() as cur:
            if start_date and end_date:
                cur.execute("""
                    SELECT * FROM tb_financial_metrics 
                    WHERE ticker = %s AND report_period BETWEEN %s AND %s
                    ORDER BY report_period DESC
                """, (ticker, start_date, end_date))
            else:
                cur.execute("""
                    SELECT * FROM tb_financial_metrics 
                    WHERE ticker = %s
                    ORDER BY report_period DESC
                """, (ticker,))
            
            metrics = []
            for row in cur.fetchall():
                metrics.append(FinancialMetrics(
                    report_period=row[2],
                    period=row[3],
                    currency=row[4],
                    market_cap=row[5],
                    enterprise_value=row[6],
                    pe_ratio=row[7],
                    pb_ratio=row[8],
                    ps_ratio=row[9],
                    enterprise_value_to_ebitda_ratio=row[10],
                    enterprise_value_to_revenue_ratio=row[11],
                    free_cash_flow_yield=row[12],
                    peg_ratio=row[13],
                    gross_margin=row[14],
                    operating_margin=row[15],
                    net_margin=row[16],
                    return_on_equity=row[17],
                    return_on_assets=row[18],
                    return_on_invested_capital=row[19],
                    asset_turnover=row[20],
                    inventory_turnover=row[21],
                    receivables_turnover=row[22],
                    days_sales_outstanding=row[23],
                    operating_cycle=row[24],
                    working_capital_turnover=row[25],
                    current_ratio=row[26],
                    quick_ratio=row[27],
                    cash_ratio=row[28],
                    operating_cash_flow_ratio=row[29],
                    debt_to_equity=row[30],
                    debt_to_assets=row[31],
                    interest_coverage=row[32],
                    revenue_growth=row[33],
                    earnings_growth=row[34],
                    book_value_growth=row[35],
                    earnings_per_share_growth=row[36],
                    free_cash_flow_growth=row[37],
                    operating_income_growth=row[38],
                    ebitda_growth=row[39],
                    payout_ratio=row[40],
                    earnings_per_share=row[41],
                    book_value_per_share=row[42],
                    free_cash_flow_per_share=row[43]
                ))
            return metrics


    def delete_financial_metrics(self, ticker: str, start_date: str = None, end_date: str = None):
        """删除财务指标数据"""
        with self.conn.cursor() as cur:
            if start_date and end_date:
                cur.execute("""
                    DELETE FROM tb_financial_metrics 
                    WHERE ticker = %s AND report_period BETWEEN %s AND %s
                """, (ticker, start_date, end_date))
            else:
                cur.execute("DELETE FROM tb_financial_metrics WHERE ticker = %s", (ticker,))
            self.conn.commit()

    def update_financial_metrics(self, host: str, user: str, password: str, database: str, metrics: FinancialMetrics, ticker: str):
        """更新单条财务指标数据"""
        with self.conn.cursor() as cur:
            cur.execute("""
                UPDATE tb_financial_metrics 
                SET period = %s, currency = %s, market_cap = %s, enterprise_value = %s,
                    pe_ratio = %s, pb_ratio = %s, ps_ratio = %s,
                    enterprise_value_to_ebitda_ratio = %s,
                    enterprise_value_to_revenue_ratio = %s, free_cash_flow_yield = %s,
                    peg_ratio = %s, gross_margin = %s, operating_margin = %s,
                    net_margin = %s, return_on_equity = %s, return_on_assets = %s,
                    return_on_invested_capital = %s, asset_turnover = %s,
                    inventory_turnover = %s, receivables_turnover = %s,
                    days_sales_outstanding = %s, operating_cycle = %s,
                    working_capital_turnover = %s, current_ratio = %s,
                    quick_ratio = %s, cash_ratio = %s, operating_cash_flow_ratio = %s,
                    debt_to_equity = %s, debt_to_assets = %s, interest_coverage = %s,
                    revenue_growth = %s, earnings_growth = %s, book_value_growth = %s,
                    earnings_per_share_growth = %s, free_cash_flow_growth = %s,
                    operating_income_growth = %s, ebitda_growth = %s,
                    payout_ratio = %s, earnings_per_share = %s,
                    book_value_per_share = %s, free_cash_flow_per_share = %s
                WHERE ticker = %s AND report_period = %s
            """, (
                metrics.period, metrics.currency, metrics.market_cap,
                metrics.enterprise_value, metrics.pe_ratio, metrics.pb_ratio,
                metrics.ps_ratio, metrics.enterprise_value_to_ebitda_ratio,
                metrics.enterprise_value_to_revenue_ratio, metrics.free_cash_flow_yield,
                metrics.peg_ratio, metrics.gross_margin, metrics.operating_margin,
                metrics.net_margin, metrics.return_on_equity, metrics.return_on_assets,
                metrics.return_on_invested_capital, metrics.asset_turnover,
                metrics.inventory_turnover, metrics.receivables_turnover,
                metrics.days_sales_outstanding, metrics.operating_cycle,
                metrics.working_capital_turnover, metrics.current_ratio,
                metrics.quick_ratio, metrics.cash_ratio,
                metrics.operating_cash_flow_ratio, metrics.debt_to_equity,
                metrics.debt_to_assets, metrics.interest_coverage,
                metrics.revenue_growth, metrics.earnings_growth,
                metrics.book_value_growth, metrics.earnings_per_share_growth,
                metrics.free_cash_flow_growth, metrics.operating_income_growth,
                metrics.ebitda_growth, metrics.payout_ratio,
                metrics.earnings_per_share, metrics.book_value_per_share,
                metrics.free_cash_flow_per_share, ticker, metrics.report_period
            ))
            self.conn.commit()

