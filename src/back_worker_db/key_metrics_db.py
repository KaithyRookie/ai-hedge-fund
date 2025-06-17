import logging
from ast import Dict
from datetime import date, datetime
from typing import Optional

import psycopg2
from pydantic import BaseModel, Field


class KeyMetricsData(BaseModel):
    # 主键
    id: Optional[int] = Field(default=None, description="自增主键")
    
    # 基本信息
    ticker: Optional[str] = Field(default=None, max_length=10, description="股票代码")
    report_date: Optional[datetime] = Field(default=None, description="报告日期")
    
    # 主要财务数据
    parent_company_net_profit: Optional[float] = Field(default=None, description="归母净利润")
    total_operating_revenue: Optional[float] = Field(default=None, description="营业总收入")
    operating_cost: Optional[float] = Field(default=None, description="营业成本")
    net_profit: Optional[float] = Field(default=None, description="净利润")
    non_recurring_profit: Optional[float] = Field(default=None, description="扣非净利润")
    total_shareholders_equity: Optional[float] = Field(default=None, description="股东权益合计(净资产)")
    goodwill: Optional[float] = Field(default=None, description="商誉")
    net_operating_cash_flow: Optional[float] = Field(default=None, description="经营现金流量净额")
    
    # 每股指标
    basic_eps: Optional[float] = Field(default=None, description="基本每股收益")
    net_assets_per_share: Optional[float] = Field(default=None, description="每股净资产")
    cash_flow_per_share: Optional[float] = Field(default=None, description="每股现金流")
    diluted_eps: Optional[float] = Field(default=None, description="稀释每股收益")
    diluted_net_assets_per_share: Optional[float] = Field(default=None, description="摊薄每股净资产_期末股数")
    adjusted_net_assets_per_share: Optional[float] = Field(default=None, description="调整每股净资产_期末股数")
    net_assets_per_share_new: Optional[float] = Field(default=None, description="每股净资产_最新股数")
    operating_cash_flow_per_share: Optional[float] = Field(default=None, description="每股经营现金流")
    net_cash_flow_per_share: Optional[float] = Field(default=None, description="每股现金流量净额")
    enterprise_fcf_per_share: Optional[float] = Field(default=None, description="每股企业自由现金流量")
    shareholder_fcf_per_share: Optional[float] = Field(default=None, description="每股股东自由现金流量")
    undistributed_profit_per_share: Optional[float] = Field(default=None, description="每股未分配利润")
    capital_reserve_per_share: Optional[float] = Field(default=None, description="每股资本公积金")
    surplus_reserve_per_share: Optional[float] = Field(default=None, description="每股盈余公积金")
    retained_earnings_per_share: Optional[float] = Field(default=None, description="每股留存收益")
    operating_revenue_per_share: Optional[float] = Field(default=None, description="每股营业收入")
    total_operating_revenue_per_share: Optional[float] = Field(default=None, description="每股营业总收入")
    ebit_per_share: Optional[float] = Field(default=None, description="每股息税前利润")
    
    # 盈利能力指标
    roe: Optional[float] = Field(default=None, description="净资产收益率(ROE)")
    roa: Optional[float] = Field(default=None, description="总资产报酬率(ROA)")
    gross_margin: Optional[float] = Field(default=None, description="毛利率")
    net_profit_margin: Optional[float] = Field(default=None, description="销售净利率")
    period_expense_ratio: Optional[float] = Field(default=None, description="期间费用率")
    diluted_roe: Optional[float] = Field(default=None, description="摊薄净资产收益率")
    average_roe: Optional[float] = Field(default=None, description="净资产收益率_平均")
    average_roe_non_recurring: Optional[float] = Field(default=None, description="净资产收益率_平均_扣除非经常损益")
    diluted_roe_non_recurring: Optional[float] = Field(default=None, description="摊薄净资产收益率_扣除非经常损益")
    ebit_margin: Optional[float] = Field(default=None, description="息税前利润率")
    total_capital_return: Optional[float] = Field(default=None, description="总资本回报率")
    invested_capital_return: Optional[float] = Field(default=None, description="投入资本回报率")
    after_tax_roa: Optional[float] = Field(default=None, description="息前税后总资产报酬率_平均")
    cost_profit_ratio: Optional[float] = Field(default=None, description="成本费用利润率")
    operating_profit_margin: Optional[float] = Field(default=None, description="营业利润率")
    average_asset_net_profit_rate: Optional[float] = Field(default=None, description="总资产净利率_平均")
    average_asset_net_profit_rate_minority: Optional[float] = Field(default=None, description="总资产净利率_平均(含少数股东损益)")
    
    # 成长能力指标
    operating_revenue_growth_rate: Optional[float] = Field(default=None, description="营业总收入增长率")
    parent_company_net_profit_growth_rate: Optional[float] = Field(default=None, description="归属母公司净利润增长率")
    
    # 现金流指标
    operating_cash_sales_ratio: Optional[float] = Field(default=None, description="经营活动净现金/销售收入")
    operating_cash_total_revenue_ratio: Optional[float] = Field(default=None, description="经营性现金净流量/营业总收入")
    cost_expense_ratio: Optional[float] = Field(default=None, description="成本费用率")
    sales_cost_ratio: Optional[float] = Field(default=None, description="销售成本率")
    operating_cash_parent_profit_ratio: Optional[float] = Field(default=None, description="经营活动净现金/归属母公司的净利润")
    income_tax_profit_ratio: Optional[float] = Field(default=None, description="所得税/利润总额")
    
    # 偿债能力指标
    asset_liability_ratio: Optional[float] = Field(default=None, description="资产负债率")
    current_ratio: Optional[float] = Field(default=None, description="流动比率")
    quick_ratio: Optional[float] = Field(default=None, description="速动比率")
    conservative_quick_ratio: Optional[float] = Field(default=None, description="保守速动比率")
    equity_multiplier: Optional[float] = Field(default=None, description="权益乘数")
    equity_multiplier_minority: Optional[float] = Field(default=None, description="权益乘数(含少数股权的净资产)")
    equity_debt_ratio: Optional[float] = Field(default=None, description="产权比率")
    cash_ratio: Optional[float] = Field(default=None, description="现金比率")
    
    # 营运能力指标
    accounts_receivable_turnover: Optional[float] = Field(default=None, description="应收账款周转率")
    accounts_receivable_days: Optional[float] = Field(default=None, description="应收账款周转天数")
    inventory_turnover: Optional[float] = Field(default=None, description="存货周转率")
    inventory_days: Optional[float] = Field(default=None, description="存货周转天数")
    total_asset_turnover: Optional[float] = Field(default=None, description="总资产周转率")
    total_asset_days: Optional[float] = Field(default=None, description="总资产周转天数")
    current_asset_turnover: Optional[float] = Field(default=None, description="流动资产周转率")
    current_asset_days: Optional[float] = Field(default=None, description="流动资产周转天数")
    accounts_payable_turnover: Optional[float] = Field(default=None, description="应付账款周转率")
    
    # 系统字段
    created_at: Optional[datetime] = Field(default=None, description="创建时间")
    updated_at: Optional[datetime] = Field(default=None, description="更新时间")
    is_deleted: Optional[bool] = Field(default=False, description="是否删除")

