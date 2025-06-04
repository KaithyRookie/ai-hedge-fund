from typing import List
from src.data.models import Price
from src.back_worker_db.database import get_db_connection

class StockPriceDB:
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

    def insert_stock_prices(self, prices: List[Price], ticker: str, stock_type: StockType):
        """插入股票价格数据"""
        with self.conn.cursor() as cur:
            for price in prices:
                cur.execute("""
                    INSERT INTO tb_stock_price (ticker, stock_type, time, open, high, low, close, volume)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                    ON CONFLICT (ticker, stock_type, time) DO UPDATE SET
                        open = EXCLUDED.open,
                        high = EXCLUDED.high, 
                        low = EXCLUDED.low,
                        close = EXCLUDED.close,
                        volume = EXCLUDED.volume
                """, (
                    ticker,
                    stock_type,
                    price.time,
                    price.open,
                    price.high,
                    price.low,
                    price.close,
                    price.volume
                ))
            self.conn.commit()


    def get_stock_prices(self, ticker: str, start_date: str, end_date: str) -> List[Price]:
        """查询股票价格数据"""
        with self.conn.cursor() as cur:
            cur.execute("""
                SELECT time, open, high, low, close, volume
                FROM tb_stock_price 
                WHERE ticker = %s AND time BETWEEN %s AND %s
                ORDER BY time
            """, (ticker, start_date, end_date))
            
            prices = []
            for row in cur.fetchall():
                prices.append(Price(
                    time=row[0],
                    open=row[1],
                    high=row[2],
                    low=row[3],
                    close=row[4],
                    volume=row[5]
                ))
            return prices


    def delete_stock_prices(self, ticker: str, start_date: str = None, end_date: str = None):
        """删除股票价格数据"""
        with self.conn.cursor() as cur:
            if start_date and end_date:
                cur.execute("""
                    DELETE FROM tb_stock_price 
                    WHERE ticker = %s AND time BETWEEN %s AND %s
                """, (ticker, start_date, end_date))
            else:
                cur.execute("DELETE FROM tb_stock_price WHERE ticker = %s", (ticker,))
            self.conn.commit()


    def update_stock_price(self, price: Price, ticker: str):
        """更新单条股票价格数据"""
        with self.conn.cursor() as cur:
            cur.execute("""
                UPDATE tb_stock_price 
                SET open = %s, high = %s, low = %s, close = %s, volume = %s
                WHERE ticker = %s AND time = %s
            """, (
                price.open,
                price.high,
                price.low,
                price.close,
                price.volume,
                ticker,
                price.time
            ))
            self.conn.commit()
    
    def get_latest_stock_price_by_ticker(self, ticker: str, stock_type: StockType) -> Price:
        """获取最近一天的价格数据"""
        with self.conn.cursor() as cur:
            cur.execute("""
                SELECT time, open, high, low, close, volume
                FROM tb_stock_price 
                WHERE ticker = %s AND stock_type = %s
                ORDER BY id DESC
                LIMIT 1
            """, (ticker, stock_type))
            row = cur.fetchone()
            if row:
                return Price(
                    time=row[0],
                    open=row[1],
                    high=row[2],
                    low=row[3],
                    close=row[4],
                    volume=row[5]
                )
            else:
                return None

