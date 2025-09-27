from fastapi import APIRouter, HTTPException, Query
from typing import Optional
from services.news_service import NewsService
from models.news_models import StockMarketNewsResponse, NewsRequest
from utils.logger import logger

router = APIRouter()

# Initialize news service
news_service = NewsService()

@router.get("/stock-market", response_model=StockMarketNewsResponse)
async def get_stock_market_news(
    limit: int = Query(default=5, ge=1, le=10, description="Number of news items to return (1-10)")
):
    """
    Get latest Indian stock market news.
    
    - **limit**: Number of news items to return (1-10, default: 5)
    
    Returns structured news data with AI-generated analysis.
    """
    try:
        logger.api_request("/api/news/stock-market", "GET", {"limit": limit})
        logger.info(f"🚀 Starting stock market news request with limit={limit}")
        
        # Get news from service
        logger.info(f"📞 Calling news service...")
        news_response = await news_service.get_stock_market_news(limit)
        
        # Log response statistics
        stats = news_service.get_news_statistics(news_response.news_items)
        logger.info(f"📊 News response stats: {stats}")
        
        # Log API response
        logger.api_response("/api/news/stock-market", 200, {
            "total_count": news_response.total_count,
            "source": news_response.source,
            "generated_at": news_response.generated_at.isoformat()
        })
        
        logger.info(f"✅ Successfully completed stock market news request")
        return news_response
        
    except Exception as e:
        logger.error(f"❌ Error in stock market news endpoint: {e}")
        logger.api_response("/api/news/stock-market", 500, {"error": str(e)})
        raise HTTPException(
            status_code=500,
            detail="Failed to fetch stock market news. Please try again later."
        )

@router.get("/stock-market/stats")
async def get_news_statistics(limit: int = Query(default=5, ge=1, le=10)):
    """
    Get statistics about the latest stock market news.
    
    - **limit**: Number of news items to analyze (1-10, default: 5)
    
    Returns news statistics and analysis.
    """
    try:
        logger.info(f"API request: Get news statistics with limit={limit}")
        
        # Get news data
        news_response = await news_service.get_stock_market_news(limit)
        
        # Get statistics
        stats = news_service.get_news_statistics(news_response.news_items)
        
        # Add additional metadata
        stats.update({
            "generated_at": news_response.generated_at,
            "source": news_response.source,
            "total_count": news_response.total_count
        })
        
        logger.info(f"Statistics generated: {stats}")
        return stats
        
    except Exception as e:
        logger.error(f"Error in news statistics endpoint: {e}")
        raise HTTPException(
            status_code=500,
            detail="Failed to generate news statistics. Please try again later."
        )
