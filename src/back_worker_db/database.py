import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

def init_database(host: str, user: str, password: str, database: str):
    """初始化数据库和表"""
    # 首先连接到默认数据库以创建新数据库
    conn = psycopg2.connect(
        host=host,
        user=user,
        password=password,
        database="postgres"
    )
    conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    cur = conn.cursor()

    # 检查并创建数据库
    cur.execute("SELECT 1 FROM pg_database WHERE datname = 'db_ai_hedge_fund'")
    if not cur.fetchone():
        cur.execute(f"CREATE DATABASE {database}")
    
    cur.close()
    conn.close()

    # 连接到新创建的数据库
    conn = psycopg2.connect(
        host=host,
        user=user, 
        password=password,
        database=database
    )
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS tb_stock (
            id SERIAL PRIMARY KEY,
            ticker VARCHAR(20),
            name VARCHAR(200),
            stock_type VARCHAR(20),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
            is_deleted BOOLEAN DEFAULT FALSE,
            PRIMARY KEY (id),
            index (ticker)
        )
    """)

    # 创建股票价格表
    cur.execute("""
        CREATE TABLE IF NOT EXISTS tb_stock_price (
            id SERIAL PRIMARY KEY,
            ticker VARCHAR(20),
            stock_type VARCHAR(20),
            time DATE,
            open DECIMAL,
            high DECIMAL,
            low DECIMAL,
            close DECIMAL,
            volume BIGINT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
            is_deleted BOOLEAN DEFAULT FALSE,
            PRIMARY KEY (id),
            index (ticker, stock_type, time)
        )
    """)

    # 创建财务指标表
    cur.execute("""
        CREATE TABLE IF NOT EXISTS tb_financial_metrics (
            id SERIAL PRIMARY KEY,
            ticker VARCHAR(20),
            report_period DATE,
            period VARCHAR(20),
            currency VARCHAR(20),
            market_cap DECIMAL,
            enterprise_value DECIMAL,
            pe_ratio DECIMAL,
            pb_ratio DECIMAL,
            ps_ratio DECIMAL,
            enterprise_value_to_ebitda_ratio FLOAT,
            enterprise_value_to_revenue_ratio FLOAT,
            free_cash_flow_yield FLOAT,
            peg_ratio FLOAT,
            gross_margin FLOAT,
            operating_margin FLOAT,
            net_margin FLOAT,
            return_on_equity FLOAT,
            return_on_assets FLOAT,
            return_on_invested_capital FLOAT,
            asset_turnover FLOAT,
            inventory_turnover FLOAT,
            receivables_turnover FLOAT,
            days_sales_outstanding FLOAT,
            operating_cycle FLOAT,
            working_capital_turnover FLOAT,
            current_ratio FLOAT,
            quick_ratio FLOAT,
            cash_ratio FLOAT,
            operating_cash_flow_ratio FLOAT,
            debt_to_equity FLOAT,
            debt_to_assets FLOAT,
            interest_coverage FLOAT,
            revenue_growth FLOAT,
            earnings_growth FLOAT,
            book_value_growth FLOAT,
            earnings_per_share_growth FLOAT,
            free_cash_flow_growth FLOAT,
            operating_income_growth FLOAT,
            ebitda_growth FLOAT,
            payout_ratio FLOAT,
            earnings_per_share FLOAT,
            book_value_per_share FLOAT,
            free_cash_flow_per_share FLOAT,
            fcff_per_share FLOAT,
            fcfe_per_share FLOAT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
            is_deleted BOOLEAN DEFAULT FALSE,
            PRIMARY KEY (id),
            index (ticker, report_period)
        )
    """)

    # 创建利润表
    cur.execute("""
        CREATE TABLE IF NOT EXISTS tb_profit (
            id SERIAL PRIMARY KEY,
            ticker VARCHAR(20),
            report_period DATE,
            consolidated_income DECIMAL,
            cost_of_revenue DECIMAL,
            dividends_per_common_share DECIMAL,
            earnings_per_share DECIMAL,
            earnings_per_share_diluted FLOAT,
            ebit FLOAT,
            ebit_usd FLOAT,
            earnings_per_share_usd FLOAT,
            gross_profit FLOAT,
            income_tax_expense FLOAT,
            interest_expense FLOAT,
            net_income_common_stock DECIMAL,
            net_income_common_stock_usd DECIMAL,
            net_income_discontinued_operations DECIMAL,
            net_income_non_controlling_interests DECIMAL,
            operating_expense DECIMAL,
            operating_income DECIMAL,
            preferred_dividends_impact DECIMAL,
            research_and_development DECIMAL,
            revenue DECIMAL,
            revenue_usd DECIMAL,
            selling_general_and_administrative_expenses DECIMAL,
            weighted_average_shares DECIMAL,
            weighted_average_shares_diluted DECIMAL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
            is_deleted BOOLEAN DEFAULT FALSE,
            PRIMARY KEY (id),
            index (ticker, report_period)
        )
    """)

    # 创建资产负债表

    cur.execute("""
        CREATE TABLE IF NOT EXISTS tb_balance_sheet (
            id SERIAL PRIMARY KEY,
            ticker VARCHAR(20),
            report_period DATE,
            accumulated_other_comprehensive_income DECIMAL,
            cash_and_equivalents DECIMAL,
            cash_and_equivalents_usd DECIMAL,
            current_assets DECIMAL,
            current_debt DECIMAL,
            current_investments DECIMAL,
            current_liabilities DECIMAL,
            deferred_revenue DECIMAL,
            deposit_liabilities DECIMAL,
            goodwill_and_intangible_assets DECIMAL,
            inventory DECIMAL,
            investments DECIMAL,
            non_current_assets DECIMAL,
            non_current_debt DECIMAL,
            non_current_investments DECIMAL,
            non_current_liabilities DECIMAL,
            outstanding_shares DECIMAL,
            property_plant_and_equipment DECIMAL,
            retained_earnings DECIMAL,
            shareholders_equity DECIMAL,
            shareholders_equity_usd DECIMAL,
            tax_assets DECIMAL,
            tax_liabilities DECIMAL,
            total_assets DECIMAL,
            total_debt DECIMAL,
            total_debt_usd DECIMAL,
            total_liabilities DECIMAL,
            trade_and_non_trade_payables DECIMAL,
            trade_and_non_trade_receivables DECIMAL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
            is_deleted BOOLEAN DEFAULT FALSE,
            PRIMARY KEY (id),
            index (ticker, report_period)
        )
    """)

    # 创建现金流量表
    cur.execute("""
        CREATE TABLE IF NOT EXISTS tb_cash_flow (
            id SERIAL PRIMARY KEY,
            ticker VARCHAR(20),
            report_period DATE,
            business_acquisitions_and_disposals DECIMAL,
            capital_expenditure DECIMAL,
            change_in_cash_and_equivalents DECIMAL,
            depreciation_and_amortization DECIMAL,
            dividends_and_other_cash_distributions DECIMAL,
            effect_of_exchange_rate_changes DECIMAL,
            investment_acquisitions_and_disposals DECIMAL,
            issuance_or_purchase_of_equity_shares DECIMAL,
            issuance_or_repayment_of_debt_securities DECIMAL,
            net_cash_flow_from_financing DECIMAL,
            net_cash_flow_from_investing DECIMAL,
            net_cash_flow_from_operations DECIMAL,
            share_based_compensation DECIMAL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
            is_deleted BOOLEAN DEFAULT FALSE,
            PRIMARY KEY (id),
            index (ticker, report_period)
        )
    """)

    # 创建财务明细项表
    cur.execute("""
        CREATE TABLE IF NOT EXISTS tb_line_item (
            id SERIAL PRIMARY KEY,
            ticker VARCHAR(20),
            report_period DATE,
            period VARCHAR(20),
            currency VARCHAR(20),
            search_result LONGTEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
            is_deleted BOOLEAN DEFAULT FALSE,
            PRIMARY KEY (id),
            index (ticker, report_period)
        )
    """)

    # 创建内部交易表
    cur.execute("""
        CREATE TABLE IF NOT EXISTS tb_insider_trade (
            id SERIAL PRIMARY KEY,
            ticker VARCHAR(20),
            issuer VARCHAR(100),
            name VARCHAR(100),
            title VARCHAR(100),
            is_board_director BOOLEAN,
            transaction_date VARCHAR(20),
            transaction_shares FLOAT,
            transaction_price_per_share FLOAT,
            transaction_value FLOAT,
            shares_owned_before_transaction FLOAT,
            shares_owned_after_transaction FLOAT,
            security_title VARCHAR(100),
            filing_date VARCHAR(20),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
            is_deleted BOOLEAN DEFAULT FALSE,
            PRIMARY KEY (id)
        )
    """)

    # 创建公司新闻表
    cur.execute("""
        CREATE TABLE IF NOT EXISTS tb_company_news (
            id SERIAL PRIMARY KEY,
            ticker VARCHAR(20),
            title VARCHAR(200),
            author VARCHAR(100),
            source VARCHAR(100),
            date VARCHAR(20),
            content TEXT,
            url TEXT,
            sentiment VARCHAR(20),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
            is_deleted BOOLEAN DEFAULT FALSE,
            PRIMARY KEY (id)
        )
    """)

    # 创建公司基本信息表
    cur.execute("""
        CREATE TABLE IF NOT EXISTS tb_company_facts (
            id SERIAL PRIMARY KEY,
            ticker VARCHAR(20) PRIMARY KEY,
            name VARCHAR(200),
            cik VARCHAR(20),
            industry VARCHAR(100),
            sector VARCHAR(100),
            category VARCHAR(100),
            exchange VARCHAR(100),
            is_active BOOLEAN,
            listing_date VARCHAR(20),
            location VARCHAR(100),
            market_cap DECIMAL,
            number_of_employees INTEGER,
            sec_filings_url TEXT,
            sic_code VARCHAR(20),
            sic_industry VARCHAR(100),
            sic_sector VARCHAR(100),
            website_url TEXT,
            weighted_average_shares DECIMAL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
            is_deleted BOOLEAN DEFAULT FALSE,
            PRIMARY KEY (id)
        )
    """)

    conn.commit()
    cur.close()
    conn.close()

def get_db_connection(host: str, user: str, password: str, database: str):
    """获取数据库连接"""
    return psycopg2.connect(
        host=host,
        user=user,
        password=password,
        database=database
    )
