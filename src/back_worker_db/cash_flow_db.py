import psycopg2

class CashFlowDB:
    def __init__(self, host: str, user: str, password: str, database: str):
        """
        初始化数据库连接
        :param host: 数据库主机地址
        :param user: 数据库用户名
        :param password: 数据库密码
        :param database: 数据库名
        """
        self.conn = psycopg2.connect(
            host=host,
            user=user,
            password=password,
            database=database
        )
    
    def __del__(self):
        """
        析构函数，关闭数据库连接
        """
        if hasattr(self, 'conn'):
            self.conn.close()

    def insert_cash_flow(self, ticker: str, report_period: str, **kwargs):
        """
        插入单条现金流量表数据
        :param ticker: 股票代码
        :param report_period: 报告期
        :param kwargs: 其他现金流量表字段及对应值
        """
        columns = ['ticker', 'report_period']
        values = [ticker, report_period]
        for key, value in kwargs.items():
            columns.append(key)
            values.append(value)
        
        columns_str = ', '.join(columns)
        placeholders = ', '.join(['%s'] * len(values))
        
        with self.conn.cursor() as cur:
            cur.execute(f"""
                INSERT INTO tb_cash_flow ({columns_str})
                VALUES ({placeholders})
            """, values)
            self.conn.commit()

    def get_cash_flow(self, ticker: str, start_date: str = None, end_date: str = None) -> list:
        """
        查询现金流量表数据
        :param ticker: 股票代码
        :param start_date: 开始日期
        :param end_date: 结束日期
        :return: 现金流量表数据列表
        """
        with self.conn.cursor() as cur:
            if start_date and end_date:
                cur.execute("""
                    SELECT *
                    FROM tb_cash_flow
                    WHERE ticker = %s AND report_period BETWEEN %s AND %s
                    ORDER BY report_period
                """, (ticker, start_date, end_date))
            else:
                cur.execute("""
                    SELECT *
                    FROM tb_cash_flow
                    WHERE ticker = %s
                    ORDER BY report_period
                """, (ticker,))
            
            return cur.fetchall()

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
                    DELETE FROM tb_cash_flow
                    WHERE ticker = %s AND report_period BETWEEN %s AND %s
                """, (ticker, start_date, end_date))
            else:
                cur.execute("DELETE FROM tb_cash_flow WHERE ticker = %s", (ticker,))
            self.conn.commit()

    def update_cash_flow(self, ticker: str, report_period: str, **kwargs):
        """
        更新单条现金流量表数据
        :param ticker: 股票代码
        :param report_period: 报告期
        :param kwargs: 要更新的字段及对应值
        """
        if not kwargs:
            return
        
        set_clauses = ', '.join([f"{key} = %s" for key in kwargs.keys()])
        values = list(kwargs.values()) + [ticker, report_period]
        
        with self.conn.cursor() as cur:
            cur.execute(f"""
                UPDATE tb_cash_flow
                SET {set_clauses}
                WHERE ticker = %s AND report_period = %s
            """, values)
            self.conn.commit()
