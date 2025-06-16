import psycopg2
from typing import Optional, List
from datetime import datetime
from enum import Enum
from pydantic import BaseModel
from typing import Optional
from psycopg2.extras import RealDictCursor

class StockData(BaseModel):
    id: Optional[int] = None  # 序号
    serial_number: Optional[int] = None  # 序号
    ticker: str = None  # 代码
    ticker_name: str = None  # 名称
    stock_type: str = None  # 类型
    created_at: datetime = None
    updated_at: datetime = None
    is_deleted: bool


class StockType(Enum):
    """股票类型枚举"""
    A_SHARE = 'A'  # A股
    B_SHARE = 'B'  # B股
    STAR_MARKET = 'K'  # 科创板
    US_STOCK = 'U'  # 美股
    HK_STOCK = 'H'  # 港股

    def to_string(self):
        return self.value

class StockDB:
    def __init__(self, conn: psycopg2.connect):
        self.conn = conn

    def get_cursor(self, commit: bool = True):
        """获取数据库游标的上下文管理器"""
        cursor = self.get_cursor(cursor_factory=RealDictCursor)
        try:
            yield cursor
            if commit:
                self.conn.commit()
        except Exception as e:
            self.conn.rollback()
            logging.error(f"Database operation failed: {e}")
            raise
        finally:
            cursor.close()
    
    def _convert_record_to_model(self, record) -> StockData:
        """将数据库记录转换为 StockData 模型"""
        if not record:
            return None
        return StockData(**record)

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

        with self.get_cursor() as cur:
            try:
                cur.execute(
                    f"INSERT INTO tb_stock ({columns_str}) VALUES ({placeholders}) RETURNING id",
                    tuple(values)
                )
            except psycopg2.errors.UniqueViolation as e:
                logging.warning(f"Duplicate data found for ticker {data.ticker} and stock_type {data.stock_type}. Skipping insertion.")
                raise e
            except Exception as e:
                logging.error(f"Error inserting data: {e}")
                raise e
    
    def check_stock_exists(self, ticker: str, stock_type: StockType) -> bool:
        """检查股票是否存在"""
        with self.get_cursor(False) as cur:
            try:
                cur.execute(
                    "SELECT 1 FROM tb_stock WHERE ticker = %s AND stock_type = %s AND is_deleted = FALSE",
                    (ticker, stock_type.to_string())
                )
                return cur.fetchone() is not None
            except Exception as e:
                logging.error(f"Error checking stock existence: {e}")
                raise e

    def get_stock_by_id(self, stock_id: int, stock_type: StockType) -> Optional[StockData]:
        """根据ID获取股票信息"""
        with self.get_cursor(False) as cur:
            try:
                cur.execute(
                    "SELECT * FROM tb_stock WHERE id = %s AND stock_type = %s AND is_deleted = FALSE",
                    (stock_id, stock_type.to_string())
                )
                result = cur.fetchone()
                if result:
                    return self._convert_record_to_model(result)
                return None
            except Exception as e:
                logging.error(f"Error fetching stock by ID: {e}")
                raise e

    def get_stock_by_ticker_name(self, ticker_name: str) -> Optional[StockData]:
        with self.get_cursor(False) as cur:
            try:
                cur.execute(
                    "SELECT * FROM tb_stock WHERE ticker_name = %s AND is_deleted = FALSE",
                    (ticker_name, )
                )
                result = cur.fetchone()
                # 将 result 转换为 StockData 实例
                if result:
                    return self._convert_record_to_model(result)  
                return None
            except Exception as e:
                logging.error(f"Error fetching stock by ticker_name: {e}")
                raise e

    def get_stock_by_ticker(self, ticker: str, stock_type: StockType) -> Optional[StockData]:
        """根据股票代码获取股票信息"""
        with self.get_cursor(False) as cur:
            try:
                cur.execute(
                    "SELECT * FROM tb_stock WHERE ticker = %s AND stock_type = %s AND is_deleted = FALSE",
                    (ticker, stock_type.to_string())
                )
                result = cur.fetchone()
                if result:
                    return self._convert_record_to_model(result)
                return None
            except Exception as e:
                logging.error(f"Error fetching stock by ticker: {e}")
                raise e

    def get_all_stocks(self, stock_type: StockType) -> List[StockData]:
        """获取所有股票列表"""
        with self.get_cursor(False) as cur:
            try:
                cur.execute(
                    "SELECT * FROM tb_stock WHERE stock_type = %s AND is_deleted = FALSE",
                    (stock_type.to_string(),)
                )
                results = cur.fetchall()
                data_list = []
                for row in results:
                    data = self._convert_record_to_model(row)
                    data_list.append(data)
                return data_list
            except Exception as e:
                logging.error(f"Error fetching all stocks: {e}")
                raise e


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
            params.append(stock_type.to_string())

        if not updates:
            return False

        params.append(stock_id)
        query = f"UPDATE tb_stock SET {', '.join(updates)} WHERE id = %s AND stock_type = %s AND is_deleted = FALSE"

        with self.get_cursor() as cur:
            try:
                cur.execute(query, params)
                return cur.rowcount > 0
            except Exception as e:
                logging.error(f"Error updating stock: {e}")
                raise e

    def delete_stock(self, stock_id: int) -> bool:
        """软删除股票"""
        with self.get_cursor() as cur:
            try:
                cur.execute(
                    "UPDATE tb_stock SET is_deleted = TRUE WHERE id = %s",
                    (stock_id,)
                )
                return cur.rowcount > 0
            except Exception as e:
                logging.error(f"Error deleting stock: {e}")
                raise e

    def hard_delete_stock(self, stock_id: int) -> bool:
        """硬删除股票"""
        with self.get_cursor() as cur:
            try:
                cur.execute(
                    "DELETE FROM tb_stock WHERE id = %s",
                    (stock_id,)
                )
                return cur.rowcount > 0
            except Exception as e:
                logging.error(f"Error hard deleting stock: {e}")
                raise e
