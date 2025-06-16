from pydantic import BaseModel, Field, HttpUrl
from typing import Optional
from datetime import datetime

class CompanyNewsData(BaseModel):
    """公司新闻信息数据模型"""
    
    id: Optional[int] = Field(None, description="主键ID")
    ticker: str = Field(..., max_length=50, description="股票代码")
    news_title: str = Field(..., max_length=500, description="新闻标题")
    news_content: str = Field(..., description="新闻内容")
    publish_time: datetime = Field(..., description="发布时间")
    news_source: str = Field(..., max_length=100, description="文章来源")
    news_url: Optional[str] = Field(None, max_length=1000, description="新闻链接")
    sentiment: Optional[str] = Field(None, max_length=20, description="情感分析结果")
    sentiment_score: Optional[float] = Field(None, description="情感分析分数,取值范围[-2, 2]")
    confidence: Optional[str] = Field(None, description="置信度")
    confidence_score: Optional[float] = Field(None, description="置信度分数,取值范围[0, 1]")
    key_factors: Optional[str] = Field(None, description="关键判断依据")
    market_impact: Optional[str] = Field(None, description="市场影响, 重大/中等/轻微/无")
    impact_reason: Optional[str] = Field(None, description="影响原因说明")
    is_deleted: Optional[bool] = Field(False, description="是否删除")
    created_at: Optional[datetime] = Field(None, description="创建时间")
    updated_at: Optional[datetime] = Field(None, description="更新时间")
    is_deleted: bool
    
    class Config:
        # 启用 ORM 模式，便于与 SQLAlchemy 等 ORM 框架集成
        from_attributes = True
        # 允许使用字段别名
        populate_by_name = True
        # JSON 编码配置
        json_encoders = {
            datetime: lambda v: v.isoformat()  # 时间格式化
        }
    
    def __str__(self) -> str:
        return f"CompanyNewsData(ticker={self.ticker}, title={self.news_title[:50]}...)"
    
    def __repr__(self) -> str:
        return self.__str__()
    
    @property
    def content_summary(self) -> str:
        """获取新闻内容摘要（前100个字符）"""
        return self.news_content[:100] + "..." if len(self.news_content) > 100 else self.news_content
    
    @property
    def is_today_news(self) -> bool:
        """判断是否为今日新闻"""
        if not self.publish_time:
            return False
        today = datetime.now().date()
        return self.publish_time.date() == today
    
    def get_formatted_publish_time(self, format_str: str = "%Y-%m-%d %H:%M:%S") -> str:
        """获取格式化的发布时间
        
        Args:
            format_str: 时间格式字符串，默认为 "%Y-%m-%d %H:%M:%S"
            
        Returns:
            str: 格式化后的时间字符串
        """
        return self.publish_time.strftime(format_str)
    
    def contains_ticker_in_content(self, ticker: str) -> bool:
        """检查新闻内容是否包含指定关键词
        
        Args:
            ticker: 要搜索的关键词
            
        Returns:
            bool: 是否包含关键词
        """
        return ticker.lower() in self.news_content.lower()
    
    def get_domain_from_url(self) -> Optional[str]:
        """从新闻链接中提取域名
        
        Returns:
            Optional[str]: 域名，如果没有链接则返回 None
        """
        if not self.news_url:
            return None
        
        try:
            from urllib.parse import urlparse
            parsed_url = urlparse(self.news_url)
            return parsed_url.netloc
        except Exception:
            return None
import psycopg2
from psycopg2.extras import RealDictCursor
from typing import List, Optional, Dict, Any
from datetime import datetime, date

