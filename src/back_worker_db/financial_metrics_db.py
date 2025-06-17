import logging
from datetime import datetime
from src.data.models import FinancialMetrics
import psycopg2

from contextlib import contextmanager
from psycopg2.extras import RealDictCursor

class FinancialMetricsDB:
    def __init__(self, conn: psycopg2.connect):
        self.conn = conn

    def __del__(self):
        if hasattr(self, 'conn'):
            self.conn.close()
    @contextmanager
    def get_cursor(self, commit: bool = True):
        """获取数据库游标的上下文管理器"""
        cursor = self.conn.cursor(cursor_factory=RealDictCursor)
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

    def get_ticker_latest_report_period(self, ticker: str) -> str:
        """获取股票最新报告期"""
        with self.get_cursor(False) as cur:
            try:
                cur.execute("""
                    SELECT report_period FROM tb_financial_metric 
                    WHERE ticker = %s
                    ORDER BY report_period DESC
                    LIMIT 1
                """, [ticker])
                row = cur.fetchone()
                if row:
                    return row[0]
                else:
                    return None
            except Exception as e:
                logging.error(f"Error fetching latest report period for ticker {ticker}: {e}")
                raise e

    def insert_financial_metrics(self, data: FinancialMetrics):
        """插入单条财务指标数据"""
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
                cur.execute(f"""
                    INSERT INTO tb_financial_metric ({columns_str})
                    VALUES ({placeholders})
                """, values)
            except psycopg2.Error as e:
                logging.error(f"Failed to insert financial metrics: {e}")
                raise e

    def get_financial_metrics(self, ticker: str, start_date: str = None, end_date: str = None) -> list[FinancialMetrics]:
        """查询财务指标数据"""
        params = [' ticker = %s ']
        values = [ticker]
        if start_date:
            params.append("report_period >= %s")
            values.append(start_date)
        if end_date:
            params.append("report_period <= %s")
            values.append(end_date)
        params_str = ' AND '.join(params)
        with self.get_cursor() as cur:
            try:
                cur.execute(f"""
                    SELECT * FROM tb_financial_metric
                    WHERE {params_str}
                """, values)
                metrics = [FinancialMetrics(**row) for row in cur.fetchall()]
                return metrics
            except psycopg2.Error as e:
                logging.error(f"Failed to fetch financial metrics: {e}")
                raise e

    def delete_financial_metrics(self, ticker: str, start_date: str = None, end_date: str = None):
        """删除财务指标数据"""
        params = []
        values = [ticker]
        if start_date:
            params.append("report_period >= %s")
            values.append(start_date)
        if end_date:
            params.append("report_period <= %s")
            values.append(end_date)
        params_str = ' AND '.join(params)
        with self.get_cursor() as cur:
            try:
                cur.execute(f"""
                    DELETE FROM tb_financial_metric
                    WHERE {params_str}
                """, values)
            except psycopg2.Error as e:
                logging.error(f"Failed to delete financial metrics: {e}")
                raise e

    def _model_to_insert_data(self, model: FinancialMetrics) -> dict:
        """将 Pydantic 模型转换为插入数据"""
        data = model.model_dump(exclude={'id', 'created_at', 'updated_at', 'is_deleted'}, exclude_none=True)
        # 确保 report_period 存在
        if 'report_period' not in data or 'ticker' not in data:
            raise ValueError("report_period or ticker is required")
        
        return data

    def update_financial_metrics(self, record_id: int, data: FinancialMetrics):
        """更新单条财务指标数据"""
        update_data = self._model_to_insert_data(data)
        update_data['updated_at'] = datetime.now()
        # 构建 SET 子句
        set_clauses = []
        values = []
        for key, value in update_data.items():
            set_clauses.append(f"{key} = %s")
            values.append(value)
        set_clauses_str = ', '.join(set_clauses)
        with self.get_cursor() as cur:
            try:
                cur.execute(f"""
                    UPDATE tb_financial_metric
                    SET {set_clauses_str}
                    WHERE id = %s
                """, values + [record_id])  
                logging.info(f"Updated financial metrics record with ID: {record_id}")
            except psycopg2.Error as e:
                logging.error(f"Failed to update financial metrics record with ID {record_id}: {e}")
                raise e

