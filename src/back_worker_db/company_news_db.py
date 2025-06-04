from src.back_worker_db.database import get_db_connection
from src.data.models import CompanyNews

class CompanyNewsDB:
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

    def insert_company_news(self, news: CompanyNews, ticker: str):
        """插入单条公司新闻数据"""
        with self.conn.cursor() as cur:
            cur.execute("""
                INSERT INTO tb_company_news (
                    ticker, publish_time, title, content, source, url
                ) VALUES (
                    %s, %s, %s, %s, %s, %s
                )
            """, (
                ticker, news.publish_time, news.title, news.content,
                news.source, news.url
            ))
            self.conn.commit()


    def get_company_news(self, ticker: str, start_date: str = None, end_date: str = None) -> list[CompanyNews]:
        """查询公司新闻数据"""
        with self.conn.cursor() as cur:
            if start_date and end_date:
                cur.execute("""
                    SELECT publish_time, title, content, source, url
                    FROM tb_company_news
                    WHERE ticker = %s AND publish_time BETWEEN %s AND %s
                    ORDER BY publish_time DESC
                """, (ticker, start_date, end_date))
            else:
                cur.execute("""
                    SELECT publish_time, title, content, source, url
                    FROM tb_company_news
                    WHERE ticker = %s
                    ORDER BY publish_time DESC
                """, (ticker,))
                
            news_list = []
            for row in cur.fetchall():
                news_list.append(CompanyNews(
                    publish_time=row[0],
                    title=row[1],
                    content=row[2], 
                    source=row[3],
                    url=row[4]
                ))
            return news_list


    def delete_company_news(self, ticker: str, start_date: str = None, end_date: str = None):
        """删除公司新闻数据"""
        with self.conn.cursor() as cur:
            if start_date and end_date:
                cur.execute("""
                    DELETE FROM tb_company_news
                    WHERE ticker = %s AND publish_time BETWEEN %s AND %s
                """, (ticker, start_date, end_date))
            else:
                cur.execute("DELETE FROM tb_company_news WHERE ticker = %s", (ticker,))
            self.conn.commit()


    def update_company_news(self, news: CompanyNews, ticker: str):
        """更新单条公司新闻数据"""
        with self.conn.cursor() as cur:
            cur.execute("""
                UPDATE tb_company_news
                SET title = %s, content = %s, source = %s, url = %s
                WHERE ticker = %s AND publish_time = %s
            """, (
                news.title,
                news.content,
                news.source,
                news.url,
                ticker,
                news.publish_time
            ))
            self.conn.commit()