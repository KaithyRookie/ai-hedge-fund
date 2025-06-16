CREATE TABLE IF NOT EXISTS tb_company_facts (
    id SERIAL PRIMARY KEY,
    company_name VARCHAR(255) NOT NULL , -- '公司名称',
    company_name_en VARCHAR(255) , -- '英文名称',
    former_short_name VARCHAR(255) , -- '曾用简称',
    a_share_code VARCHAR(20) , -- 'A股代码',
    a_share_name VARCHAR(100) , -- 'A股简称',
    b_share_code VARCHAR(20) , -- 'B股代码',
    b_share_name VARCHAR(100) , -- 'B股简称',
    h_share_code VARCHAR(20) , -- 'H股代码',
    h_share_name VARCHAR(100) , -- 'H股简称',
    selected_indices TEXT , -- '入选指数',
    market_category VARCHAR(100) , -- '所属市场',
    industry_category VARCHAR(100) , -- '所属行业',
    legal_representative VARCHAR(100) , -- '法人代表',
    registered_capital DECIMAL(15,4) , -- '注册资金',
    establishment_date DATE , -- '成立日期',
    listing_date DATE , -- '上市日期',
    official_website VARCHAR(255) , -- '官方网站',
    email VARCHAR(255) , -- '电子邮箱',
    contact_phone VARCHAR(50) , -- '联系电话',
    fax VARCHAR(50) , -- '传真',
    registered_address TEXT , -- '注册地址',
    office_address TEXT , -- '办公地址',
    postal_code VARCHAR(20) , -- '邮政编码',
    main_business TEXT , -- '主营业务',
    business_scope TEXT , -- '经营范围',
    company_profile TEXT , -- '机构简介',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 创建索引以提高查询性能
CREATE INDEX idx_company_name ON tb_company_facts(company_name);
CREATE INDEX idx_a_share_code ON tb_company_facts(a_share_code);
CREATE INDEX idx_h_share_code ON tb_company_facts(h_share_code);
CREATE INDEX idx_listing_date ON tb_company_facts(listing_date);