from contextlib import contextmanager
from psycopg2.extras import RealDictCursor

class KeyMetricsDB:
    def __init__(self, conn):
        self.conn = conn

    @contextmanager
    def get_cursor(self, commit: bool = True):
        """获取数据库游标的上下文管理器"""
        cursor = self.conn.cursor(cursor_factory=RealDictCursor)
        try:
            yield cursor
            if commit:
                self.conn.commit()
        except Exception as e:
            self.conn.rollback()
            logging.error(f"Database operation failed: {e}")
            raise
        finally:
            cursor.close()
    
    def get_latest_report_date(self, ticker:str) ->datetime:
        sql = """
            SELECT report_date
            FROM tb_key_metrics
            WHERE ticker = %s
            ORDER BY report_date DESC
            LIMIT 1
        """
        with self.get_cursor(False) as cursor:
            try:
                cursor.execute(sql, (ticker,))
                result = cursor.fetchone()
                return result['report_date'] if result else None
            except psycopg2.Error as e:
                logging.error(f"Failed to get latest report date: {e}")
                raise e
            except Exception as e:
                logging.error(f"Error fetching latest report date: {e}")
                raise e

    def insert_key_metrics(self, data:KeyMetricsData):
        columns = []
        values = []
        kwargs = data.model_dump(exclude={'id', 'created_at', 'update_at', 'is_deleted'})
        for key, value in kwargs.items():
            if value is None:
                continue
            columns.append(key)
            values.append(value)
        columns_str = ', '.join(columns)
        placeholders = ', '.join(['%s'] * len(values))
        sql = f"INSERT INTO tb_key_metrics ({columns_str}) VALUES ({placeholders})"
        with self.get_cursor() as cursor:
            try:
                cursor.execute(sql, values)
            except psycopg2.Error as e:
                logging.error(f"Failed to insert key metrics: {e}")
                raise e
            except Exception as e:
                logging.error(f"Error insert key metrics: {e}")
                raise e
    
    def update_key_metrics(self, ticker:str, report_date:str, update_dict:dict):
        set_clause = ', '.join([f"{key} = %s" for key in update_dict.keys()])
        values = list(update_dict.values())
        values.append(ticker)
        values.append(report_date)
        sql = f"UPDATE tb_key_metrics SET {set_clause} WHERE ticker = %s AND report_date = %s"
        with self.get_cursor() as cursor:
            try:
                cursor.execute(sql, values)
            except psycopg2.Error as e:
                logging.error(f"Failed to update key metrics: {e}")
                raise e
    
    def query_key_metrics(self, ticker:str, start_date:str=None, end_date:str=None) ->list[KeyMetricsData]:
        params = ['ticker = %s']
        values = [ticker]
        if start_date:
            params.append('report_date >= %s')
            values.append(start_date)
        if end_date:
            params.append('report_date <= %s')
            values.append(end_date)
        params_str = ' AND '.join(params)
        sql = f"""
            SELECT *
            FROM tb_key_metrics
            WHERE {params_str}
            ORDER BY id
        """
        with self.get_cursor(False) as cursor:
            try:
                cursor.execute(sql, values)
                data_list = []
                for row in cursor.fetchall():
                    data_list.append(KeyMetricsData(**row))
                return data_list
            except psycopg2.Error as e:
                logging.error(f"Failed to query key metrics: {e}")
                raise e

