import psycopg2
from typing import Optional, List
from datetime import datetime
from enum import Enum
from pydantic import BaseModel
from typing import Optional

class StockData(BaseModel):
    id: Optional[int] = None  # 序号
    serial_number: Optional[int] = None  # 序号
    ticker: str = None  # 代码
    ticker_name: str = None  # 名称
    stock_type: str = None  # 类型
    created_at: str = None
    updated_at: str = None
    is_deleted: bool


class StockType(Enum):
    """股票类型枚举"""
    A_SHARE = 'A'  # A股
    B_SHARE = 'B'  # B股
    STAR_MARKET = 'K'  # 科创板
    US_STOCK = 'U'  # 美股
    HK_STOCK = 'H'  # 港股

class StockDB:
    def __init__(self, conn: psycopg2.connect):
        self.conn = conn

    def __del__(self):
        """关闭数据库连接"""
        if hasattr(self, 'conn'):
            self.conn.close()

    def add_stock(self, data: StockData):
        """添加股票到数据库"""
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
            cur.execute(
                f"INSERT INTO tb_stock ({columns_str}) VALUES ({placeholders}) RETURNING id",
                tuple(values)
            )
            self.conn.commit()
    
    def check_stock_exists(self, ticker: str, stock_type: StockType) -> bool:
        """检查股票是否存在"""
        with self.conn.cursor() as cur:
            cur.execute(
                "SELECT 1 FROM tb_stock WHERE ticker = %s AND stock_type = %s AND is_deleted = FALSE",
                (ticker, stock_type)
            )
            return cur.fetchone() is not None

    def get_stock_by_id(self, stock_id: int, stock_type: StockType) -> Optional[StockData]:
        """根据ID获取股票信息"""
        with self.conn.cursor() as cur:
            cur.execute(
                "SELECT * FROM tb_stock WHERE id = %s AND stock_type = %s AND is_deleted = FALSE",
                (stock_id, stock_type)
            )
            result = cur.fetchone()
            if result:
                data = StockData.model_construct()
                for key, value in result.items():
                    if value is None:
                        continue  # 跳过None值，避免TypeError: Object of type NoneType is not JSON serializable
                    if key == 'created_at' or key == 'update_at':
                        value = datetime.strptime(value, '%Y-%m-%d %H:%M:%S')
                    setattr(data, key, value)
                return data
            return None

    def get_stock_by_ticker(self, ticker: str, stock_type: StockType) -> Optional[StockData]:
        """根据股票代码获取股票信息"""
        with self.conn.cursor() as cur:
            cur.execute(
                "SELECT * FROM tb_stock WHERE ticker = %s AND stock_type = %s AND is_deleted = FALSE",
                (ticker, stock_type)
            )
            result = cur.fetchone()
            if result:
                data = StockData.model_construct()
                for key, value in result.items():
                    if value is None:
                        continue  # 跳过None值，避免TypeError: Object of type NoneType is not JSON serializable
                    if key == 'created_at' or key == 'update_at':
                        value = datetime.strptime(value, '%Y-%m-%d %H:%M:%S')
                    setattr(data, key, value)
                return data
            return None

    def get_all_stocks(self, stock_type: StockType) -> List[StockData]:
        """获取所有股票列表"""
        with self.conn.cursor() as cur:
            cur.execute(
                "SELECT * FROM tb_stock WHERE stock_type = %s AND is_deleted = FALSE",
                (stock_type,)
            )
            results = cur.fetchall()
            data_list = []
            for row in results:
                data = StockData.model_construct()
                for key, value in row.items():
                    if key == 'created_at' or key == 'update_at':
                        value = datetime.strptime(value, '%Y-%m-%d %H:%M:%S')
                    setattr(data, key, value)
                data_list.append(data)
            return data_list

    def update_stock(self, stock_id: int, ticker: str = None, name: str = None, stock_type: StockType = None) -> bool:
        """更新股票信息"""
        updates = []
        params = []

        if ticker:
            updates.append("ticker = %s")
            params.append(ticker)
        if name:
            updates.append("ticker_name = %s")
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
