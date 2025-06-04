from src.back_worker_db.database import get_db_connection
from src.data.models import CompanyFacts

class CompanyFactsDB:
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

    def insert_company_facts(self, facts: CompanyFacts, ticker: str):
        """插入单条公司事实数据"""
        with self.conn.cursor() as cur:
            cur.execute("""
                INSERT INTO tb_company_facts (
                    ticker, report_period, period, currency, 
                    facts_data
                ) VALUES (
                    %s, %s, %s, %s, %s
                )
            """, (
                ticker, facts.report_period, facts.period, 
                facts.currency, facts.facts_data
            ))
            self.conn.commit()


    def get_company_facts(self, ticker: str, start_date: str = None, end_date: str = None) -> list[CompanyFacts]:
        """查询公司事实数据"""
        with self.conn.cursor() as cur:
            if start_date and end_date:
                cur.execute("""
                    SELECT report_period, period, currency, facts_data
                    FROM tb_company_facts
                    WHERE ticker = %s AND report_period BETWEEN %s AND %s
                    ORDER BY report_period
                """, (ticker, start_date, end_date))
            else:
                cur.execute("""
                    SELECT report_period, period, currency, facts_data
                    FROM tb_company_facts
                    WHERE ticker = %s
                    ORDER BY report_period
                """, (ticker,))
            
            facts_list = []
            for row in cur.fetchall():
                facts_list.append(CompanyFacts(
                    report_period=row[0],
                    period=row[1],
                    currency=row[2],
                    facts_data=row[3]
                ))
            return facts_list


    def delete_company_facts(self, ticker: str, start_date: str = None, end_date: str = None):
        """删除公司事实数据"""
        with self.conn.cursor() as cur:
            if start_date and end_date:
                cur.execute("""
                    DELETE FROM tb_company_facts
                    WHERE ticker = %s AND report_period BETWEEN %s AND %s
                """, (ticker, start_date, end_date))
            else:
                cur.execute("DELETE FROM tb_company_facts WHERE ticker = %s", (ticker,))
            self.conn.commit()  

    def update_company_facts(self, facts: CompanyFacts, ticker: str):
        """更新单条公司事实数据"""
        with self.conn.cursor() as cur:
            cur.execute("""
                UPDATE tb_company_facts
                SET period = %s, currency = %s, facts_data = %s
                WHERE ticker = %s AND report_period = %s
            """, (
                facts.period,
                facts.currency,
                facts.facts_data,
                ticker,
                facts.report_period
            ))
            self.conn.commit()

