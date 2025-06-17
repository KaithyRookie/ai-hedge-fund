from pydantic import BaseModel, Field
from typing import Optional
from datetime import date, datetime
from decimal import Decimal

import psycopg2
from psycopg2.extras import RealDictCursor
from typing import List, Optional, Dict, Any
from datetime import datetime
import logging
from decimal import Decimal

class CompanyFactData(BaseModel):
    """公司基本信息数据模型"""
    
    id: Optional[int] = Field(None, description="主键ID")
    company_name: str = Field(..., max_length=255, description="公司名称")
    company_name_en: Optional[str] = Field(None, max_length=255, description="英文名称")
    former_short_name: Optional[str] = Field(None, max_length=255, description="曾用简称")
    a_share_code: Optional[str] = Field(None, max_length=20, description="A股代码")
    a_share_name: Optional[str] = Field(None, max_length=100, description="A股简称")
    b_share_code: Optional[str] = Field(None, max_length=20, description="B股代码")
    b_share_name: Optional[str] = Field(None, max_length=100, description="B股简称")
    h_share_code: Optional[str] = Field(None, max_length=20, description="H股代码")
    h_share_name: Optional[str] = Field(None, max_length=100, description="H股简称")
    selected_indices: Optional[str] = Field(None, description="入选指数")
    market_category: Optional[str] = Field(None, max_length=100, description="所属市场")
    industry_category: Optional[str] = Field(None, max_length=100, description="所属行业")
    legal_representative: Optional[str] = Field(None, max_length=100, description="法人代表")
    registered_capital: Optional[Decimal] = Field(None, max_digits=15, decimal_places=4, description="注册资金")
    establishment_date: Optional[date] = Field(None, description="成立日期")
    listing_date: Optional[date] = Field(None, description="上市日期")
    official_website: Optional[str] = Field(None, max_length=255, description="官方网站")
    email: Optional[str] = Field(None, max_length=255, description="电子邮箱")
    contact_phone: Optional[str] = Field(None, max_length=50, description="联系电话")
    fax: Optional[str] = Field(None, max_length=50, description="传真")
    registered_address: Optional[str] = Field(None, description="注册地址")
    office_address: Optional[str] = Field(None, description="办公地址")
    postal_code: Optional[str] = Field(None, max_length=20, description="邮政编码")
    main_business: Optional[str] = Field(None, description="主营业务")
    business_scope: Optional[str] = Field(None, description="经营范围")
    company_profile: Optional[str] = Field(None, description="机构简介")
    created_at: Optional[datetime] = Field(None, description="创建时间")
    updated_at: Optional[datetime] = Field(None, description="更新时间")
    is_deleted: bool

    class Config:
        """Pydantic 配置"""
        # 允许使用 ORM 模式，便于与数据库 ORM 对象互转
        from_attributes = True
        # 使用枚举值而不是枚举名称
        use_enum_values = True
        # 验证赋值
        validate_assignment = True
        # 允许任意类型（主要用于 Decimal）
        arbitrary_types_allowed = True
        # JSON 编码器配置
        json_encoders = {
            datetime: lambda v: v.isoformat() if v else None,
            date: lambda v: v.isoformat() if v else None,
            Decimal: lambda v: float(v) if v else None,
        }

    def to_dict(self) -> dict:
        """转换为字典"""
        return self.model_dump(exclude_none=True)

    def to_dict_for_db(self) -> dict:
        """转换为适合数据库存储的字典"""
        data = self.model_dump(exclude_none=True, exclude={'id', 'created_at', 'updated_at'})
        return data

