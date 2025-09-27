from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime

class NewsItem(BaseModel):
    """Model for individual news item."""
    title: str = Field(..., description="News headline")
    summary: str = Field(..., description="Brief summary of the news")
    impact: str = Field(..., description="Market impact: Positive, Negative, or Neutral")
    relevance_score: float = Field(..., ge=0, le=1, description="Relevance score from 0 to 1")

class StockMarketNewsResponse(BaseModel):
    """Response model for stock market news."""
    news_items: List[NewsItem] = Field(..., description="List of news items")
    total_count: int = Field(..., description="Total number of news items")
    generated_at: datetime = Field(default_factory=datetime.now, description="Generation timestamp")
    source: str = Field(default="AI Generated", description="News source")

class NewsRequest(BaseModel):
    """Request model for news endpoint."""
    limit: int = Field(default=5, ge=1, le=10, description="Number of news items to return (1-10)")
    include_analysis: bool = Field(default=True, description="Include AI analysis of news impact")
