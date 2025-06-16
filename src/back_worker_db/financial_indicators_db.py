from pandas.core.indexes.base import str_t
from pydantic import BaseModel, Field
from typing import Optional
from datetime import date, datetime
from decimal import Decimal
import logging
from typing import List, Optional, Dict, Any
from datetime import date, datetime
from decimal import Decimal
import psycopg2
from psycopg2.extras import RealDictCursor
from psycopg2 import sql
import pandas as pd

logger = logging.getLogger(__name__)

class FinancialIndicatorsData(BaseModel):
    """财务指标数据模型"""
    
    # 主键和基础信息
    id: Optional[int] = Field(None, description="主键ID")
    ticker: str = Field(..., description="股票代码")
    report_date: date = Field(..., description="报告日期")
    
    # 每股指标
    diluted_eps: Optional[Decimal] = Field(None, description="摊薄每股收益(元)")
    weighted_eps: Optional[Decimal] = Field(None, description="加权每股收益(元)")
    adjusted_eps: Optional[Decimal] = Field(None, description="每股收益_调整后(元)")
    eps_excluding_non_recurring: Optional[Decimal] = Field(None, description="扣除非经常性损益后的每股收益(元)")
    book_value_per_share_before_adj: Optional[Decimal] = Field(None, description="每股净资产_调整前(元)")
    book_value_per_share_after_adj: Optional[Decimal] = Field(None, description="每股净资产_调整后(元)")
    operating_cash_flow_per_share: Optional[Decimal] = Field(None, description="每股经营性现金流(元)")
    capital_reserve_per_share: Optional[Decimal] = Field(None, description="每股资本公积金(元)")
    retained_earnings_per_share: Optional[Decimal] = Field(None, description="每股未分配利润(元)")
    adjusted_book_value_per_share: Optional[Decimal] = Field(None, description="调整后的每股净资产(元)")
    
    # 盈利能力指标
    total_asset_profit_rate: Optional[Decimal] = Field(None, description="总资产利润率(%)")
    main_business_profit_margin: Optional[Decimal] = Field(None, description="主营业务利润率(%)")
    roa: Optional[Decimal] = Field(None, description="总资产净利润率(%)")
    cost_expense_profit_rate: Optional[Decimal] = Field(None, description="成本费用利润率(%)")
    operating_profit_margin: Optional[Decimal] = Field(None, description="营业利润率(%)")
    main_business_cost_rate: Optional[Decimal] = Field(None, description="主营业务成本率(%)")
    net_profit_margin: Optional[Decimal] = Field(None, description="销售净利率(%)")
    equity_return_rate: Optional[Decimal] = Field(None, description="股本报酬率(%)")
    roe: Optional[Decimal] = Field(None, description="净资产报酬率(%)")
    asset_return_rate: Optional[Decimal] = Field(None, description="资产报酬率(%)")
    gross_profit_margin: Optional[Decimal] = Field(None, description="销售毛利率(%)")
    
    # 财务结构指标
    three_expense_ratio: Optional[Decimal] = Field(None, description="三项费用比重")
    non_main_business_ratio: Optional[Decimal] = Field(None, description="非主营比重")
    main_profit_ratio: Optional[Decimal] = Field(None, description="主营利润比重")
    dividend_payout_ratio: Optional[Decimal] = Field(None, description="股息发放率(%)")
    investment_return_rate: Optional[Decimal] = Field(None, description="投资收益率(%)")
    
    # 绝对金额指标
    main_business_profit: Optional[Decimal] = Field(None, description="主营业务利润(元)")
    net_asset_yield: Optional[Decimal] = Field(None, description="净资产收益率(%)")
    weighted_roe: Optional[Decimal] = Field(None, description="加权净资产收益率(%)")
    net_profit_excluding_non_recurring: Optional[Decimal] = Field(None, description="扣除非经常性损益后的净利润(元)")
    
    # 成长能力指标
    main_revenue_growth_rate: Optional[Decimal] = Field(None, description="主营业务收入增长率(%)")
    net_profit_growth_rate: Optional[Decimal] = Field(None, description="净利润增长率(%)")
    net_asset_growth_rate: Optional[Decimal] = Field(None, description="净资产增长率(%)")
    total_asset_growth_rate: Optional[Decimal] = Field(None, description="总资产增长率(%)")
    
    # 营运能力指标
    accounts_receivable_turnover: Optional[Decimal] = Field(None, description="应收账款周转率(次)")
    accounts_receivable_days: Optional[Decimal] = Field(None, description="应收账款周转天数(天)")
    inventory_turnover_days: Optional[Decimal] = Field(None, description="存货周转天数(天)")
    inventory_turnover: Optional[Decimal] = Field(None, description="存货周转率(次)")
    fixed_asset_turnover: Optional[Decimal] = Field(None, description="固定资产周转率(次)")
    total_asset_turnover: Optional[Decimal] = Field(None, description="总资产周转率(次)")
    total_asset_turnover_days: Optional[Decimal] = Field(None, description="总资产周转天数(天)")
    current_asset_turnover: Optional[Decimal] = Field(None, description="流动资产周转率(次)")
    current_asset_turnover_days: Optional[Decimal] = Field(None, description="流动资产周转天数(天)")
    equity_turnover: Optional[Decimal] = Field(None, description="股东权益周转率(次)")
    
    # 偿债能力指标
    current_ratio: Optional[Decimal] = Field(None, description="流动比率")
    quick_ratio: Optional[Decimal] = Field(None, description="速动比率")
    cash_ratio: Optional[Decimal] = Field(None, description="现金比率(%)")
    interest_coverage_ratio: Optional[Decimal] = Field(None, description="利息支付倍数")
    long_term_debt_to_working_capital: Optional[Decimal] = Field(None, description="长期债务与营运资金比率(%)")
    equity_ratio: Optional[Decimal] = Field(None, description="股东权益比率(%)")
    long_term_debt_ratio: Optional[Decimal] = Field(None, description="长期负债比率(%)")
    equity_to_fixed_asset_ratio: Optional[Decimal] = Field(None, description="股东权益与固定资产比率(%)")
    debt_to_equity_ratio: Optional[Decimal] = Field(None, description="负债与所有者权益比率(%)")
    long_term_asset_to_fund_ratio: Optional[Decimal] = Field(None, description="长期资产与长期资金比率(%)")
    capitalization_ratio: Optional[Decimal] = Field(None, description="资本化比率(%)")
    fixed_asset_net_rate: Optional[Decimal] = Field(None, description="固定资产净值率(%)")
    capital_fixation_ratio: Optional[Decimal] = Field(None, description="资本固定化比率(%)")
    property_ratio: Optional[Decimal] = Field(None, description="产权比率(%)")
    liquidation_value_ratio: Optional[Decimal] = Field(None, description="清算价值比率(%)")
    fixed_asset_ratio: Optional[Decimal] = Field(None, description="固定资产比重(%)")
    debt_to_asset_ratio: Optional[Decimal] = Field(None, description="资产负债率(%)")
    total_assets: Optional[Decimal] = Field(None, description="总资产(元)")
    
    # 现金流量指标
    operating_cash_to_revenue_ratio: Optional[Decimal] = Field(None, description="经营现金净流量对销售收入比率(%)")
    operating_cash_to_asset_ratio: Optional[Decimal] = Field(None, description="资产的经营现金流量回报率(%)")
    operating_cash_to_net_profit_ratio: Optional[Decimal] = Field(None, description="经营现金净流量与净利润的比率(%)")
    operating_cash_to_debt_ratio: Optional[Decimal] = Field(None, description="经营现金净流量对负债比率(%)")
    cash_flow_ratio: Optional[Decimal] = Field(None, description="现金流量比率(%)")
    
    # 投资相关
    short_term_stock_investment: Optional[Decimal] = Field(None, description="短期股票投资(元)")
    short_term_bond_investment: Optional[Decimal] = Field(None, description="短期债券投资(元)")
    short_term_other_investment: Optional[Decimal] = Field(None, description="短期其它经营性投资(元)")
    long_term_stock_investment: Optional[Decimal] = Field(None, description="长期股票投资(元)")
    long_term_bond_investment: Optional[Decimal] = Field(None, description="长期债券投资(元)")
    long_term_other_investment: Optional[Decimal] = Field(None, description="长期其它经营性投资(元)")
    
    # 应收账款账龄分析
    accounts_receivable_within_1y: Optional[Decimal] = Field(None, description="1年以内应收帐款(元)")
    accounts_receivable_1_2y: Optional[Decimal] = Field(None, description="1-2年以内应收帐款(元)")
    accounts_receivable_2_3y: Optional[Decimal] = Field(None, description="2-3年以内应收帐款(元)")
    accounts_receivable_over_3y: Optional[Decimal] = Field(None, description="3年以内应收帐款(元)")
    
    # 预付款账龄分析
    prepaid_within_1y: Optional[Decimal] = Field(None, description="1年以内预付货款(元)")
    prepaid_1_2y: Optional[Decimal] = Field(None, description="1-2年以内预付货款(元)")
    prepaid_2_3y: Optional[Decimal] = Field(None, description="2-3年以内预付货款(元)")
    prepaid_over_3y: Optional[Decimal] = Field(None, description="3年以内预付货款(元)")
    
    # 其他应收款账龄分析
    other_receivables_within_1y: Optional[Decimal] = Field(None, description="1年以内其它应收款(元)")
    other_receivables_1_2y: Optional[Decimal] = Field(None, description="1-2年以内其它应收款(元)")
    other_receivables_2_3y: Optional[Decimal] = Field(None, description="2-3年以内其它应收款(元)")
    other_receivables_over_3y: Optional[Decimal] = Field(None, description="3年以内其它应收款(元)")
    
    # 创建和更新时间
    created_at: Optional[datetime] = Field(None, description="创建时间")
    updated_at: Optional[datetime] = Field(None, description="更新时间")
    is_deleted: bool
    
    class Config:
        """Pydantic 配置"""
        # 允许从 ORM 对象创建实例
        from_attributes = True
        # 使用枚举值而不是枚举名称
        use_enum_values = True
        # 验证赋值
        validate_assignment = True
        # JSON 编码器配置
        json_encoders = {
            Decimal: lambda v: float(v) if v is not None else None,
            datetime: lambda v: v.isoformat() if v is not None else None,
            date: lambda v: v.isoformat() if v is not None else None,
        }
        
    def to_dict(self) -> dict:
        """转换为字典格式"""
        return self.model_dump(exclude_none=True)
    
    @classmethod
    def from_raw_data(cls, raw_data: dict, ticker:str, report_date: date) -> 'FinancialIndicatorsData':
        """从原始数据创建实例的工厂方法"""
        # 这里可以添加数据映射逻辑
        # 例如将中文字段名映射到英文字段名
        field_mapping = {
            '股票代码': 'ticker',
            '报告日期': 'report_date',
            '摊薄每股收益(元)': 'diluted_eps',
            '加权每股收益(元)': 'weighted_eps',
            '每股收益_调整后(元)': 'adjusted_eps',
            '扣除非经常性损益后的每股收益(元)': 'eps_excluding_non_recurring',
            '每股净资产_调整前(元)': 'book_value_per_share_before_adj',
            '每股净资产_调整后(元)': 'book_value_per_share_after_adj',
            '每股经营性现金流(元)': 'operating_cash_flow_per_share',
            '每股资本公积金(元)': 'capital_reserve_per_share',
            '每股未分配利润(元)': 'retained_earnings_per_share',
            '调整后的每股净资产(元)': 'adjusted_book_value_per_share',
            '总资产利润率(%)': 'total_asset_profit_rate',
            '主营业务利润率(%)': 'main_business_profit_margin',
            '总资产净利润率(%)': 'roa',
            '成本费用利润率(%)': 'cost_expense_profit_rate',
            '营业利润率(%)': 'operating_profit_margin',
            '主营业务成本率(%)': 'main_business_cost_rate',
            '销售净利率(%)': 'net_profit_margin',
            '股本报酬率(%)': 'equity_return_rate',
            '净资产报酬率(%)': 'roe',
            '资产报酬率(%)': 'asset_return_rate',
            '销售毛利率(%)': 'gross_profit_margin',
            '三项费用比重': 'three_expense_ratio',
            '非主营比重': 'non_main_business_ratio',
            '主营利润比重': 'main_profit_ratio',
            '股息发放率(%)': 'dividend_payout_ratio',
            '投资收益率(%)': 'investment_return_rate',
            '主营业务利润(元)': 'main_business_profit',
            '净资产收益率(%)': 'net_asset_yield',
            '加权净资产收益率(%)': 'weighted_roe',
            '扣除非经常性损益后的净利润(元)': 'net_profit_excluding_non_recurring',
            '主营业务收入增长率(%)': 'main_revenue_growth_rate',
            '净利润增长率(%)': 'net_profit_growth_rate',
            '净资产增长率(%)': 'net_asset_growth_rate',
            '总资产增长率(%)': 'total_asset_growth_rate',
            '应收账款周转率(次)': 'accounts_receivable_turnover',
            '应收账款周转天数(天)': 'accounts_receivable_days',
            '存货周转天数(天)': 'inventory_turnover_days',
            '存货周转率(次)': 'inventory_turnover',
            '固定资产周转率(次)': 'fixed_asset_turnover',
            '总资产周转率(次)': 'total_asset_turnover',
            '总资产周转天数(天)': 'total_asset_turnover_days',
            '流动资产周转率(次)': 'current_asset_turnover',
            '流动资产周转天数(天)': 'current_asset_turnover_days',
            '股东权益周转率(次)': 'equity_turnover',
            '流动比率': 'current_ratio',
            '速动比率': 'quick_ratio',
            '现金比率(%)': 'cash_ratio',
            '利息支付倍数': 'interest_coverage_ratio',
            '长期债务与营运资金比率(%)': 'long_term_debt_to_working_capital',
            '股东权益比率(%)': 'equity_ratio',
            '长期负债比率(%)': 'long_term_debt_ratio',
            '股东权益与固定资产比率(%)': 'equity_to_fixed_asset_ratio',
            '负债与所有者权益比率(%)': 'debt_to_equity_ratio',
            '长期资产与长期资金比率(%)': 'long_term_asset_to_fund_ratio',
            '资本化比率(%)': 'capitalization_ratio',
            '固定资产净值率(%)': 'fixed_asset_net_rate',
            '资本固定化比率(%)': 'capital_fixation_ratio',
            '产权比率(%)': 'property_ratio',
            '清算价值比率(%)': 'liquidation_value_ratio',
            '固定资产比重(%)': 'fixed_asset_ratio',
            '资产负债率(%)': 'debt_to_asset_ratio',
            '总资产(元)': 'total_assets',
            '经营现金净流量对销售收入比率(%)': 'operating_cash_to_revenue_ratio',
            '资产的经营现金流量回报率(%)': 'operating_cash_to_asset_ratio',
            '经营现金净流量与净利润的比率(%)': 'operating_cash_to_net_profit_ratio',
            '经营现金净流量对负债比率(%)': 'operating_cash_to_debt_ratio',
            '现金流量比率(%)': 'cash_flow_ratio',
            '长期股票投资(元)': 'long_term_stock_investment',
        }
        
        mapped_data = {'report_date': report_date, 'ticker': ticker}
        for chinese_name, value in raw_data.items():
            if chinese_name in field_mapping:
                english_name = field_mapping[chinese_name]
                # 处理 nan 值
                if pd.isna(value):
                    mapped_data[english_name] = None
                else:
                    try:
                        mapped_data[english_name] = Decimal(str(value))
                    except (ValueError, TypeError):
                        mapped_data[english_name] = None
        
        return cls(**mapped_data)

