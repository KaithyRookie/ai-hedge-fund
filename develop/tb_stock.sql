CREATE TABLE IF NOT EXISTS tb_stock (
    id SERIAL PRIMARY KEY,  -- 序号
    serial_number INTEGER,  -- 序号
    ticker VARCHAR NOT NULL,  -- 代码
    ticker_name VARCHAR NOT NULL,  -- 名称
    stock_type VARCHAR,  -- 类型
    created_at TIMESTAMP,
    updated_at TIMESTAMP,
    is_deleted BOOLEAN DEFAULT FALSE
);

CREATE INDEX idx_tb_stock_ticker ON tb_stock (ticker, ticker_name);
CREATE INDEX idx_stock_type ON tb_stock (ticker, stock_type);