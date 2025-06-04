import akshare as ak
from src.data.cache import get_cache
from src.data.models import (
    CompanyNews,
    CompanyNewsResponse,
    FinancialMetrics,
    FinancialMetricsResponse,
    Price,
    PriceResponse,
    LineItem,
    LineItemResponse,
    InsiderTrade,
    InsiderTradeResponse,
    CompanyFactsResponse,
)

def get_cn_prices(ticker: str, start_date: str, end_date: str) -> list[Price]:
    """Fetch price data from cache or AKShare."""
    cache = get_cache()
    if cached_data := cache.get_prices(ticker):
        return [Price(**price) for price in cached_data if start_date <= price["time"] <= end_date]
    
    # Fetch from akshare
    df_stock_zh_a_hist = ak.stock_zh_a_hist(symbol=ticker, start_date=start_date, end_date=end_date, adjust="qfq")
    prices = []
    for index, row in df_stock_zh_a_hist.iterrows():
        prices.append(Price(
            time=row["date"],
            open=row["open"],
            high=row["high"],
            low=row["low"],
            close=row["close"],
            volume=row["volume"],
        ))
    cache.set_prices(ticker, [p.model_dump() for p in prices])
    return prices

def get_cn_financial_metrics(
    ticker: str,
    end_date: str,
    period: str = "ttm",
    limit: int = 10,
) -> list[FinancialMetrics]:
    """Fetch financial metrics from cache or AKShare."""
    cache = get_cache()
    if cached_data := cache.get_financial_metrics(ticker):
        return [FinancialMetrics(**metric) for metric in cached_data]

    # Fetch market cap
    stock_individual_info_em_df = ak.stock_a_indicator_lg(symbol=ticker)
    market_cap_dict = {}
    price_to_earnings_ratio_dict = {}
    price_to_book_ratio_dict = {}
    price_to_sales_ratio_dict = {}

    for index, row in stock_individual_info_em_df.iterrows():
        market_cap_dict[row["trade_date"]] = row["total_mv"]
        price_to_earnings_ratio_dict[row["trade_date"]] = row["pe"]
        price_to_book_ratio_dict[row["trade_date"]] = row["pb"]
        price_to_sales_ratio_dict[row["trade_date"]] = row["ps"]
    

    # Fetch enterprise debt
    stock_financial_report_sina_df = ak.stock_financial_report_sina(stock=ticker, symbol="资产负债表")
    enterprise_debt_dict = {}
    for index, row in stock_financial_report_sina_df.iterrows():
        enterprise_debt_dict[row["报告日"]] = row["负债合计"]
    
    # Fetch enterprise cash
    stock_financial_report_sina_df = ak.stock_financial_report_sina(stock=ticker, symbol="现金流量表")
    enterprise_cash_dict = {}
    for index, row in stock_financial_report_sina_df.iterrows():
        enterprise_cash_dict[row["报告日"]] = row["经营活动产生的现金流量净额"]
    

    # Fetch financial metrics
    stock_financial_report_data_em_df = ak.stock_financial_report_data_em(symbol=ticker, report_type="单季度")

    return None

def search_cn_line_items(
    ticker: str,
    line_items: list[str],
    end_date: str,
    period: str = "ttm",
    limit: int = 10,
) -> list[LineItem]:
    """Fetch line items from AKShare."""
    return None

def get_cn_insider_trades(
    ticker: str,
    end_date: str,
    start_date: str | None = None,
    limit: int = 1000,
) -> list[InsiderTrade]:
    """Fetch insider trades from cache or API."""
    return None

def get_cn_company_news(
    ticker: str,
    end_date: str,
    start_date: str | None = None,
    limit: int = 1000,
) -> list[CompanyNews]:
    """Fetch company news from cache or API."""
    return None

def get_cn_market_cap(
    ticker: str,
    end_date: str,
) -> float | None:
    """Fetch market cap from the API."""
    return None