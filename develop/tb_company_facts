CREATE TABLE tb_company_facts (
    id SERIAL PRIMARY KEY,
    company_name VARCHAR(255) NOT NULL COMMENT '公司名称',
    company_name_en VARCHAR(255) COMMENT '英文名称',
    former_short_name VARCHAR(255) COMMENT '曾用简称',
    a_share_code VARCHAR(20) COMMENT 'A股代码',
    a_share_name VARCHAR(100) COMMENT 'A股简称',
    b_share_code VARCHAR(20) COMMENT 'B股代码',
    b_share_name VARCHAR(100) COMMENT 'B股简称',
    h_share_code VARCHAR(20) COMMENT 'H股代码',
    h_share_name VARCHAR(100) COMMENT 'H股简称',
    selected_indices TEXT COMMENT '入选指数',
    market_category VARCHAR(100) COMMENT '所属市场',
    industry_category VARCHAR(100) COMMENT '所属行业',
    legal_representative VARCHAR(100) COMMENT '法人代表',
    registered_capital DECIMAL(15,4) COMMENT '注册资金',
    establishment_date DATE COMMENT '成立日期',
    listing_date DATE COMMENT '上市日期',
    official_website VARCHAR(255) COMMENT '官方网站',
    email VARCHAR(255) COMMENT '电子邮箱',
    contact_phone VARCHAR(50) COMMENT '联系电话',
    fax VARCHAR(50) COMMENT '传真',
    registered_address TEXT COMMENT '注册地址',
    office_address TEXT COMMENT '办公地址',
    postal_code VARCHAR(20) COMMENT '邮政编码',
    main_business TEXT COMMENT '主营业务',
    business_scope TEXT COMMENT '经营范围',
    company_profile TEXT COMMENT '机构简介',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 创建索引以提高查询性能
CREATE INDEX idx_company_name ON tb_company_facts(company_name);
CREATE INDEX idx_a_share_code ON tb_company_facts(a_share_code);
CREATE INDEX idx_h_share_code ON tb_company_facts(h_share_code);
CREATE INDEX idx_listing_date ON tb_company_facts(listing_date);