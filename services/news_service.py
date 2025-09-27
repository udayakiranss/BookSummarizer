from typing import List, Dict, Any
from datetime import datetime
from integrations.openai_client import OpenAIClient
from integrations.openai_stub import OpenAIStub
from models.news_models import NewsItem, StockMarketNewsResponse
from utils.logger import logger
from config.config import settings

class NewsService:
    """Service layer for news-related business logic."""
    
    def __init__(self):
        # Use stub or real OpenAI client based on configuration
        if settings.use_openai_stub or settings.stub_mode:
            logger.info("🔧 Using OpenAI Stub for development/testing")
            self.openai_client = OpenAIStub()
        else:
            logger.info("🤖 Using real OpenAI API")
            self.openai_client = OpenAIClient()
    
    async def get_stock_market_news(self, limit: int = 5) -> StockMarketNewsResponse:
        """
        Get latest Indian stock market news.
        
        Args:
            limit: Number of news items to return (1-10)
            
        Returns:
            StockMarketNewsResponse: Structured news data
        """
        try:
            logger.service_flow("NewsService", "get_stock_market_news", {"limit": limit})
            logger.info(f"📰 Fetching {limit} stock market news items")
            
            # Validate limit
            if limit < 1 or limit > 10:
                limit = 5
                logger.warning(f"⚠️  Invalid limit {limit}, using default value 5")
            
            # Get news from OpenAI (or stub)
            logger.info(f"🔄 Calling OpenAI client with limit={limit}")
            news_data = await self.openai_client.generate_news(limit)
            logger.info(f"✅ Received news data: {len(news_data.get('news_items', []))} items")
            
            # Transform to our models
            news_items = []
            for i, item in enumerate(news_data.get("news_items", [])):
                try:
                    logger.debug(f"🔄 Processing news item {i+1}: {item.get('title', 'No title')[:50]}...")
                    news_item = NewsItem(
                        title=item.get("title", "No title available"),
                        summary=item.get("summary", "No summary available"),
                        impact=item.get("impact", "Neutral"),
                        relevance_score=float(item.get("relevance_score", 0.5))
                    )
                    news_items.append(news_item)
                    logger.debug(f"✅ Processed news item {i+1} successfully")
                except Exception as e:
                    logger.warning(f"⚠️  Failed to process news item {i+1}: {e}")
                    continue
            
            # Create response
            response = StockMarketNewsResponse(
                news_items=news_items,
                total_count=len(news_items),
                generated_at=datetime.now(),
                source=news_data.get("source", "AI Generated")
            )
            
            logger.service_flow("NewsService", "get_stock_market_news", output_data={
                "total_items": len(news_items),
                "source": response.source,
                "generated_at": response.generated_at.isoformat()
            })
            logger.info(f"🎉 Successfully processed {len(news_items)} news items")
            return response
            
        except Exception as e:
            logger.error(f"❌ Error in news service: {e}")
            # Return empty response on error
            return StockMarketNewsResponse(
                news_items=[],
                total_count=0,
                generated_at=datetime.now(),
                source="Error"
            )
    
    async def analyze_news_impact(self, news_title: str) -> Dict[str, Any]:
        """
        Analyze the market impact of a specific news item.
        
        Args:
            news_title: Title of the news to analyze
            
        Returns:
            Dict containing analysis results
        """
        try:
            logger.info(f"Analyzing impact for news: {news_title[:50]}...")
            
            analysis = await self.openai_client.analyze_news_impact(news_title)
            
            logger.info("News impact analysis completed")
            return analysis
            
        except Exception as e:
            logger.error(f"Error analyzing news impact: {e}")
            return {"analysis": "Impact: Neutral | Score: 0.5"}
    
    def get_news_statistics(self, news_items: List[NewsItem]) -> Dict[str, Any]:
        """
        Get statistics about the news items.
        
        Args:
            news_items: List of news items to analyze
            
        Returns:
            Dict containing statistics
        """
        if not news_items:
            return {
                "total_items": 0,
                "positive_impact": 0,
                "negative_impact": 0,
                "neutral_impact": 0,
                "average_relevance": 0.0
            }
        
        positive_count = sum(1 for item in news_items if item.impact.lower() == "positive")
        negative_count = sum(1 for item in news_items if item.impact.lower() == "negative")
        neutral_count = sum(1 for item in news_items if item.impact.lower() == "neutral")
        avg_relevance = sum(item.relevance_score for item in news_items) / len(news_items)
        
        return {
            "total_items": len(news_items),
            "positive_impact": positive_count,
            "negative_impact": negative_count,
            "neutral_impact": neutral_count,
            "average_relevance": round(avg_relevance, 2)
        }