class FinancialIndicatorsDB:
    """财务指标数据库操作类"""
    
    def __init__(self, conn: psycopg2.connect):
        """
        初始化数据库连接
        
        Args:
            conn: psycopg2 数据库连接对象
        """
        self.conn = conn
    
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
            logger.error(f"Database operation failed: {e}")
            raise
        finally:
            cursor.close()
    
    def _convert_record_to_model(self, record: dict) -> FinancialIndicatorsData:
        """将数据库记录转换为 Pydantic 模型"""
        if not record:
            return None
        
        # 处理 None 值和数据类型转换
        data = {}
        for key, value in record.items():
            if value is None:
                data[key] = None
            elif isinstance(value, Decimal):
                data[key] = value
            else:
                data[key] = value
                
        return FinancialIndicatorsData(**data)
    
    def _model_to_insert_data(self, model: FinancialIndicatorsData) -> Dict[str, Any]:
        """将 Pydantic 模型转换为插入数据"""
        data = model.model_dump(exclude={'id', 'created_at', 'updated_at', 'is_deleted'}, exclude_none=True)
        
        # 确保 report_date 存在
        if 'report_date' not in data or 'ticker' not in data:
            raise ValueError("report_date or ticker is required")
        
        return data
    
    def create(self, data: FinancialIndicatorsData) -> FinancialIndicatorsData:
        """
        创建新的财务指标记录
        
        Args:
            data: 财务指标数据
            
        Returns:
            创建后的财务指标数据（包含ID）
        """
        insert_data = self._model_to_insert_data(data)
        
        # 构建 SQL 语句
        columns = list(insert_data.keys())
        placeholders = ['%s'] * len(columns)
        values = [insert_data[col] for col in columns]
        
        query = sql.SQL("""
            INSERT INTO tb_financial_indicators ({})
            VALUES ({})
            RETURNING *
        """).format(
            sql.SQL(', ').join(map(sql.Identifier, columns)),
            sql.SQL(', ').join(sql.Placeholder() * len(columns))
        )
        
        with self.get_cursor() as cursor:
            try:
                cursor.execute(query, values)
                record = cursor.fetchone()
                logger.info(f"Created financial indicator record with ID: {record['id']}")
                return self._convert_record_to_model(dict(record))
            except Exception as e:
                logger.error(f"Error creating financial indicator: {e}")
                raise
    
    def get_by_id(self, record_id: int) -> Optional[FinancialIndicatorsData]:
        """
        根据ID查询财务指标
        
        Args:
            record_id: 记录ID
            
        Returns:
            财务指标数据或None
        """
        query = "SELECT * FROM tb_financial_indicators WHERE id = %s"
        
        with self.get_cursor(commit=False) as cursor:
            try:
                cursor.execute(query, (record_id,))
                record = cursor.fetchone()
                if record:
                    return self._convert_record_to_model(dict(record))
                return None
            except Exception as e:
                logger.error(f"Error fetching financial indicator by ID {record_id}: {e}")
                raise
    
    def get_by_ticker_date(self, ticker: str, report_date: date) -> List[FinancialIndicatorsData]:
        """
        根据报告日期查询财务指标
        
        Args:
            report_date: 报告日期
            
        Returns:
            财务指标数据列表
        """
        query = "SELECT * FROM tb_financial_indicators WHERE ticker = % and report_date = %s ORDER BY id"
        
        with self.get_cursor(commit=False) as cursor:
            try:
                cursor.execute(query, (ticker, report_date,))
                records = cursor.fetchall()
                return [self._convert_record_to_model(dict(record)) for record in records]
            except Exception as e:
                logger.error(f"Error fetching financial indicators by date {report_date}: {e}")
                raise
    
    def get_by_date_range(
        self, 
        ticker: str,
        start_date: date =None, 
        end_date: date = None,
        limit: Optional[int] = None,
        offset: Optional[int] = None
    ) -> List[FinancialIndicatorsData]:
        """
        根据日期范围查询财务指标
        
        Args:
            ticker: 股票代码
            start_date: 开始日期
            end_date: 结束日期
            limit: 限制数量
            offset: 偏移量
            
        Returns:
            财务指标数据列表
        """
        params = ['ticker = %s']
        values = [ticker]
        if start_date:
            params.append('report_date >= %s')
            values.append(start_date)
        if end_date:
            params.append('report_date <= %s')
            values.append(end_date)
        params_str = ' AND '.join(params)
        query = f"""
            SELECT * FROM tb_financial_indicators 
            WHERE {params_str}
            ORDER BY report_date DESC, id
        """
        if limit is not None:
            query += " LIMIT %s"
            params.append(limit)
        
        if offset is not None:
            query += " OFFSET %s"
            params.append(offset)
        
        with self.get_cursor(commit=False) as cursor:
            try:
                cursor.execute(query, params)
                records = cursor.fetchall()
                return [self._convert_record_to_model(dict(record)) for record in records]
            except Exception as e:
                logger.error(f"Error fetching financial indicators by date range: {e}")
                raise
    
    def update(self, record_id: int, data: FinancialIndicatorsData) -> Optional[FinancialIndicatorsData]:
        """
        更新财务指标记录
        
        Args:
            record_id: 记录ID
            data: 更新的数据
            
        Returns:
            更新后的财务指标数据或None
        """
        update_data = self._model_to_insert_data(data)
        update_data['updated_at'] = datetime.now()
        
        # 构建 SET 子句
        set_clauses = []
        values = []
        
        for column, value in update_data.items():
            set_clauses.append(f"{column} = %s")
            values.append(value)
        
        # 添加 WHERE 条件的参数
        values.append(record_id)
        
        query = f"""
            UPDATE tb_financial_indicators 
            SET {', '.join(set_clauses)}
            WHERE id = %s
            RETURNING *
        """
        
        with self.get_cursor() as cursor:
            try:
                cursor.execute(query, values)
                record = cursor.fetchone()
                if record:
                    logger.info(f"Updated financial indicator record with ID: {record_id}")
                    return self._convert_record_to_model(dict(record))
                return None
            except Exception as e:
                logger.error(f"Error updating financial indicator {record_id}: {e}")
                raise
    
    def delete(self, record_id: int) -> bool:
        """
        删除财务指标记录
        
        Args:
            record_id: 记录ID
            
        Returns:
            是否删除成功
        """
        query = "DELETE FROM tb_financial_indicators WHERE id = %s"
        
        with self.get_cursor() as cursor:
            try:
                cursor.execute(query, (record_id,))
                deleted = cursor.rowcount > 0
                if deleted:
                    logger.info(f"Deleted financial indicator record with ID: {record_id}")
                return deleted
            except Exception as e:
                logger.error(f"Error deleting financial indicator {record_id}: {e}")
                raise
    
    def delete_by_ticker_date(self, ticker: str, report_date: date) -> int:
        """
        根据报告日期删除财务指标记录
        
        Args:
            ticker: 股票代码
            report_date: 报告日期
            
        Returns:
            删除的记录数量
        """
        query = "DELETE FROM tb_financial_indicators WHERE ticker = % AND report_date = %s"
        
        with self.get_cursor() as cursor:
            try:
                cursor.execute(query, (ticker, report_date,))
                deleted_count = cursor.rowcount
                logger.info(f"Deleted {deleted_count} financial indicator records for ticker: {ticker} and date: {report_date}")
                return deleted_count
            except Exception as e:
                logger.error(f"Error deleting financial indicators by date {report_date}: {e}")
                raise
    
    def bulk_create(self, data_list: List[FinancialIndicatorsData]) -> List[FinancialIndicatorsData]:
        """
        批量创建财务指标记录
        
        Args:
            data_list: 财务指标数据列表
            
        Returns:
            创建后的财务指标数据列表
        """
        if not data_list:
            return []
        
        # 准备批量插入数据
        insert_data_list = [self._model_to_insert_data(data) for data in data_list]
        
        # 获取所有字段（以第一条记录为准）
        columns = list(insert_data_list[0].keys())
        
        with self.get_cursor() as cursor:
            try:
                results = []
                
                # 构建批量插入 SQL
                placeholders = ['%s'] * len(columns)
                query = sql.SQL("""
                    INSERT INTO tb_financial_indicators ({})
                    VALUES ({})
                    RETURNING *
                """).format(
                    sql.SQL(', ').join(map(sql.Identifier, columns)),
                    sql.SQL(', ').join(sql.Placeholder() * len(columns))
                )
                
                for insert_data in insert_data_list:
                    values = [insert_data[col] for col in columns]
                    cursor.execute(query, values)
                    record = cursor.fetchone()
                    results.append(self._convert_record_to_model(dict(record)))
                
                logger.info(f"Bulk created {len(results)} financial indicator records")
                return results
                    
            except Exception as e:
                logger.error(f"Error in bulk create: {e}")
                raise
    
    def bulk_create_efficient(self, data_list: List[FinancialIndicatorsData]) -> int:
        """
        高效批量创建财务指标记录（使用 execute_values）
        
        Args:
            data_list: 财务指标数据列表
            
        Returns:
            创建的记录数量
        """
        if not data_list:
            return 0
        
        from psycopg2.extras import execute_values
        
        # 准备批量插入数据
        insert_data_list = [self._model_to_insert_data(data) for data in data_list]
        
        # 获取所有字段（以第一条记录为准）
        columns = list(insert_data_list[0].keys())
        
        # 准备数据
        values_list = []
        for insert_data in insert_data_list:
            values_list.append([insert_data[col] for col in columns])
        
        query = sql.SQL("""
            INSERT INTO tb_financial_indicators ({})
            VALUES %s
        """).format(
            sql.SQL(', ').join(map(sql.Identifier, columns))
        )
        
        with self.get_cursor() as cursor:
            try:
                execute_values(cursor, query, values_list)
                created_count = cursor.rowcount
                logger.info(f"Bulk created {created_count} financial indicator records efficiently")
                return created_count
            except Exception as e:
                logger.error(f"Error in efficient bulk create: {e}")
                raise
    
    def exists(self, ticker: str, report_date: date) -> bool:
        """
        检查指定日期的记录是否存在
        
        Args:
            ticker: 股票代码
            report_date: 报告日期
            
        Returns:
            是否存在记录
        """
        query = "SELECT EXISTS(SELECT 1 FROM tb_financial_indicators WHERE ticker = %s AND report_date = %s)"
        
        with self.get_cursor(commit=False) as cursor:
            try:
                cursor.execute(query, (ticker, report_date,))
                result = cursor.fetchone()[0]
                return result
            except Exception as e:
                logger.error(f"Error checking existence for date {report_date}: {e}")
                raise
    
    def get_latest_date(self, ticker: str) -> Optional[date]:
        """
        获取最新的报告日期
        
        Returns:
            最新的报告日期或None
        """
        query = "SELECT MAX(report_date) FROM tb_financial_indicators WHERE ticker = %s"
        
        with self.get_cursor(commit=False) as cursor:
            try:
                cursor.execute(query, (ticker,))
                result = cursor.fetchone()[0]
                return result
            except Exception as e:
                logger.error(f"Error getting latest date: {e}")
                raise
    
    def count(self, ticker: Optional[str] = None, report_date: Optional[date] = None) -> int:
        """
        统计记录数量
        
        Args:
            ticker: 可选的股票代码过滤条件
            report_date: 可选的报告日期过滤条件
            
        Returns:
            记录数量
        """
        params = []
        if ticker:
            params.append(ticker)
        if report_date:
            params.append(report_date)
        
        query = "SELECT COUNT(*) FROM tb_financial_indicators"
        if params:
            query += " WHERE " + " AND ".join([f"{col} = %s" for col in params]) 
        
        with self.get_cursor(commit=False) as cursor:
            try:
                cursor.execute(query, params)
                result = cursor.fetchone()[0]
                return result
            except Exception as e:
                logger.error(f"Error counting records: {e}")
                raise
    
    def upsert(self, ticker: str, data: FinancialIndicatorsData, unique_fields: List[str] = None) -> FinancialIndicatorsData:
        """
        插入或更新记录（ON CONFLICT）
        
        Args:
            ticker: 股票代码
            data: 财务指标数据
            unique_fields: 唯一字段列表，默认使用 ['ticker', 'report_date']
            
        Returns:
            插入或更新后的财务指标数据
        """
        if unique_fields is None:
            unique_fields = ['ticker', 'report_date']
        
        insert_data = self._model_to_insert_data(data)
        insert_data['updated_at'] = datetime.now()
        
        columns = list(insert_data.keys())
        placeholders = ['%s'] * len(columns)
        values = [insert_data[col] for col in columns]
        
        # 构建 ON CONFLICT 子句
        update_clauses = [f"{col} = EXCLUDED.{col}" for col in columns if col not in unique_fields + ['updated_at']]
        
        query = sql.SQL("""
            INSERT INTO tb_financial_indicators ({})
            VALUES ({})
            ON CONFLICT ({}) DO UPDATE SET
            {}
            RETURNING *
        """).format(
            sql.SQL(', ').join(map(sql.Identifier, columns)),
            sql.SQL(', ').join(sql.Placeholder() * len(columns)),
            sql.SQL(', ').join(map(sql.Identifier, unique_fields)),
            sql.SQL(', ').join(map(sql.SQL, update_clauses))
        )
        
        with self.get_cursor() as cursor:
            try:
                cursor.execute(query, values)
                record = cursor.fetchone()
                logger.info(f"Upserted financial indicator record")
                return self._convert_record_to_model(dict(record))
            except Exception as e:
                logger.error(f"Error upserting financial indicator: {e}")
                raise
    
    def execute_custom_query(self, query: str, params: tuple = None) -> List[dict]:
        """
        执行自定义查询
        
        Args:
            query: SQL 查询语句
            params: 查询参数
            
        Returns:
            查询结果列表
        """
        with self.get_cursor(commit=False) as cursor:
            try:
                cursor.execute(query, params or ())
                records = cursor.fetchall()
                return [dict(record) for record in records]
            except Exception as e:
                logger.error(f"Error executing custom query: {e}")
                raise
