from pydantic import BaseModel, Field
from typing import Optional
from datetime import date, datetime
from decimal import Decimal

import psycopg2
from psycopg2.extras import RealDictCursor
from typing import List, Optional, Dict, Any
from datetime import date, datetime
from decimal import Decimal

class InsideTradeData(BaseModel):
    """内部交易记录数据模型"""
    
    id: Optional[int] = Field(None, description="主键ID")
    stock_code: str = Field(..., max_length=20, description="股票代码")
    stock_name: str = Field(..., max_length=100, description="股票名称")
    change_date: date = Field(..., description="变动日期")
    change_person: str = Field(..., max_length=50, description="变动人")
    change_shares: int = Field(..., description="变动股数")
    avg_price: Decimal = Field(..., max_digits=10, decimal_places=2, description="成交均价")
    shares_after_change: Decimal = Field(..., max_digits=15, decimal_places=1, description="变动后持股数")
    relation_to_executive: Optional[str] = Field(None, max_length=100, description="与董监高关系")
    executive_position: Optional[str] = Field(None, max_length=100, description="董监高职务")
    created_at: Optional[datetime] = Field(None, description="创建时间")
    updated_at: Optional[datetime] = Field(None, description="更新时间")
    
    class Config:
        # 启用 ORM 模式，便于与 SQLAlchemy 等 ORM 框架集成
        from_attributes = True
        # 允许使用字段别名
        populate_by_name = True
        # JSON 编码配置
        json_encoders = {
            Decimal: float,  # 将 Decimal 类型序列化为 float
            datetime: lambda v: v.isoformat(),  # 时间格式化
            date: lambda v: v.isoformat()  # 日期格式化
        }
        
    def __str__(self) -> str:
        return f"InsideTradeData(stock_code={self.stock_code}, change_person={self.change_person}, change_date={self.change_date})"
    
    def __repr__(self) -> str:
        return self.__str__()



