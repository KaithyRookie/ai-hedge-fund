CREATE TABLE tb_company_news (
    id SERIAL PRIMARY KEY,
    ticker VARCHAR(50) NOT NULL,
    news_title VARCHAR(500) NOT NULL,
    news_content TEXT NOT NULL,
    publish_time TIMESTAMP NOT NULL,
    news_source VARCHAR(100) NOT NULL,
    news_url VARCHAR(1000),
    sentiment VARCHAR(20),
    sentiment_score NUMERIC(3,2) CHECK (sentiment_score >= -2 AND sentiment_score <= 2),
    confidence VARCHAR(50),
    confidence_score NUMERIC(3,2) CHECK (confidence_score >= 0 AND confidence_score <= 1),
    key_factors TEXT,
    market_impact VARCHAR(20) CHECK (market_impact IN ('重大', '中等', '轻微', '无') OR market_impact IS NULL),
    impact_reason TEXT,
    is_deleted BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 创建索引以提高查询性能
CREATE INDEX idx_tb_company_news_ticker ON tb_company_news(ticker);
CREATE INDEX idx_tb_company_news_publish_time ON tb_company_news(publish_time);
CREATE INDEX idx_tb_company_news_news_source ON tb_company_news(news_source);
CREATE INDEX idx_tb_company_news_sentiment ON tb_company_news(sentiment);
CREATE INDEX idx_tb_company_news_market_impact ON tb_company_news(market_impact);
CREATE INDEX idx_tb_company_news_is_deleted ON tb_company_news(is_deleted);
CREATE INDEX idx_tb_company_news_title ON tb_company_news USING gin(to_tsvector('chinese', news_title));
CREATE INDEX idx_tb_company_news_content ON tb_company_news USING gin(to_tsvector('chinese', news_content));

-- 创建复合索引
CREATE INDEX idx_tb_company_news_ticker_time ON tb_company_news(ticker, publish_time DESC);
CREATE INDEX idx_tb_company_news_ticker_sentiment ON tb_company_news(ticker, sentiment);
CREATE INDEX idx_tb_company_news_active_news ON tb_company_news(ticker, publish_time DESC) WHERE is_deleted = FALSE;

-- 创建更新时间自动更新的触发器
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER update_tb_company_news_updated_at 
    BEFORE UPDATE ON tb_company_news 
    FOR EACH ROW 
    EXECUTE FUNCTION update_updated_at_column();

-- 添加表注释
COMMENT ON TABLE tb_company_news IS '公司新闻信息表';

-- 添加字段注释
COMMENT ON COLUMN tb_company_news.id IS '主键ID';
COMMENT ON COLUMN tb_company_news.ticker IS '股票代码';
COMMENT ON COLUMN tb_company_news.news_title IS '新闻标题';
COMMENT ON COLUMN tb_company_news.news_content IS '新闻内容';
COMMENT ON COLUMN tb_company_news.publish_time IS '发布时间';
COMMENT ON COLUMN tb_company_news.news_source IS '文章来源';
COMMENT ON COLUMN tb_company_news.news_url IS '新闻链接';
COMMENT ON COLUMN tb_company_news.sentiment IS '情感分析结果';
COMMENT ON COLUMN tb_company_news.sentiment_score IS '情感分析分数,取值范围[-2, 2]';
COMMENT ON COLUMN tb_company_news.confidence IS '置信度';
COMMENT ON COLUMN tb_company_news.confidence_score IS '置信度分数,取值范围[0, 1]';
COMMENT ON COLUMN tb_company_news.key_factors IS '关键判断依据';
COMMENT ON COLUMN tb_company_news.market_impact IS '市场影响, 重大/中等/轻微/无';
COMMENT ON COLUMN tb_company_news.impact_reason IS '影响原因说明';
COMMENT ON COLUMN tb_company_news.is_deleted IS '是否删除';
COMMENT ON COLUMN tb_company_news.created_at IS '创建时间';
COMMENT ON COLUMN tb_company_news.updated_at IS '更新时间';

-- 创建视图：仅显示未删除的新闻
CREATE VIEW v_active_company_news AS
SELECT * FROM tb_company_news 
WHERE is_deleted = FALSE;

-- 添加视图注释
COMMENT ON VIEW v_active_company_news IS '活跃新闻视图（未删除的新闻）';