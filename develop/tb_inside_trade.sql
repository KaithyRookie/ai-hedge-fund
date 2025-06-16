CREATE TABLE tb_inside_trade (
    id SERIAL PRIMARY KEY,
    stock_code VARCHAR(20) NOT NULL , -- COMMENT '股票代码',
    stock_name VARCHAR(100) NOT NULL , -- COMMENT '股票名称',
    change_date DATE NOT NULL , -- COMMENT '变动日期',
    change_person VARCHAR(50) NOT NULL , -- COMMENT '变动人',
    change_shares BIGINT NOT NULL , -- COMMENT '变动股数',
    avg_price DECIMAL(10,2) NOT NULL , -- COMMENT '成交均价',
    shares_after_change DECIMAL(15,1) NOT NULL , -- COMMENT '变动后持股数',
    relation_to_executive VARCHAR(100) , -- COMMENT '与董监高关系',
    executive_position VARCHAR(100) , -- COMMENT '董监高职务',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP , -- COMMENT '创建时间',
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP , -- COMMENT '更新时间',
    is_deleted BOOLEAN DEFAULT FALSE -- COMMENT '是否删除'
);

-- 创建索引以提高查询性能
CREATE INDEX idx_tb_inside_trade_stock_code ON tb_inside_trade(stock_code);
CREATE INDEX idx_tb_inside_trade_change_date ON tb_inside_trade(change_date);
CREATE INDEX idx_tb_inside_trade_change_person ON tb_inside_trade(change_person);

-- 添加表注释
COMMENT ON TABLE tb_inside_trade IS '内部交易记录表';