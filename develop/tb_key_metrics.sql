-- 创建 tb_key_metrics 表
CREATE TABLE IF NOT EXISTS tb_key_metrics (
    id SERIAL PRIMARY KEY,  -- 自增主键
    ticker VARCHAR(10) NOT NULL,  -- 股票代码
    report_date DATE NOT NULL,  -- 报告日期
    parent_company_net_profit NUMERIC(20, 2),  -- 归母净利润
    total_operating_revenue NUMERIC(20, 2),  -- 营业总收入
    operating_cost NUMERIC(20, 2),  -- 营业成本
    net_profit NUMERIC(20, 2),  -- 净利润
    non_recurring_profit NUMERIC(20, 2),  -- 扣非净利润
    total_shareholders_equity NUMERIC(20, 2),  -- 股东权益合计(净资产)
    goodwill NUMERIC(20, 2),  -- 商誉
    net_operating_cash_flow NUMERIC(20, 2),  -- 经营现金流量净额
    basic_eps NUMERIC(10, 6),  -- 基本每股收益
    net_assets_per_share NUMERIC(10, 6),  -- 每股净资产
    cash_flow_per_share NUMERIC(10, 6),  -- 每股现金流
    roe NUMERIC(10, 6),  -- 净资产收益率(ROE)
    roa NUMERIC(10, 6),  -- 总资产报酬率(ROA)
    gross_margin NUMERIC(10, 6),  -- 毛利率
    net_profit_margin NUMERIC(10, 6),  -- 销售净利率
    period_expense_ratio NUMERIC(10, 6),  -- 期间费用率
    asset_liability_ratio NUMERIC(10, 6),  -- 资产负债率
    diluted_eps NUMERIC(10, 6),  -- 稀释每股收益
    diluted_net_assets_per_share NUMERIC(10, 6),  -- 摊薄每股净资产_期末股数
    adjusted_net_assets_per_share NUMERIC(10, 6),  -- 调整每股净资产_期末股数
    net_assets_per_share_new NUMERIC(10, 6),  -- 每股净资产_最新股数
    operating_cash_flow_per_share NUMERIC(10, 6),  -- 每股经营现金流
    net_cash_flow_per_share NUMERIC(10, 6),  -- 每股现金流量净额
    enterprise_fcf_per_share NUMERIC(10, 6),  -- 每股企业自由现金流量
    shareholder_fcf_per_share NUMERIC(10, 6),  -- 每股股东自由现金流量
    undistributed_profit_per_share NUMERIC(10, 6),  -- 每股未分配利润
    capital_reserve_per_share NUMERIC(10, 6),  -- 每股资本公积金
    surplus_reserve_per_share NUMERIC(10, 6),  -- 每股盈余公积金
    retained_earnings_per_share NUMERIC(10, 6),  -- 每股留存收益
    operating_revenue_per_share NUMERIC(10, 6),  -- 每股营业收入
    total_operating_revenue_per_share NUMERIC(10, 6),  -- 每股营业总收入
    ebit_per_share NUMERIC(10, 6),  -- 每股息税前利润
    diluted_roe NUMERIC(10, 6),  -- 摊薄净资产收益率
    average_roe NUMERIC(10, 6),  -- 净资产收益率_平均
    average_roe_non_recurring NUMERIC(10, 6),  -- 净资产收益率_平均_扣除非经常损益
    diluted_roe_non_recurring NUMERIC(10, 6),  -- 摊薄净资产收益率_扣除非经常损益
    ebit_margin NUMERIC(10, 6),  -- 息税前利润率
    total_capital_return NUMERIC(10, 6),  -- 总资本回报率
    invested_capital_return NUMERIC(10, 6),  -- 投入资本回报率
    after_tax_roa NUMERIC(10, 6),  -- 息前税后总资产报酬率_平均
    cost_profit_ratio NUMERIC(10, 6),  -- 成本费用利润率
    operating_profit_margin NUMERIC(10, 6),  -- 营业利润率
    average_asset_net_profit_rate NUMERIC(10, 6),  -- 总资产净利率_平均
    average_asset_net_profit_rate_minority NUMERIC(10, 6),  -- 总资产净利率_平均(含少数股东损益)
    operating_revenue_growth_rate NUMERIC(10, 6),  -- 营业总收入增长率
    parent_company_net_profit_growth_rate NUMERIC(10, 6),  -- 归属母公司净利润增长率
    operating_cash_sales_ratio NUMERIC(10, 6),  -- 经营活动净现金/销售收入
    operating_cash_total_revenue_ratio NUMERIC(10, 6),  -- 经营性现金净流量/营业总收入
    cost_expense_ratio NUMERIC(10, 6),  -- 成本费用率
    sales_cost_ratio NUMERIC(10, 6),  -- 销售成本率
    operating_cash_parent_profit_ratio NUMERIC(10, 6),  -- 经营活动净现金/归属母公司的净利润
    income_tax_profit_ratio NUMERIC(10, 6),  -- 所得税/利润总额
    current_ratio NUMERIC(10, 6),  -- 流动比率
    quick_ratio NUMERIC(10, 6),  -- 速动比率
    conservative_quick_ratio NUMERIC(10, 6),  -- 保守速动比率
    equity_multiplier NUMERIC(10, 6),  -- 权益乘数
    equity_multiplier_minority NUMERIC(10, 6),  -- 权益乘数(含少数股权的净资产)
    equity_debt_ratio NUMERIC(10, 6),  -- 产权比率
    cash_ratio NUMERIC(10, 6),  -- 现金比率
    accounts_receivable_turnover NUMERIC(10, 6),  -- 应收账款周转率
    accounts_receivable_days NUMERIC(10, 6),  -- 应收账款周转天数
    inventory_turnover NUMERIC(10, 6),  -- 存货周转率
    inventory_days NUMERIC(10, 6),  -- 存货周转天数
    total_asset_turnover NUMERIC(10, 6),  -- 总资产周转率
    total_asset_days NUMERIC(10, 6),  -- 总资产周转天数
    current_asset_turnover NUMERIC(10, 6),  -- 流动资产周转率
    current_asset_days NUMERIC(10, 6),  -- 流动资产周转天数
    accounts_payable_turnover NUMERIC(10, 6),  -- 应付账款周转率
    ebitbd NUMERIC(10, 6),  -- 息税前利润(EBITDA)
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP, -- '创建时间'
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP, -- '更新时间'
    is_deleted BOOLEAN DEFAULT FALSE -- '是否删除'
);

CREATE INDEX IF NOT EXISTS idx_ticker_report_date ON tb_key_metrics (ticker, report_date);