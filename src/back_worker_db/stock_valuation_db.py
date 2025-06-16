
from pydantic import BaseModel


class StockValuationData(BaseModel):
    id: int
    ticker: str
    data_date: str  
    closing_price: float | None
    daily_change: float | None
    market_cap: float | None
    flow_market_cap: float | None
    total_share: int | None
    float_share: int | None
    pe_ttm_ratio: float | None
    pe_static_ratio: float | None
    pb_ratio: float | None
    peg_ratio: float | None
    pc_ratio: float | None
    ps_ratio: float | None
    update_date: str = None
    created_at: str = None
    updated_at: str = None
    is_deleted: bool = False
    
class StockValuationDB:
    def __init__(self, conn):
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

    def add_stock_valuation(self, data: StockValuationData):
        """添加股票估值数据到数据库中"""
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
        sql = f"INSERT INTO stock_valuation ({columns_str}) VALUES ({placeholders})"
        with self.get_cursor() as cur:
            try:
                cur.execute(sql, values)
            except psycopg2.errors.UniqueViolation as e:
                logging.warning(f"Duplicate data found for ticker {data.ticker} and data_date {data.data_date}. Skipping insertion.")
                raise e
            except Exception as e:
                logging.error(f"Error inserting data: {e}")
                raise e
    def get_latest_stock_valuation_date(self, ticker: str):
        """获取最新的股票估值数据"""
        sql = "SELECT data_date FROM tb_stock_valuation WHERE ticker = %s ORDER BY data_date DESC LIMIT 1"
        with self.get_cursor(False) as cur:
            try:
                cur.execute(sql, (ticker,))
                result = cur.fetchone()
                if result:
                    return result[0]
                return None
            except Exception as e: 
                logging.error(f"Error fetching latest stock valuation date: {e}")
                raise e

    def query_stock_valuation(self, ticker: str, start_date:str=None, end_date: str = None) -> list[StockValuationData]:
        """
        查询股票估值数据
        :param ticker: 股票代码
        :param data_date: 数据日期，可选参数
        :return: 查询结果列表
        """
        params = ['ticker = %s']
        values = [ticker]
        if start_date:
            params.append('data_date >= %s')
            values.append(start_date)
        if end_date:
            params.append('data_date <= %s')
            values.append(end_date)
        sql = f"SELECT * FROM tb_stock_valuation WHERE {' AND '.join(params)}"
        
        with self.get_cursor(False) as cur:
            try:
                cur.execute(sql, values)
                data_list = []
                for row in cur.fetchall():
                    data_list.append(StockValuationData(**row))
                return data_list
            except Exception as e:
                logging.error(f"Error fetching data for ticker {ticker}: {e}")
                raise e

    def update_stock_valuation(self, ticker: str, data_date: str, update_data: dict):
        """
        更新股票估值数据
        :param ticker: 股票代码
        :param data_date: 数据日期
        :param update_data: 要更新的数据字典，键为字段名，值为新值
        """
        set_clause = ', '.join([f"{key} = %s" for key in update_data.keys()])
        values = list(update_data.values()) + [ticker, data_date]
        sql = f"UPDATE tb_stock_valuation SET {set_clause} WHERE ticker = %s AND data_date = %s"
        
        with self.get_cursor() as cur:
            try:
                cur.execute(sql, values)
            except Exception as e:
                logging.error(f"Error updating data for ticker {ticker} and data_date {data_date}: {e}")
                raise e

    def delete_stock_valuation(self, ticker: str, data_date: str = None):
        """
        删除股票估值数据
        :param ticker: 股票代码
        :param data_date: 数据日期，可选参数。若指定，则删除该日期的记录；若未指定，则删除该股票的所有记录
        """
        if data_date:
            sql = "DELETE FROM tb_stock_valuation WHERE ticker = %s AND data_date = %s"
            params = (ticker, data_date)
        else:
            sql = "DELETE FROM tb_stock_valuation WHERE ticker = %s"
            params = (ticker,)
        
        with self.get_cursor() as cur:
            try:
                cur.execute(sql, params)
            except Exception as e:
                logging.error(f"Error deleting data for ticker {ticker} and data_date {data_date}: {e}")
                raise e
