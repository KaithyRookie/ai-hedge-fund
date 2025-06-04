import psycopg2
from typing import Optional, List
from datetime import datetime

from enum import Enum

class StockType(Enum):
    """股票类型枚举"""
    A_SHARE = 'A'  # A股
    B_SHARE = 'B'  # B股
    STAR_MARKET = 'K'  # 科创板
    US_STOCK = 'U'  # 美股
    HK_STOCK = 'H'  # 港股

class StockDB:
    def __init__(self, host: str, user: str, password: str, database: str):
        """初始化股票数据库连接"""
        self.conn = psycopg2.connect(
            host=host,
            user=user,
            password=password,
            database=database
        )
    
    def __del__(self):
        """关闭数据库连接"""
        if hasattr(self, 'conn'):
            self.conn.close()
    
    def add_stock(self, ticker: str, name: str, stock_type: StockType) -> int:
        """添加股票到数据库"""
        with self.conn.cursor() as cur:
            cur.execute(
                "INSERT INTO tb_stock (ticker, name, stock_type) VALUES (%s, %s, %s) RETURNING id",
                (ticker, name, stock_type)
            )
            stock_id = cur.fetchone()[0]
            self.conn.commit()
            return stock_id
    
    def get_stock_by_id(self, stock_id: int, stock_type: StockType) -> Optional[dict]:
        """根据ID获取股票信息"""
        with self.conn.cursor() as cur:
            cur.execute(
                "SELECT id, ticker, name FROM tb_stock WHERE id = %s AND stock_type = %s AND is_deleted = FALSE",
                (stock_id, stock_type)
            )
            result = cur.fetchone()
            if result:
                return {
                    'id': result[0],
                    'ticker': result[1],
                    'name': result[2]
                }
            return None
    
    def get_stock_by_ticker(self, ticker: str, stock_type: StockType) -> Optional[dict]:
        """根据股票代码获取股票信息"""
        with self.conn.cursor() as cur:
            cur.execute(
                "SELECT id, ticker, name FROM tb_stock WHERE ticker = %s AND stock_type = %s AND is_deleted = FALSE",
                (ticker, stock_type)
            )
            result = cur.fetchone()
            if result:
                return {
                    'id': result[0],
                    'ticker': result[1],
                    'name': result[2]
                }
            return None
    
    def get_all_stocks(self, stock_type: StockType) -> List[dict]:
        """获取所有股票列表"""
        with self.conn.cursor() as cur:
            cur.execute(
                "SELECT id, ticker, name FROM tb_stock WHERE stock_type = %s AND is_deleted = FALSE",
                (stock_type,)
            )
            return [{
                'id': row[0],
                'ticker': row[1],
                'name': row[2]
            } for row in cur.fetchall()]
    
    def update_stock(self, stock_id: int, ticker: str = None, name: str = None, stock_type: StockType = None) -> bool:
        """更新股票信息"""
        updates = []
        params = []
        
        if ticker:
            updates.append("ticker = %s")
            params.append(ticker)
        if name:
            updates.append("name = %s")
            params.append(name)
        if stock_type:
            updates.append("stock_type = %s")
            params.append(stock_type)
        
        if not updates:
            return False
            
        params.append(stock_id)
        query = f"UPDATE tb_stock SET {', '.join(updates)} WHERE id = %s AND stock_type = %s AND is_deleted = FALSE"
        
        with self.conn.cursor() as cur:
            cur.execute(query, params)
            self.conn.commit()
            return cur.rowcount > 0
    
    def delete_stock(self, stock_id: int) -> bool:
        """软删除股票"""
        with self.conn.cursor() as cur:
            cur.execute(
                "UPDATE tb_stock SET is_deleted = TRUE WHERE id = %s",
                (stock_id,)
            )
            self.conn.commit()
            return cur.rowcount > 0
    
    def hard_delete_stock(self, stock_id: int) -> bool:
        """硬删除股票"""
        with self.conn.cursor() as cur:
            cur.execute(
                "DELETE FROM tb_stock WHERE id = %s",
                (stock_id,)
            )
            self.conn.commit()
            return cur.rowcount > 0
