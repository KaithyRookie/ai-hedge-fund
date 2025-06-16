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
        
        with self.conn.cursor() as cursor:
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
            self.conn.commit()
            return record_id
    
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
        with self.conn.cursor() as cursor:
            for news_data in news_data_list:
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
            self.conn.commit()
        return record_ids
    
    def select_by_id(self, record_id: int, include_deleted: bool = False) -> Optional[Dict[str, Any]]:
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
        
        with self.conn.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(sql, params)
            result = cursor.fetchone()
            return dict(result) if result else None
    
    def select_by_ticker(self, ticker: str, limit: int = 100, offset: int = 0, 
                        include_deleted: bool = False) -> List[Dict[str, Any]]:
        """根据股票代码查询记录
        
        Args:
            ticker: 股票代码
            limit: 限制返回数量
            offset: 偏移量
            include_deleted: 是否包含已删除记录，默认False
            
        Returns:
            List[Dict[str, Any]]: 查询结果列表
        """
        sql = "SELECT * FROM tb_company_news WHERE ticker = %s"
        params = [ticker]
        
        if not include_deleted:
            sql += " AND is_deleted = FALSE"
        
        sql += " ORDER BY publish_time DESC LIMIT %s OFFSET %s"
        params.extend([limit, offset])
        
        with self.conn.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(sql, params)
            results = cursor.fetchall()
            return [dict(row) for row in results]
    
    def select_by_sentiment(self, sentiment: str, limit: int = 100, 
                          include_deleted: bool = False) -> List[Dict[str, Any]]:
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
        
        with self.conn.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(sql, params)
            results = cursor.fetchall()
            return [dict(row) for row in results]
    
    def select_by_market_impact(self, market_impact: str, limit: int = 100,
                              include_deleted: bool = False) -> List[Dict[str, Any]]:
        """根据市场影响级别查询记录
        
        Args:
            market_impact: 市场影响级别（重大/中等/轻微/无）
            limit: 限制返回数量
            include_deleted: 是否包含已删除记录，默认False
            
        Returns:
            List[Dict[str, Any]]: 查询结果列表
        """
        sql = "SELECT * FROM tb_company_news WHERE market_impact = %s"
        params = [market_impact]
        
        if not include_deleted:
            sql += " AND is_deleted = FALSE"
        
        sql += " ORDER BY publish_time DESC LIMIT %s"
        params.append(limit)
        
        with self.conn.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(sql, params)
            results = cursor.fetchall()
            return [dict(row) for row in results]
    
    def select_by_sentiment_score_range(self, min_score: float, max_score: float, 
                                      limit: int = 100, include_deleted: bool = False) -> List[Dict[str, Any]]:
        """根据情感分析分数范围查询记录
        
        Args:
            min_score: 最小分数
            max_score: 最大分数
            limit: 限制返回数量
            include_deleted: 是否包含已删除记录，默认False
            
        Returns:
            List[Dict[str, Any]]: 查询结果列表
        """
        sql = """
        SELECT * FROM tb_company_news 
        WHERE sentiment_score BETWEEN %s AND %s
        """
        params = [min_score, max_score]
        
        if not include_deleted:
            sql += " AND is_deleted = FALSE"
        
        sql += " ORDER BY sentiment_score DESC, publish_time DESC LIMIT %s"
        params.append(limit)
        
        with self.conn.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(sql, params)
            results = cursor.fetchall()
            return [dict(row) for row in results]
    
    def select_by_confidence_score_range(self, min_score: float, max_score: float, 
                                       limit: int = 100, include_deleted: bool = False) -> List[Dict[str, Any]]:
        """根据置信度分数范围查询记录
        
        Args:
            min_score: 最小置信度分数
            max_score: 最大置信度分数
            limit: 限制返回数量
            include_deleted: 是否包含已删除记录，默认False
            
        Returns:
            List[Dict[str, Any]]: 查询结果列表
        """
        sql = """
        SELECT * FROM tb_company_news 
        WHERE confidence_score BETWEEN %s AND %s
        """
        params = [min_score, max_score]
        
        if not include_deleted:
            sql += " AND is_deleted = FALSE"
        
        sql += " ORDER BY confidence_score DESC, publish_time DESC LIMIT %s"
        params.append(limit)
        
        with self.conn.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(sql, params)
            results = cursor.fetchall()
            return [dict(row) for row in results]
    
    def select_by_date_range(self, start_date: datetime, end_date: datetime, 
                           ticker: Optional[str] = None, include_deleted: bool = False) -> List[Dict[str, Any]]:
        """根据日期范围查询记录
        
        Args:
            start_date: 开始时间
            end_date: 结束时间
            ticker: 可选的股票代码过滤
            include_deleted: 是否包含已删除记录，默认False
            
        Returns:
            List[Dict[str, Any]]: 查询结果列表
        """
        sql = "SELECT * FROM tb_company_news WHERE publish_time BETWEEN %s AND %s"
        params = [start_date, end_date]
        
        if ticker:
            sql += " AND ticker = %s"
            params.append(ticker)
        
        if not include_deleted:
            sql += " AND is_deleted = FALSE"
        
        sql += " ORDER BY publish_time DESC"
        
        with self.conn.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(sql, params)
            results = cursor.fetchall()
            return [dict(row) for row in results]
    
    def select_by_news_source(self, news_source: str, limit: int = 100, 
                            include_deleted: bool = False) -> List[Dict[str, Any]]:
        """根据新闻来源查询记录
        
        Args:
            news_source: 新闻来源
            limit: 限制返回数量
            include_deleted: 是否包含已删除记录，默认False
            
        Returns:
            List[Dict[str, Any]]: 查询结果列表
        """
        sql = "SELECT * FROM tb_company_news WHERE news_source = %s"
        params = [news_source]
        
        if not include_deleted:
            sql += " AND is_deleted = FALSE"
        
        sql += " ORDER BY publish_time DESC LIMIT %s"
        params.append(limit)
        
        with self.conn.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(sql, params)
            results = cursor.fetchall()
            return [dict(row) for row in results]
    
    def search_by_title(self, search_text: str, limit: int = 100, 
                       include_deleted: bool = False) -> List[Dict[str, Any]]:
        """根据标题内容搜索记录
        
        Args:
            search_text: 搜索文本
            limit: 限制返回数量
            include_deleted: 是否包含已删除记录，默认False
            
        Returns:
            List[Dict[str, Any]]: 查询结果列表
        """
        sql = "SELECT * FROM tb_company_news WHERE news_title ILIKE %s"
        params = [f"%{search_text}%"]
        
        if not include_deleted:
            sql += " AND is_deleted = FALSE"
        
        sql += " ORDER BY publish_time DESC LIMIT %s"
        params.append(limit)
        
        with self.conn.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(sql, params)
            results = cursor.fetchall()
            return [dict(row) for row in results]
    
    def full_text_search(self, search_text: str, limit: int = 100, 
                        include_deleted: bool = False) -> List[Dict[str, Any]]:
        """全文搜索（标题和内容）
        
        Args:
            search_text: 搜索文本
            limit: 限制返回数量
            include_deleted: 是否包含已删除记录，默认False
            
        Returns:
            List[Dict[str, Any]]: 查询结果列表
        """
        sql = """
        SELECT *, 
               ts_rank(to_tsvector('chinese', news_title || ' ' || news_content), 
                      plainto_tsquery('chinese', %s)) as rank
        FROM tb_company_news 
        WHERE to_tsvector('chinese', news_title || ' ' || news_content) @@ plainto_tsquery('chinese', %s)
        """
        params = [search_text, search_text]
        
        if not include_deleted:
            sql += " AND is_deleted = FALSE"
        
        sql += " ORDER BY rank DESC, publish_time DESC LIMIT %s"
        params.append(limit)
        
        with self.conn.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(sql, params)
            results = cursor.fetchall()
            return [dict(row) for row in results]
    
    def select_high_impact_news(self, ticker: Optional[str] = None, days: int = 7,
                              include_deleted: bool = False) -> List[Dict[str, Any]]:
        """查询高影响力新闻（重大市场影响）
        
        Args:
            ticker: 可选的股票代码过滤
            days: 查询最近几天的新闻，默认7天
            include_deleted: 是否包含已删除记录，默认False
            
        Returns:
            List[Dict[str, Any]]: 查询结果列表
        """
        sql = """
        SELECT * FROM tb_company_news 
        WHERE market_impact = '重大' 
        AND publish_time >= CURRENT_TIMESTAMP - INTERVAL '%s days'
        """
        params = [days]
        
        if ticker:
            sql += " AND ticker = %s"
            params.append(ticker)
        
        if not include_deleted:
            sql += " AND is_deleted = FALSE"
        
        sql += " ORDER BY publish_time DESC"
        
        with self.conn.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(sql, params)
            results = cursor.fetchall()
            return [dict(row) for row in results]
    
    def select_latest_by_ticker(self, ticker: str, days: int = 7, 
                              include_deleted: bool = False) -> List[Dict[str, Any]]:
        """获取指定股票代码最近几天的新闻
        
        Args:
            ticker: 股票代码
            days: 天数，默认7天
            include_deleted: 是否包含已删除记录，默认False
            
        Returns:
            List[Dict[str, Any]]: 查询结果列表
        """
        sql = """
        SELECT * FROM tb_company_news 
        WHERE ticker = %s 
        AND publish_time >= CURRENT_TIMESTAMP - INTERVAL '%s days'
        """
        params = [ticker, days]
        
        if not include_deleted:
            sql += " AND is_deleted = FALSE"
        
        sql += " ORDER BY publish_time DESC"
        
        with self.conn.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(sql, params)
            results = cursor.fetchall()
            return [dict(row) for row in results]
    
    def select_all(self, limit: int = 1000, offset: int = 0, 
                  include_deleted: bool = False) -> List[Dict[str, Any]]:
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
        
        with self.conn.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(sql, params)
            results = cursor.fetchall()
            return [dict(row) for row in results]
    
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
        
        with self.conn.cursor() as cursor:
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
            self.conn.commit()
            return affected_rows > 0
    
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
        
        with self.conn.cursor() as cursor:
            cursor.execute(sql, (sentiment, sentiment_score, confidence, 
                               confidence_score, key_factors, record_id))
            affected_rows = cursor.rowcount
            self.conn.commit()
            return affected_rows > 0
    
    def update_market_impact(self, record_id: int, market_impact: str, impact_reason: str) -> bool:
        """更新市场影响评估
        
        Args:
            record_id: 记录 ID
            market_impact: 市场影响级别
            impact_reason: 影响原因说明
            
        Returns:
            bool: 更新是否成功
        """
        sql = """
        UPDATE tb_company_news SET
            market_impact = %s,
            impact_reason = %s
        WHERE id = %s AND is_deleted = FALSE
        """
        
        with self.conn.cursor() as cursor:
            cursor.execute(sql, (market_impact, impact_reason, record_id))
            affected_rows = cursor.rowcount
            self.conn.commit()
            return affected_rows > 0
    
    def soft_delete_by_id(self, record_id: int) -> bool:
        """软删除记录（标记为已删除）
        
        Args:
            record_id: 记录 ID
            
        Returns:
            bool: 删除是否成功
        """
        sql = "UPDATE tb_company_news SET is_deleted = TRUE WHERE id = %s"
        
        with self.conn.cursor() as cursor:
            cursor.execute(sql, (record_id,))
            affected_rows = cursor.rowcount
            self.conn.commit()
            return affected_rows > 0
    
    def restore_by_id(self, record_id: int) -> bool:
        """恢复已删除的记录
        
        Args:
            record_id: 记录 ID
            
        Returns:
            bool: 恢复是否成功
        """
        sql = "UPDATE tb_company_news SET is_deleted = FALSE WHERE id = %s"
        
        with self.conn.cursor() as cursor:
            cursor.execute(sql, (record_id,))
            affected_rows = cursor.rowcount
            self.conn.commit()
            return affected_rows > 0
    
    def hard_delete_by_id(self, record_id: int) -> bool:
        """物理删除记录
        
        Args:
            record_id: 记录 ID
            
        Returns:
            bool: 删除是否成功
        """
        sql = "DELETE FROM tb_company_news WHERE id = %s"
        
        with self.conn.cursor() as cursor:
            cursor.execute(sql, (record_id,))
            affected_rows = cursor.rowcount
            self.conn.commit()
            return affected_rows > 0
    
    def soft_delete_by_ticker(self, ticker: str) -> int:
        """软删除指定股票代码的所有记录
        
        Args:
            ticker: 股票代码
            
        Returns:
            int: 删除的记录数量
        """
        sql = "UPDATE tb_company_news SET is_deleted = TRUE WHERE ticker = %s AND is_deleted = FALSE"
        
        with self.conn.cursor() as cursor:
            cursor.execute(sql, (ticker,))
            affected_rows = cursor.rowcount
            self.conn.commit()
            return affected_rows
    
    def delete_old_news(self, days: int = 365, hard_delete: bool = False) -> int:
        """删除指定天数之前的旧新闻
        
        Args:
            days: 保留天数，超过这个天数的新闻将被删除
            hard_delete: 是否物理删除，默认为软删除
            
        Returns:
            int: 删除的记录数量
        """
        if hard_delete:
            sql = """
            DELETE FROM tb_company_news 
            WHERE publish_time < CURRENT_TIMESTAMP - INTERVAL '%s days'
            """
        else:
            sql = """
            UPDATE tb_company_news SET is_deleted = TRUE
            WHERE publish_time < CURRENT_TIMESTAMP - INTERVAL '%s days'
            AND is_deleted = FALSE
            """
        
        with self.conn.cursor() as cursor:
            cursor.execute(sql, (days,))
            affected_rows = cursor.rowcount
            self.conn.commit()
            return affected_rows
    
    def count_total(self, include_deleted: bool = False) -> int:
        """统计总记录数
        
        Args:
            include_deleted: 是否包含已删除记录，默认False
            
        Returns:
            int: 总记录数
        """
        sql = "SELECT COUNT(*) FROM tb_company_news"
        
        if not include_deleted:
            sql += " WHERE is_deleted = FALSE"
        
        with self.conn.cursor() as cursor:
            cursor.execute(sql)
            return cursor.fetchone()[0]
    
    def count_by_ticker(self, ticker: str, include_deleted: bool = False) -> int:
        """统计指定股票代码的记录数
        
        Args:
            ticker: 股票代码
            include_deleted: 是否包含已删除记录，默认False
            
        Returns:
            int: 记录数
        """
        sql = "SELECT COUNT(*) FROM tb_company_news WHERE ticker = %s"
        params = [ticker]
        
        if not include_deleted:
            sql += " AND is_deleted = FALSE"
        
        with self.conn.cursor() as cursor:
            cursor.execute(sql, params)
            return cursor.fetchone()[0]
    
    def count_by_sentiment(self, sentiment: str, include_deleted: bool = False) -> int:
        """统计指定情感分析结果的记录数
        
        Args:
            sentiment: 情感分析结果
            include_deleted: 是否包含已删除记录，默认False
            
        Returns:
            int: 记录数
        """
        sql = "SELECT COUNT(*) FROM tb_company_news WHERE sentiment = %s"
        params = [sentiment]
        
        if not include_deleted:
            sql += " AND is_deleted = FALSE"
        
        with self.conn.cursor() as cursor:
            cursor.execute(sql, params)
            return cursor.fetchone()[0]
    
    def count_by_market_impact(self, market_impact: str, include_deleted: bool = False) -> int:
        """统计指定市场影响级别的记录数
        
        Args:
            market_impact: 市场影响级别
            include_deleted: 是否包含已删除记录，默认False
            
        Returns:
            int: 记录数
        """
        sql = "SELECT COUNT(*) FROM tb_company_news WHERE market_impact = %s"
        params = [market_impact]
        
        if not include_deleted:
            sql += " AND is_deleted = FALSE"
        
        with self.conn.cursor() as cursor:
            cursor.execute(sql, params)
            return cursor.fetchone()[0]
    
    def get_ticker_statistics(self, include_deleted: bool = False) -> List[Dict[str, Any]]:
        """获取股票代码统计信息
        
        Args:
            include_deleted: 是否包含已删除记录，默认False
            
        Returns:
            List[Dict[str, Any]]: 股票代码统计结果
        """
        sql = """
        SELECT ticker, COUNT(*) as news_count, 
               MAX(publish_time) as latest_news_time,
               MIN(publish_time) as earliest_news_time,
               AVG(sentiment_score) as avg_sentiment_score,
               COUNT(CASE WHEN market_impact = '重大' THEN 1 END) as high_impact_count
        FROM tb_company_news
        """
        
        if not include_deleted:
            sql += " WHERE is_deleted = FALSE"
        
        sql += " GROUP BY ticker ORDER BY news_count DESC"
        
        with self.conn.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(sql)
            results = cursor.fetchall()
            return [dict(row) for row in results]
    
    def get_sentiment_statistics(self, include_deleted: bool = False) -> List[Dict[str, Any]]:
        """获取情感分析统计信息
        
        Args:
            include_deleted: 是否包含已删除记录，默认False
            
        Returns:
            List[Dict[str, Any]]: 情感分析统计结果
        """
        sql = """
        SELECT sentiment, COUNT(*) as count,
               AVG(sentiment_score) as avg_score,
               MIN(sentiment_score) as min_score,
               MAX(sentiment_score) as max_score
        FROM tb_company_news 
        WHERE sentiment IS NOT NULL
        """
        
        if not include_deleted:
            sql += " AND is_deleted = FALSE"
        
        sql += " GROUP BY sentiment ORDER BY count DESC"
        
        with self.conn.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(sql)
            results = cursor.fetchall()
            return [dict(row) for row in results]
    
    def get_market_impact_statistics(self, include_deleted: bool = False) -> List[Dict[str, Any]]:
        """获取市场影响统计信息
        
        Args:
            include_deleted: 是否包含已删除记录，默认False
            
        Returns:
            List[Dict[str, Any]]: 市场影响统计结果
        """
        sql = """
        SELECT market_impact, COUNT(*) as count,
               COUNT(*) * 100.0 / SUM(COUNT(*)) OVER() as percentage
        FROM tb_company_news 
        WHERE market_impact IS NOT NULL
        """
        
        if not include_deleted:
            sql += " AND is_deleted = FALSE"
        
        sql += " GROUP BY market_impact ORDER BY count DESC"
        
        with self.conn.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(sql)
            results = cursor.fetchall()
            return [dict(row) for row in results]
    
    def check_news_exists(self, news_title: str, news_source: str, 
                         include_deleted: bool = False) -> bool:
        """检查新闻是否已存在（基于标题和来源）
        
        Args:
            news_title: 新闻标题
            news_source: 新闻来源
            include_deleted: 是否包含已删除记录，默认False
            
        Returns:
            bool: 是否存在
        """
        sql = "SELECT 1 FROM tb_company_news WHERE news_title = %s AND news_source = %s"
        params = [news_title, news_source]
        
        if not include_deleted:
            sql += " AND is_deleted = FALSE"
        
        sql += " LIMIT 1"
        
        with self.conn.cursor() as cursor:
            cursor.execute(sql, params)
            return cursor.fetchone() is not None
    
    def get_news_trend_by_ticker(self, ticker: str, days: int = 30, 
                               include_deleted: bool = False) -> List[Dict[str, Any]]:
        """获取指定股票代码的新闻趋势（按日期统计）
        
        Args:
            ticker: 股票代码
            days: 统计最近几天，默认30天
            include_deleted: 是否包含已删除记录，默认False
            
        Returns:
            List[Dict[str, Any]]: 新闻趋势统计结果
        """
        sql = """
        SELECT DATE(publish_time) as news_date,
               COUNT(*) as news_count,
               AVG(sentiment_score) as avg_sentiment_score,
               COUNT(CASE WHEN market_impact IN ('重大', '中等') THEN 1 END) as important_news_count
        FROM tb_company_news 
        WHERE ticker = %s 
        AND publish_time >= CURRENT_TIMESTAMP - INTERVAL '%s days'
        """
        params = [ticker, days]
        
        if not include_deleted:
            sql += " AND is_deleted = FALSE"
        
        sql += " GROUP BY DATE(publish_time) ORDER BY news_date DESC"
        
        with self.conn.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(sql, params)
            results = cursor.fetchall()
            return [dict(row) for row in results]