CREATE TABLE IF NOT EXISTS tb_financial_indicators (
    id SERIAL PRIMARY KEY,
    ticker VARCHAR(20) , -- '股票代码',
    report_date DATE NOT NULL , -- '报告日期',

    -- 每股指标
    diluted_eps DECIMAL(10,4) , -- '摊薄每股收益(元)',
    weighted_eps DECIMAL(10,4) , -- '加权每股收益(元)',
    adjusted_eps DECIMAL(10,4) , -- '每股收益_调整后(元)',
    eps_excluding_non_recurring DECIMAL(10,4) , -- '扣除非经常性损益后的每股收益(元)',
    book_value_per_share_before_adj DECIMAL(10,4) , -- '每股净资产_调整前(元)',
    book_value_per_share_after_adj DECIMAL(10,4) , -- '每股净资产_调整后(元)',
    operating_cash_flow_per_share DECIMAL(10,4) , -- '每股经营性现金流(元)',
    capital_reserve_per_share DECIMAL(10,4) , -- '每股资本公积金(元)',
    retained_earnings_per_share DECIMAL(10,4) , -- '每股未分配利润(元)',
    adjusted_book_value_per_share DECIMAL(10,4) , -- '调整后的每股净资产(元)',

    -- 盈利能力指标
    total_asset_profit_rate DECIMAL(8,4) , -- '总资产利润率(%)',
    main_business_profit_margin DECIMAL(8,4) , -- '主营业务利润率(%)',
    roa DECIMAL(8,4) , -- '总资产净利润率(%)',
    cost_expense_profit_rate DECIMAL(8,4) , -- '成本费用利润率(%)',
    operating_profit_margin DECIMAL(8,4) , -- '营业利润率(%)',
    main_business_cost_rate DECIMAL(8,4) , -- '主营业务成本率(%)',
    net_profit_margin DECIMAL(8,4) , -- '销售净利率(%)',
    equity_return_rate DECIMAL(8,4) , -- '股本报酬率(%)',
    roe DECIMAL(8,4) , -- '净资产报酬率(%)',
    asset_return_rate DECIMAL(8,4) , -- '资产报酬率(%)',
    gross_profit_margin DECIMAL(8,4) , -- '销售毛利率(%)',

    -- 财务结构指标
    three_expense_ratio DECIMAL(8,4) , -- '三项费用比重',
    non_main_business_ratio DECIMAL(8,4) , -- '非主营比重',
    main_profit_ratio DECIMAL(8,4) , -- '主营利润比重',
    dividend_payout_ratio DECIMAL(8,4) , -- '股息发放率(%)',
    investment_return_rate DECIMAL(8,4) , -- '投资收益率(%)',

    -- 绝对金额指标
    main_business_profit DECIMAL(15,2) , -- '主营业务利润(元)',
    net_asset_yield DECIMAL(8,4) , -- '净资产收益率(%)',
    weighted_roe DECIMAL(8,4) , -- '加权净资产收益率(%)',
    net_profit_excluding_non_recurring DECIMAL(15,2) , -- '扣除非经常性损益后的净利润(元)',

    -- 成长能力指标
    main_revenue_growth_rate DECIMAL(8,4) , -- '主营业务收入增长率(%)',
    net_profit_growth_rate DECIMAL(8,4) , -- '净利润增长率(%)',
    net_asset_growth_rate DECIMAL(8,4) , -- '净资产增长率(%)',
    total_asset_growth_rate DECIMAL(8,4) , -- '总资产增长率(%)',

    -- 营运能力指标
    accounts_receivable_turnover DECIMAL(8,4) , -- '应收账款周转率(次)',
    accounts_receivable_days DECIMAL(8,4) , -- '应收账款周转天数(天)',
    inventory_turnover_days DECIMAL(8,4) , -- '存货周转天数(天)',
    inventory_turnover DECIMAL(8,4) , -- '存货周转率(次)',
    fixed_asset_turnover DECIMAL(8,4) , -- '固定资产周转率(次)',
    total_asset_turnover DECIMAL(8,4) , -- '总资产周转率(次)',
    total_asset_turnover_days DECIMAL(10,4) , -- '总资产周转天数(天)',
    current_asset_turnover DECIMAL(8,4) , -- '流动资产周转率(次)',
    current_asset_turnover_days DECIMAL(8,4) , -- '流动资产周转天数(天)',
    equity_turnover DECIMAL(8,4) , -- '股东权益周转率(次)',

    -- 偿债能力指标
    current_ratio DECIMAL(8,4) , -- '流动比率',
    quick_ratio DECIMAL(8,4) , -- '速动比率',
    cash_ratio DECIMAL(8,4) , -- '现金比率(%)',
    interest_coverage_ratio DECIMAL(10,4) , -- '利息支付倍数',
    long_term_debt_to_working_capital DECIMAL(8,4) , -- '长期债务与营运资金比率(%)',
    equity_ratio DECIMAL(8,4) , -- '股东权益比率(%)',
    long_term_debt_ratio DECIMAL(8,4) , -- '长期负债比率(%)',
    equity_to_fixed_asset_ratio DECIMAL(8,4) , -- '股东权益与固定资产比率(%)',
    debt_to_equity_ratio DECIMAL(8,4) , -- '负债与所有者权益比率(%)',
    long_term_asset_to_fund_ratio DECIMAL(8,4) , -- '长期资产与长期资金比率(%)',
    capitalization_ratio DECIMAL(8,4) , -- '资本化比率(%)',
    fixed_asset_net_rate DECIMAL(8,4) , -- '固定资产净值率(%)',
    capital_fixation_ratio DECIMAL(8,4) , -- '资本固定化比率(%)',
    property_ratio DECIMAL(8,4) , -- '产权比率(%)',
    liquidation_value_ratio DECIMAL(8,4) , -- '清算价值比率(%)',
    fixed_asset_ratio DECIMAL(8,4) , -- '固定资产比重(%)',
    debt_to_asset_ratio DECIMAL(8,4) , -- '资产负债率(%)',
    total_assets DECIMAL(15,2) , -- '总资产(元)',

    -- 现金流量指标
    operating_cash_to_revenue_ratio DECIMAL(8,4) , -- '经营现金净流量对销售收入比率(%)',
    operating_cash_to_asset_ratio DECIMAL(8,4) , -- '资产的经营现金流量回报率(%)',
    operating_cash_to_net_profit_ratio DECIMAL(8,4) , -- '经营现金净流量与净利润的比率(%)',
    operating_cash_to_debt_ratio DECIMAL(8,4) , -- '经营现金净流量对负债比率(%)',
    cash_flow_ratio DECIMAL(8,4) , -- '现金流量比率(%)',

    -- 投资相关
    short_term_stock_investment DECIMAL(15,2) , -- '短期股票投资(元)',
    short_term_bond_investment DECIMAL(15,2) , -- '短期债券投资(元)',
    short_term_other_investment DECIMAL(15,2) , -- '短期其它经营性投资(元)',
    long_term_stock_investment DECIMAL(15,2) , -- '长期股票投资(元)',
    long_term_bond_investment DECIMAL(15,2) , -- '长期债券投资(元)',
    long_term_other_investment DECIMAL(15,2) , -- '长期其它经营性投资(元)',

    -- 应收账款账龄分析
    accounts_receivable_within_1y DECIMAL(15,2) , -- '1年以内应收帐款(元)',
    accounts_receivable_1_2y DECIMAL(15,2) , -- '1-2年以内应收帐款(元)',
    accounts_receivable_2_3y DECIMAL(15,2) , -- '2-3年以内应收帐款(元)',
    accounts_receivable_over_3y DECIMAL(15,2) , -- '3年以内应收帐款(元)',

    -- 预付款账龄分析
    prepaid_within_1y DECIMAL(15,2) , -- '1年以内预付货款(元)',
    prepaid_1_2y DECIMAL(15,2) , -- '1-2年以内预付货款(元)',
    prepaid_2_3y DECIMAL(15,2) , -- '2-3年以内预付货款(元)',
    prepaid_over_3y DECIMAL(15,2) , -- '3年以内预付货款(元)',

    -- 其他应收款账龄分析
    other_receivables_within_1y DECIMAL(15,2) , -- '1年以内其它应收款(元)',
    other_receivables_1_2y DECIMAL(15,2) , -- '1-2年以内其它应收款(元)',
    other_receivables_2_3y DECIMAL(15,2) , -- '2-3年以内其它应收款(元)',
    other_receivables_over_3y DECIMAL(15,2) , -- '3年以内其它应收款(元)',

    -- 创建和更新时间
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    is_deleted BOOLEAN DEFAULT FALSE
);

-- 创建索引
CREATE INDEX idx_financial_indicators_date ON tb_financial_indicators(ticker, report_date);
CREATE INDEX idx_financial_indicators_created_at ON tb_financial_indicators(created_at);

-- 添加表注释
COMMENT ON TABLE tb_financial_indicators IS '财务指标表';