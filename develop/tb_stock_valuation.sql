-- 创建 tb_stock_valuation 表
CREATE TABLE IF NOT EXISTS tb_stock_valuation (
    id SERIAL PRIMARY KEY,  -- 自增主键
    ticker VARCHAR(10) NOT NULL,  -- 股票ticker
    data_date DATE NOT NULL,  -- 数据日期
    closing_price DECIMAL(15, 2),  -- 当日收盘价
    daily_change DECIMAL(15, 6),  -- 当日涨跌幅
    market_cap DECIMAL(20, 2),  -- 总市值
    flow_market_cap DECIMAL(20, 2),  -- 流通市值
    total_share BIGINT,  -- 总股本
    float_share BIGINT,  -- 流通股本
    pe_ttm_ratio DECIMAL(15, 8),  -- PE(TTM)
    pe_static_ratio DECIMAL(15, 8),  -- PE(静)
    pb_ratio DECIMAL(15, 8),  -- 市净率
    peg_ratio DECIMAL(15, 8),  -- PEG值
    pc_ratio DECIMAL(15, 8),  -- 市现率
    ps_ratio DECIMAL(15, 8),  -- 市销率
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP, -- '创建时间'
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP, -- '更新时间'
    is_deleted BOOLEAN DEFAULT FALSE -- '是否删除'
);

CREATE INDEX IF NOT EXISTS idx_ticker_data_date ON tb_stock_valuation (ticker, data_date);