class CompanyNewsDB:
    """公司新闻信息数据库操作类"""
    
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
    
    def insert(self, news_data: CompanyNewsData) -> int:
        """插入一条新闻记录
        
        Args:
            news_data: CompanyNewsData 实例
            
        Returns:
            int: 插入记录的 ID
        """
        sql = """
        INSERT INTO tb_company_news (
            ticker, news_title, news_content, publish_time, news_source, news_url,
            sentiment, sentiment_score, confidence, confidence_score, key_factors,
            market_impact, impact_reason
        ) VALUES (
            %(ticker)s, %(news_title)s, %(news_content)s, %(publish_time)s, %(news_source)s, %(news_url)s,
            %(sentiment)s, %(sentiment_score)s, %(confidence)s, %(confidence_score)s, %(key_factors)s,
            %(market_impact)s, %(impact_reason)s
        ) RETURNING id
        """
        
        with self.get_cursor() as cursor:
            try:
                cursor.execute(sql, {
                    'ticker': news_data.ticker,
                    'news_title': news_data.news_title,
                    'news_content': news_data.news_content,
                    'publish_time': news_data.publish_time,
                    'news_source': news_data.news_source,
                    'news_url': news_data.news_url,
                    'sentiment': news_data.sentiment,
                    'sentiment_score': news_data.sentiment_score,
                    'confidence': news_data.confidence,
                    'confidence_score': news_data.confidence_score,
                    'key_factors': news_data.key_factors,
                    'market_impact': news_data.market_impact,
                    'impact_reason': news_data.impact_reason
                })
                record_id = cursor.fetchone()[0]
                return record_id
            except Exception as e:
                logging.error(f"Failed to insert news record: {e}")
                raise e
    
    def batch_insert(self, news_data_list: List[CompanyNewsData]) -> List[int]:
        """批量插入新闻记录
        
        Args:
            news_data_list: CompanyNewsData 实例列表
            
        Returns:
            List[int]: 插入记录的 ID 列表
        """
        sql = """
        INSERT INTO tb_company_news (
            ticker, news_title, news_content, publish_time, news_source, news_url,
            sentiment, sentiment_score, confidence, confidence_score, key_factors,
            market_impact, impact_reason
        ) VALUES (
            %(ticker)s, %(news_title)s, %(news_content)s, %(publish_time)s, %(news_source)s, %(news_url)s,
            %(sentiment)s, %(sentiment_score)s, %(confidence)s, %(confidence_score)s, %(key_factors)s,
            %(market_impact)s, %(impact_reason)s
        ) RETURNING id
        """
        
        record_ids = []
        with self.get_cursor() as cursor:
            for news_data in news_data_list:
                try:
                    
                    cursor.execute(sql, {
                        'ticker': news_data.ticker,
                        'news_title': news_data.news_title,
                        'news_content': news_data.news_content,
                        'publish_time': news_data.publish_time,
                        'news_source': news_data.news_source,
                        'news_url': news_data.news_url,
                        'sentiment': news_data.sentiment,
                        'sentiment_score': news_data.sentiment_score,
                        'confidence': news_data.confidence,
                        'confidence_score': news_data.confidence_score,
                        'key_factors': news_data.key_factors,
                        'market_impact': news_data.market_impact,
                        'impact_reason': news_data.impact_reason
                    })
                    record_ids.append(cursor.fetchone()[0])
                except Exception as e:
                    logging.error(f"Failed to insert news record: {e}")
                    raise e
        return record_ids
    
    def select_by_id(self, record_id: int, include_deleted: bool = False) -> Optional[CompanyNewsData]:
        """根据 ID 查询单条记录
        
        Args:
            record_id: 记录 ID
            include_deleted: 是否包含已删除记录，默认False
            
        Returns:
            Optional[Dict[str, Any]]: 查询结果字典，如果未找到返回 None
        """
        sql = "SELECT * FROM tb_company_news WHERE id = %s"
        params = [record_id]
        
        if not include_deleted:
            sql += " AND is_deleted = FALSE"
        
        with self.get_cursor(False) as cursor:
            try:
                cursor.execute(sql, params)
                result = cursor.fetchone()
                return CompanyNewsData(**result) if result else None
            except Exception as e:
                logging.error(f"Failed to select news record by ID: {e}")
                raise e
    
    def select_by_ticker(self, ticker: str, limit: int = 100, offset: int = 0, 
                        include_deleted: bool = False) -> List[CompanyNewsData]:
        """根据股票代码查询记录
        
        Args:
            ticker: 股票代码
            limit: 限制返回数量
            offset: 偏移量
            include_deleted: 是否包含已删除记录，默认False
            
        Returns:
            List[CompanyNewsData]: 查询结果列表
        """
        sql = "SELECT * FROM tb_company_news WHERE ticker = %s"
        params = [ticker]
        
        if not include_deleted:
            sql += " AND is_deleted = FALSE"
        
        sql += " ORDER BY publish_time DESC LIMIT %s OFFSET %s"
        params.extend([limit, offset])
        with self.get_cursor(False) as cursor:
            try:
                cursor.execute(sql, params)
                results = cursor.fetchall()
                return [CompanyNewsData(**result) for result in results]
            except Exception as e:
                logging.error(f"Failed to select news records by ticker: {e}")
                raise e
        
    def select_by_sentiment(self, sentiment: str, limit: int = 100, 
                          include_deleted: bool = False) -> List[CompanyNewsData]:
        """根据情感分析结果查询记录
        Args:
            sentiment: 情感分析结果
            limit: 限制返回数量
            include_deleted: 是否包含已删除记录，默认False
            
        Returns:
            List[Dict[str, Any]]: 查询结果列表
        """
        sql = "SELECT * FROM tb_company_news WHERE sentiment = %s"
        params = [sentiment]
        
        if not include_deleted:
            sql += " AND is_deleted = FALSE"
        
        sql += " ORDER BY publish_time DESC LIMIT %s"
        params.append(limit)
        
        with self.get_cursor(False) as cursor:
            try:
                cursor.execute(sql, params)
                results = cursor.fetchall()
                return [CompanyNewsData(**result) for result in results]
            except Exception as e:
                logging.error(f"Failed to select news records by sentiment: {e}")
                raise e
    
    
    def select_all(self, limit: int = 1000, offset: int = 0, 
                  include_deleted: bool = False) -> List[CompanyNewsData]:
        """查询所有记录
        
        Args:
            limit: 限制返回数量
            offset: 偏移量
            include_deleted: 是否包含已删除记录，默认False
            
        Returns:
            List[Dict[str, Any]]: 查询结果列表
        """
        sql = "SELECT * FROM tb_company_news"
        params = []
        
        if not include_deleted:
            sql += " WHERE is_deleted = FALSE"
        
        sql += " ORDER BY publish_time DESC LIMIT %s OFFSET %s"
        params.extend([limit, offset])
        with self.get_cursor(False) as cursor:
            try:
                cursor.execute(sql, params)
                results = cursor.fetchall()
                return [CompanyNewsData(**result) for result in results]
            except Exception as e:
                logging.error(f"Failed to select all news records: {e}")
                raise e
    
    def update_by_id(self, record_id: int, news_data: CompanyNewsData) -> bool:
        """根据 ID 更新记录
        
        Args:
            record_id: 记录 ID
            news_data: 更新的数据
            
        Returns:
            bool: 更新是否成功
        """
        sql = """
        UPDATE tb_company_news SET
            ticker = %(ticker)s,
            news_title = %(news_title)s,
            news_content = %(news_content)s,
            publish_time = %(publish_time)s,
            news_source = %(news_source)s,
            news_url = %(news_url)s,
            sentiment = %(sentiment)s,
            sentiment_score = %(sentiment_score)s,
            confidence = %(confidence)s,
            confidence_score = %(confidence_score)s,
            key_factors = %(key_factors)s,
            market_impact = %(market_impact)s,
            impact_reason = %(impact_reason)s
        WHERE id = %(id)s AND is_deleted = FALSE
        """
        
        with self.get_cursor() as cursor:
            try:
               
                cursor.execute(sql, {
                    'id': record_id,
                    'ticker': news_data.ticker,
                    'news_title': news_data.news_title,
                    'news_content': news_data.news_content,
                    'publish_time': news_data.publish_time,
                    'news_source': news_data.news_source,
                    'news_url': news_data.news_url,
                    'sentiment': news_data.sentiment,
                    'sentiment_score': news_data.sentiment_score,
                    'confidence': news_data.confidence,
                    'confidence_score': news_data.confidence_score,
                    'key_factors': news_data.key_factors,
                    'market_impact': news_data.market_impact,
                    'impact_reason': news_data.impact_reason
                })
                affected_rows = cursor.rowcount
                return affected_rows > 0
            except Exception as e:
                logging.error(f"Failed to update news record by ID: {e}")
                raise e
    
    def update_sentiment_analysis(self, record_id: int, sentiment: str, sentiment_score: float,
                                confidence: str, confidence_score: float, key_factors: str) -> bool:
        """更新情感分析结果
        
        Args:
            record_id: 记录 ID
            sentiment: 情感分析结果
            sentiment_score: 情感分析分数
            confidence: 置信度
            confidence_score: 置信度分数
            key_factors: 关键判断依据
            
        Returns:
            bool: 更新是否成功
        """
        sql = """
        UPDATE tb_company_news SET
            sentiment = %s,
            sentiment_score = %s,
            confidence = %s,
            confidence_score = %s,
            key_factors = %s
        WHERE id = %s AND is_deleted = FALSE
        """
        with self.get_cursor() as cursor:
            try:
                cursor.execute(sql, (sentiment, sentiment_score, confidence, confidence_score, key_factors, record_id))
                affected_rows = cursor.rowcount
                return affected_rows > 0
            except Exception as e:
                logging.error(f"Failed to update sentiment analysis: {e}")
                raise e
    
    