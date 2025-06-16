CREATE TABLE tb_financial_metric (
    id SERIAL PRIMARY KEY,
    ticker VARCHAR(20) NOT NULL,
    report_period VARCHAR(50) NOT NULL,
    period VARCHAR(20) NOT NULL,
    currency VARCHAR(10) NOT NULL,
    market_cap DECIMAL(20,2),
    enterprise_value DECIMAL(20,2),
    price_to_earnings_ratio DECIMAL(10,4),
    price_to_book_ratio DECIMAL(10,4),
    price_to_sales_ratio DECIMAL(10,4),
    enterprise_value_to_ebitda_ratio DECIMAL(10,4),
    enterprise_value_to_revenue_ratio DECIMAL(10,4),
    free_cash_flow_yield DECIMAL(10,4),
    peg_ratio DECIMAL(10,4),
    gross_margin DECIMAL(10,4),
    operating_margin DECIMAL(10,4),
    net_margin DECIMAL(10,4),
    return_on_equity DECIMAL(10,4),
    return_on_assets DECIMAL(10,4),
    return_on_invested_capital DECIMAL(10,4),
    asset_turnover DECIMAL(10,4),
    inventory_turnover DECIMAL(10,4),
    receivables_turnover DECIMAL(10,4),
    days_sales_outstanding DECIMAL(10,2),
    operating_cycle DECIMAL(10,2),
    working_capital_turnover DECIMAL(10,4),
    current_ratio DECIMAL(10,4),
    quick_ratio DECIMAL(10,4),
    cash_ratio DECIMAL(10,4),
    operating_cash_flow_ratio DECIMAL(10,4),
    debt_to_equity DECIMAL(10,4),
    debt_to_assets DECIMAL(10,4),
    interest_coverage DECIMAL(10,4),
    revenue_growth DECIMAL(10,4),
    earnings_growth DECIMAL(10,4),
    book_value_growth DECIMAL(10,4),
    earnings_per_share_growth DECIMAL(10,4),
    free_cash_flow_growth DECIMAL(10,4),
    operating_income_growth DECIMAL(10,4),
    ebitda_growth DECIMAL(10,4),
    payout_ratio DECIMAL(10,4),
    earnings_per_share DECIMAL(10,4),
    book_value_per_share DECIMAL(10,4),
    free_cash_flow_per_share DECIMAL(10,4),
    fcff_per_share DECIMAL(10,4),
    fcfe_per_share DECIMAL(10,4),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    is_deleted BOOLEAN DEFAULT FALSE -- '是否删除'
);

-- 创建索引以提高查询性能
CREATE INDEX idx_tb_financial_metric_ticker ON tb_financial_metric(ticker);
CREATE INDEX idx_tb_financial_metric_period ON tb_financial_metric(report_period);
CREATE INDEX idx_tb_financial_metric_ticker_period ON tb_financial_metric(ticker, report_period);

-- 创建更新时间触发器
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER update_tb_financial_metric_updated_at 
    BEFORE UPDATE ON tb_financial_metric 
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();