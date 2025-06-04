from src.back_worker_db.database import get_db_connection
from src.data.models import LineItem

class LineItemDB:
    def __init__(self, host: str, user: str, password: str, database: str):
        """初始化财务明细项数据库连接"""
        self.conn = get_db_connection(host, user, password, database)
    def __del__(self):
        """关闭数据库连接"""
        if hasattr(self, 'conn'):
            self.conn.close()

    def insert_line_item(self, line_item: LineItem, ticker: str):
        """插入单条财务明细项数据"""
        
        with self.conn.cursor() as cur:
        try:
            cur.execute("""
                INSERT INTO tb_line_item (
                    ticker, report_period, period, currency, search_result
                ) VALUES (
                    %s, %s, %s, %s, %s
                )
            """, (
                ticker, line_item.report_period, line_item.period,
                line_item.currency, line_item.search_result
            ))
            self.conn.commit()


    def get_line_items(self, ticker: str, start_date: str = None, end_date: str = None) -> list[LineItem]:
        """查询财务明细项数据"""
        with self.conn.cursor() as cur:
            if start_date and end_date:
                cur.execute("""
                    SELECT report_period, period, currency, search_result
                    FROM tb_line_item
                    WHERE ticker = %s AND report_period BETWEEN %s AND %s
                    ORDER BY report_period DESC
                """, (ticker, start_date, end_date))
            else:
                cur.execute("""
                    SELECT report_period, period, currency, search_result
                    FROM tb_line_item 
                    WHERE ticker = %s
                    ORDER BY report_period DESC
                """, (ticker,))

            line_items = []
            for row in cur.fetchall():
                line_items.append(LineItem(
                    report_period=row[0],
                    period=row[1], 
                    currency=row[2],
                    search_result=row[3]
                ))
            return line_items


    def delete_line_items(self, ticker: str, start_date: str = None, end_date: str = None):
        """删除财务明细项数据"""
        with self.conn.cursor() as cur:
            if start_date and end_date:
                cur.execute("""
                    DELETE FROM tb_line_item
                    WHERE ticker = %s AND report_period BETWEEN %s AND %s
                """, (ticker, start_date, end_date))
            else:
                cur.execute("DELETE FROM tb_line_item WHERE ticker = %s", (ticker,))
            self.conn.commit()


    def update_line_item(self, line_item: LineItem, ticker: str):
        """更新单条财务明细项数据"""
        with self.conn.cursor() as cur:
            cur.execute("""
                UPDATE tb_line_item
                SET period = %s, currency = %s, search_result = %s
                WHERE ticker = %s AND report_period = %s
            """, (
                line_item.period,
                line_item.currency,
                line_item.search_result,
                ticker,
                line_item.report_period
            ))
            self.conn.commit()