class InsideTradeDB:
    """内部交易记录数据库操作类"""
    
    def __init__(self, conn: psycopg2.connect):
        self.conn = conn
    
    def insert(self, trade_data: InsideTradeData) -> int:
        """插入一条内部交易记录
        
        Args:
            trade_data: InsideTradeData 实例
            
        Returns:
            int: 插入记录的 ID
        """
        sql = """
        INSERT INTO tb_inside_trade (
            stock_code, stock_name, change_date, change_person, 
            change_shares, avg_price, shares_after_change, 
            relation_to_executive, executive_position
        ) VALUES (
            %(stock_code)s, %(stock_name)s, %(change_date)s, %(change_person)s,
            %(change_shares)s, %(avg_price)s, %(shares_after_change)s,
            %(relation_to_executive)s, %(executive_position)s
        ) RETURNING id
        """
        
        with self.conn.cursor() as cursor:
            cursor.execute(sql, {
                'stock_code': trade_data.stock_code,
                'stock_name': trade_data.stock_name,
                'change_date': trade_data.change_date,
                'change_person': trade_data.change_person,
                'change_shares': trade_data.change_shares,
                'avg_price': trade_data.avg_price,
                'shares_after_change': trade_data.shares_after_change,
                'relation_to_executive': trade_data.relation_to_executive,
                'executive_position': trade_data.executive_position
            })
            record_id = cursor.fetchone()[0]
            self.conn.commit()
            return record_id
    
    def batch_insert(self, trade_data_list: List[InsideTradeData]) -> List[int]:
        """批量插入内部交易记录
        
        Args:
            trade_data_list: InsideTradeData 实例列表
            
        Returns:
            List[int]: 插入记录的 ID 列表
        """
        sql = """
        INSERT INTO tb_inside_trade (
            stock_code, stock_name, change_date, change_person, 
            change_shares, avg_price, shares_after_change, 
            relation_to_executive, executive_position
        ) VALUES (
            %(stock_code)s, %(stock_name)s, %(change_date)s, %(change_person)s,
            %(change_shares)s, %(avg_price)s, %(shares_after_change)s,
            %(relation_to_executive)s, %(executive_position)s
        ) RETURNING id
        """
        
        record_ids = []
        with self.conn.cursor() as cursor:
            for trade_data in trade_data_list:
                cursor.execute(sql, {
                    'stock_code': trade_data.stock_code,
                    'stock_name': trade_data.stock_name,
                    'change_date': trade_data.change_date,
                    'change_person': trade_data.change_person,
                    'change_shares': trade_data.change_shares,
                    'avg_price': trade_data.avg_price,
                    'shares_after_change': trade_data.shares_after_change,
                    'relation_to_executive': trade_data.relation_to_executive,
                    'executive_position': trade_data.executive_position
                })
                record_ids.append(cursor.fetchone()[0])
            self.conn.commit()
        return record_ids
    
    def select_by_id(self, record_id: int) -> Optional[Dict[str, Any]]:
        """根据 ID 查询单条记录
        
        Args:
            record_id: 记录 ID
            
        Returns:
            Optional[Dict[str, Any]]: 查询结果字典，如果未找到返回 None
        """
        sql = "SELECT * FROM tb_inside_trade WHERE id = %s"
        
        with self.conn.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(sql, (record_id,))
            result = cursor.fetchone()
            return dict(result) if result else None
    
    def select_by_stock_code(self, stock_code: str, limit: int = 100, offset: int = 0) -> List[Dict[str, Any]]:
        """根据股票代码查询记录
        
        Args:
            stock_code: 股票代码
            limit: 限制返回数量
            offset: 偏移量
            
        Returns:
            List[Dict[str, Any]]: 查询结果列表
        """
        sql = """
        SELECT * FROM tb_inside_trade 
        WHERE stock_code = %s 
        ORDER BY change_date DESC 
        LIMIT %s OFFSET %s
        """
        
        with self.conn.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(sql, (stock_code, limit, offset))
            results = cursor.fetchall()
            return [dict(row) for row in results]
    
    def select_by_date_range(self, start_date: date, end_date: date, 
                           stock_code: Optional[str] = None) -> List[Dict[str, Any]]:
        """根据日期范围查询记录
        
        Args:
            start_date: 开始日期
            end_date: 结束日期
            stock_code: 可选的股票代码过滤
            
        Returns:
            List[Dict[str, Any]]: 查询结果列表
        """
        sql = """
        SELECT * FROM tb_inside_trade 
        WHERE change_date BETWEEN %s AND %s
        """
        params = [start_date, end_date]
        
        if stock_code:
            sql += " AND stock_code = %s"
            params.append(stock_code)
        
        sql += " ORDER BY change_date DESC"
        
        with self.conn.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(sql, params)
            results = cursor.fetchall()
            return [dict(row) for row in results]
    
    def select_by_person(self, change_person: str) -> List[Dict[str, Any]]:
        """根据变动人查询记录
        
        Args:
            change_person: 变动人姓名
            
        Returns:
            List[Dict[str, Any]]: 查询结果列表
        """
        sql = """
        SELECT * FROM tb_inside_trade 
        WHERE change_person = %s 
        ORDER BY change_date DESC
        """
        
        with self.conn.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(sql, (change_person,))
            results = cursor.fetchall()
            return [dict(row) for row in results]
    
    def select_all(self, limit: int = 1000, offset: int = 0) -> List[Dict[str, Any]]:
        """查询所有记录
        
        Args:
            limit: 限制返回数量
            offset: 偏移量
            
        Returns:
            List[Dict[str, Any]]: 查询结果列表
        """
        sql = """
        SELECT * FROM tb_inside_trade 
        ORDER BY change_date DESC 
        LIMIT %s OFFSET %s
        """
        
        with self.conn.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(sql, (limit, offset))
            results = cursor.fetchall()
            return [dict(row) for row in results]
    
    def update_by_id(self, record_id: int, trade_data: InsideTradeData) -> bool:
        """根据 ID 更新记录
        
        Args:
            record_id: 记录 ID
            trade_data: 更新的数据
            
        Returns:
            bool: 更新是否成功
        """
        sql = """
        UPDATE tb_inside_trade SET
            stock_code = %(stock_code)s,
            stock_name = %(stock_name)s,
            change_date = %(change_date)s,
            change_person = %(change_person)s,
            change_shares = %(change_shares)s,
            avg_price = %(avg_price)s,
            shares_after_change = %(shares_after_change)s,
            relation_to_executive = %(relation_to_executive)s,
            executive_position = %(executive_position)s,
            updated_at = CURRENT_TIMESTAMP
        WHERE id = %(id)s
        """
        
        with self.conn.cursor() as cursor:
            cursor.execute(sql, {
                'id': record_id,
                'stock_code': trade_data.stock_code,
                'stock_name': trade_data.stock_name,
                'change_date': trade_data.change_date,
                'change_person': trade_data.change_person,
                'change_shares': trade_data.change_shares,
                'avg_price': trade_data.avg_price,
                'shares_after_change': trade_data.shares_after_change,
                'relation_to_executive': trade_data.relation_to_executive,
                'executive_position': trade_data.executive_position
            })
            affected_rows = cursor.rowcount
            self.conn.commit()
            return affected_rows > 0
    
    def delete_by_id(self, record_id: int) -> bool:
        """根据 ID 删除记录
        
        Args:
            record_id: 记录 ID
            
        Returns:
            bool: 删除是否成功
        """
        sql = "DELETE FROM tb_inside_trade WHERE id = %s"
        
        with self.conn.cursor() as cursor:
            cursor.execute(sql, (record_id,))
            affected_rows = cursor.rowcount
            self.conn.commit()
            return affected_rows > 0
    
    def delete_by_stock_code(self, stock_code: str) -> int:
        """根据股票代码删除记录
        
        Args:
            stock_code: 股票代码
            
        Returns:
            int: 删除的记录数量
        """
        sql = "DELETE FROM tb_inside_trade WHERE stock_code = %s"
        
        with self.conn.cursor() as cursor:
            cursor.execute(sql, (stock_code,))
            affected_rows = cursor.rowcount
            self.conn.commit()
            return affected_rows
    
    def delete_by_date_range(self, start_date: date, end_date: date) -> int:
        """根据日期范围删除记录
        
        Args:
            start_date: 开始日期
            end_date: 结束日期
            
        Returns:
            int: 删除的记录数量
        """
        sql = "DELETE FROM tb_inside_trade WHERE change_date BETWEEN %s AND %s"
        
        with self.conn.cursor() as cursor:
            cursor.execute(sql, (start_date, end_date))
            affected_rows = cursor.rowcount
            self.conn.commit()
            return affected_rows
    
    def count_total(self) -> int:
        """统计总记录数
        
        Returns:
            int: 总记录数
        """
        sql = "SELECT COUNT(*) FROM tb_inside_trade"
        
        with self.conn.cursor() as cursor:
            cursor.execute(sql)
            return cursor.fetchone()[0]
    
    def count_by_stock_code(self, stock_code: str) -> int:
        """统计指定股票代码的记录数
        
        Args:
            stock_code: 股票代码
            
        Returns:
            int: 记录数
        """
        sql = "SELECT COUNT(*) FROM tb_inside_trade WHERE stock_code = %s"
        
        with self.conn.cursor() as cursor:
            cursor.execute(sql, (stock_code,))
            return cursor.fetchone()[0]