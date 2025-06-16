
from src.back_worker_db.company_news_db import CompanyNewsDB,CompanyNewsData
from src.utils.news_sentiment_analysis import analysis_news_sentiment
import akshare as ak
class CompanyNewsWorker:
    def __init__(self, db:CompanyNewsDB):
        self.db = db
    
    def download_company_news(self, ticker: str, ticker_name: str):
        """下载公司新闻
        
        Args:
            ticker: 股票代码
            start_date: 开始日期
            end_date: 结束日期
        """
        stock_news_em_df = ak.stock_news_em(symbol=ticker)
        for index, row in stock_news_em_df.iterrows():
            data = CompanyNewsData.model_construct()
            data.ticker = ticker
            data.news_title = row['新闻标题']
            data.news_content = row['新闻内容']
            data.publish_time = row['发布时间']
            data.news_source = row['文章来源']
            data.news_url = row['新闻链接']

            analysis_result = analysis_news_sentiment(data.news_url, ticker, ticker_name)
            
            data.sentiment = analysis_result["sentiment_analysis"].get('sentiment_label')
            data.sentiment_score = analysis_result["sentiment_analysis"].get('sentiment_score')
            data.confidence = analysis_result["sentiment_analysis"].get('confidence')
            data.confidence_score = analysis_result["sentiment_analysis"].get('confidence_score')
            data.key_factors = ",".join(analysis_result["analysis_details"].get('key_factors', []))
            data.market_impact = analysis_result["analysis_details"].get('market_impact')
            data.impact_reason = analysis_result["analysis_details"].get('impact_reason')

            self.db.insert(data)