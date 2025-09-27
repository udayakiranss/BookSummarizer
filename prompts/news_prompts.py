"""
Token-efficient prompts for news generation and analysis.
Optimized to minimize token consumption while maintaining quality.
"""

# Main prompt for generating Indian stock market news
STOCK_MARKET_NEWS_PROMPT = """Generate {limit} recent Indian stock market news items. Format as JSON:

{{
  "news_items": [
    {{
      "title": "Brief headline (max 80 chars)",
      "summary": "2-3 sentence summary",
      "impact": "Positive/Negative/Neutral",
      "relevance_score": 0.0-1.0
    }}
  ]
}}

Focus on: NSE, BSE, major Indian companies, RBI policy, government announcements, sector performance.
Keep summaries concise and factual. Use current date context."""

# Alternative shorter prompt for basic news
BASIC_NEWS_PROMPT = """List {limit} Indian stock market headlines today. JSON format:
{{"news": ["headline1", "headline2", ...]}}"""

# Analysis prompt for news impact
IMPACT_ANALYSIS_PROMPT = """Analyze market impact of: "{news_title}"

Respond with only: Positive/Negative/Neutral and relevance score (0.0-1.0)
Format: Impact: [result] | Score: [0.0-1.0]"""

# Token-optimized system prompt
SYSTEM_PROMPT = """You are a financial news analyst. Provide accurate, concise information about Indian stock markets. 
Use minimal tokens. Focus on facts, not speculation. Current date: {current_date}."""

def get_news_prompt(limit: int = 5) -> str:
    """Get the main news generation prompt with limit."""
    return STOCK_MARKET_NEWS_PROMPT.format(limit=limit)

def get_system_prompt() -> str:
    """Get the system prompt with current date."""
    from datetime import datetime
    return SYSTEM_PROMPT.format(current_date=datetime.now().strftime("%Y-%m-%d"))

def get_impact_analysis_prompt(news_title: str) -> str:
    """Get the impact analysis prompt for a specific news item."""
    return IMPACT_ANALYSIS_PROMPT.format(news_title=news_title)