from contextlib import contextmanager
class CompanyFactDB:
    """公司基本信息数据库操作类"""
    
    def __init__(self, conn: psycopg2.connect):
        """初始化数据库连接"""
        self.conn = conn
        self.table_name = "tb_company_facts"

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
    
    def create(self, company_data: CompanyFactData) -> int:
        """
        新增公司信息
        
        Args:
            company_data: CompanyFactData对象
            
        Returns:
            int: 新增记录的ID
        """
        # 排除id和时间戳字段
        data_dict = company_data.to_dict_for_db()
        
        # 构建插入SQL
        columns = list(data_dict.keys())
        placeholders = ["%s"] * len(columns)
        values = list(data_dict.values())
        
        query = f"""
        INSERT INTO {self.table_name} ({', '.join(columns)})
        VALUES ({', '.join(placeholders)})
        RETURNING id
        """
        
        with self.get_cursor() as cursor:
            try:
                cursor.execute(query, values)
                new_id = cursor.fetchone()[0]
                self.conn.commit()
                return new_id
            except Exception as e:
                self.conn.rollback()
                logging.error(f"创建公司信息失败: {e}")
                raise e
    
    def get_by_id(self, company_id: int) -> CompanyFactData:
        """
        根据ID查询公司信息
        
        Args:
            company_id: 公司ID
            
        Returns:
            CompanyFactData: 公司信息字典，如果不存在返回None
        """
        query = f"SELECT * FROM {self.table_name} WHERE id = %s"
        with self.get_cursor(False) as cursor:
            cursor.execute(query, (company_id,))
            result = cursor.fetchone()
            return CompanyFactData(**result) if result else None
    
    def get_by_stock_code(self, stock_code: str, stock_type: str = 'A') -> CompanyFactData:
        """
        根据股票代码查询公司信息
        
        Args:
            stock_code: 股票代码
            stock_type: 股票类型 ('A', 'B', 'H')
            
        Returns:
            CompanyFactData: 公司信息字典，如果不存在返回None
        """
        field_mapping = {
            'A': 'a_share_code',
            'B': 'b_share_code', 
            'H': 'h_share_code'
        }
        
        field = field_mapping.get(stock_type.upper())
        if not field:
            raise ValueError("股票类型必须是 'A', 'B' 或 'H'")
        
        query = f"SELECT * FROM {self.table_name} WHERE {field} = %s"
        try:
            with self.get_cursor(False) as cursor:
                cursor.execute(query, (stock_code,))
                result = cursor.fetchone()
                return CompanyFactData(**result) if result else None
        except Exception as e:
            logging.error(f"查询公司信息失败: {e}")
            raise e
    
    def get_by_company_name(self, company_name: str, exact_match: bool = True) -> List[CompanyFactData]:
        """
        根据公司名称查询公司信息
        
        Args:
            company_name: 公司名称
            exact_match: 是否精确匹配，False则模糊查询
            
        Returns:
            List[CompanyFactData]: 公司信息列表
        """
        if exact_match:
            query = f"SELECT * FROM {self.table_name} WHERE company_name = %s"
            params = (company_name,)
        else:
            query = f"SELECT * FROM {self.table_name} WHERE company_name LIKE %s"
            params = (f"%{company_name}%",)
        try:
            with self.get_cursor(False) as cursor:
                cursor.execute(query, params)
                results = cursor.fetchall()
                return [CompanyFactData(**result) for result in results]
        except Exception as e:
            logging.error(f"查询公司信息失败: {e}")
            raise e
    
    def get_by_industry(self, industry: str) -> List[CompanyFactData]:
        """
        根据行业查询公司信息
        
        Args:
            industry: 行业名称
            
        Returns:
            List[Dict]: 公司信息列表
        """
        query = f"SELECT * FROM {self.table_name} WHERE industry_category = %s ORDER BY company_name"
        try:
            with self.get_cursor(False) as cursor:
                cursor.execute(query, (industry,))
                results = cursor.fetchall()
                return [CompanyFactData(**result) for result in results]
        except Exception as e:
            logging.error(f"查询公司信息失败: {e}")
            raise e
    
    def get_by_market(self, market: str) -> List[CompanyFactData]:
        """
        根据市场查询公司信息
        
        Args:
            market: 市场名称
            
        Returns:
            List[CompanyFactData]: 公司信息列表
        """
        query = f"SELECT * FROM {self.table_name} WHERE market_category = %s ORDER BY company_name"
        try:
            with self.get_cursor(False) as cursor:
                cursor.execute(query, (market,))
                results = cursor.fetchall()
                return [CompanyFactData(**result) for result in results]
        except Exception as e:
            logging.error(f"查询公司信息失败: {e}")
            raise e
    
    def get_all(self, limit: int = None, offset: int = 0) -> List[CompanyFactData]:
        """
        查询所有公司信息
        
        Args:
            limit: 限制返回数量
            offset: 偏移量
            
        Returns:
            List[CompanyFactData]: 公司信息列表
        """
        query = f"SELECT * FROM {self.table_name} ORDER BY id"
        
        if limit:
            query += f" LIMIT {limit} OFFSET {offset}"
        
        try:
            with self.get_cursor(False) as cursor:
                cursor.execute(query)
                results = cursor.fetchall()
                return [CompanyFactData(**result) for result in results]
        except Exception as e:
            logging.error(f"查询公司信息失败: {e}")
            raise e
    
    def update_by_id(self, company_id: int, update_data: Dict[str, Any]) -> bool:
        """
        根据ID更新公司信息
        
        Args:
            company_id: 公司ID
            update_data: 更新数据字典
            
        Returns:
            bool: 更新是否成功
        """
        if not update_data:
            return False
        
        # 过滤掉不允许更新的字段
        forbidden_fields = {'id', 'created_at'}
        update_data = {k: v for k, v in update_data.items() if k not in forbidden_fields}
        
        # 添加更新时间
        update_data['updated_at'] = datetime.now()
        
        # 构建更新SQL
        set_clauses = [f"{key} = %s" for key in update_data.keys()]
        values = list(update_data.values()) + [company_id]
        
        query = f"""
        UPDATE {self.table_name} 
        SET {', '.join(set_clauses)}
        WHERE id = %s
        """
        
        try:
            with self.get_cursor() as cursor:
                cursor.execute(query, tuple(values))
                affected_rows = cursor.rowcount
            return affected_rows > 0
        except Exception as e:
            logging.error(f"更新公司信息失败: {e}")
            raise e
    
    def update_by_stock_code(self, stock_code: str, update_data: Dict[str, Any], stock_type: str = 'A') -> bool:
        """
        根据股票代码更新公司信息
        
        Args:
            stock_code: 股票代码
            update_data: 更新数据字典
            stock_type: 股票类型 ('A', 'B', 'H')
            
        Returns:
            bool: 更新是否成功
        """
        field_mapping = {
            'A': 'a_share_code',
            'B': 'b_share_code',
            'H': 'h_share_code'
        }
        
        field = field_mapping.get(stock_type.upper())
        if not field:
            raise ValueError("股票类型必须是 'A', 'B' 或 'H'")
        
        if not update_data:
            return False
        
        # 过滤掉不允许更新的字段
        forbidden_fields = {'id', 'created_at'}
        update_data = {k: v for k, v in update_data.items() if k not in forbidden_fields}
        
        # 添加更新时间
        update_data['updated_at'] = datetime.now()
        
        # 构建更新SQL
        set_clauses = [f"{key} = %s" for key in update_data.keys()]
        values = list(update_data.values()) + [stock_code]
        
        query = f"""
        UPDATE {self.table_name} 
        SET {', '.join(set_clauses)}
        WHERE {field} = %s
        """
        
        try:
            with self.get_cursor() as cursor:
                cursor.execute(query, tuple(values))
                affected_rows = cursor.rowcount
            return affected_rows > 0
        except Exception as e:
            logging.error(f"更新公司信息失败: {e}")
            raise e