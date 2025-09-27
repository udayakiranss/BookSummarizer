import json
import asyncio
from typing import Dict, Any, Optional
from openai import AsyncOpenAI
from config.config import settings
from utils.logger import logger

class OpenAIClient:
    """OpenAI API client with token optimization."""
    
    def __init__(self):
        self.client = AsyncOpenAI(api_key=settings.openai_api_key)
        self.model = "gpt-3.5-turbo"  # Cost-effective model
        self.max_tokens = 500  # Limit token usage
        self.temperature = 0.3  # Lower temperature for more consistent results
    
    async def generate_news(self, limit: int = 5) -> Dict[str, Any]:
        """
        Generate Indian stock market news using OpenAI.
        Optimized for minimal token consumption.
        """
        try:
            from prompts.news_prompts import get_news_prompt, get_system_prompt
            
            logger.info(f"Generating {limit} news items using OpenAI")
            
            # Prepare messages
            messages = [
                {"role": "system", "content": get_system_prompt()},
                {"role": "user", "content": get_news_prompt(limit)}
            ]
            
            # Log full request
            logger.openai_request(
                model=self.model,
                prompt="",  # We'll use messages instead
                max_tokens=self.max_tokens,
                temperature=self.temperature,
                messages=messages
            )
            
            response = await self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                max_tokens=self.max_tokens,
                temperature=self.temperature,
                response_format={"type": "json_object"}
            )
            
            content = response.choices[0].message.content
            usage = response.usage.dict() if response.usage else None
            
            # Log full response
            logger.openai_response(
                model=self.model,
                response_length=len(content),
                usage=usage,
                full_response=content
            )
            
            logger.info(f"OpenAI response received, length: {len(content)}")
            
            # Parse JSON response
            news_data = json.loads(content)
            
            # Validate and clean the response
            if "news_items" not in news_data:
                logger.warning("Invalid response format from OpenAI")
                return self._create_fallback_response(limit)
            
            # Ensure we have the right number of items
            news_items = news_data["news_items"][:limit]
            
            logger.info(f"Successfully generated {len(news_items)} news items")
            return {
                "news_items": news_items,
                "total_count": len(news_items),
                "source": "OpenAI GPT-3.5-turbo"
            }
            
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse OpenAI response: {e}")
            return self._create_fallback_response(limit)
        except Exception as e:
            logger.error(f"OpenAI API error: {e}")
            return self._create_fallback_response(limit)
    
    def _create_fallback_response(self, limit: int) -> Dict[str, Any]:
        """Create fallback response when OpenAI fails."""
        logger.warning("Using fallback response due to OpenAI error")
        
        fallback_news = [
            {
                "title": "Indian Stock Markets Show Mixed Signals",
                "summary": "NSE and BSE indices trading with mixed trends amid global market volatility.",
                "impact": "Neutral",
                "relevance_score": 0.8
            },
            {
                "title": "RBI Monetary Policy Review Expected",
                "summary": "Reserve Bank of India likely to maintain current interest rates in upcoming policy review.",
                "impact": "Neutral",
                "relevance_score": 0.9
            },
            {
                "title": "IT Sector Stocks Under Pressure",
                "summary": "Technology stocks facing headwinds due to global economic concerns.",
                "impact": "Negative",
                "relevance_score": 0.7
            }
        ]
        
        return {
            "news_items": fallback_news[:limit],
            "total_count": min(len(fallback_news), limit),
            "source": "Fallback Data"
        }
    
    async def analyze_news_impact(self, news_title: str) -> Dict[str, Any]:
        """Analyze the market impact of a specific news item."""
        try:
            from prompts.news_prompts import get_impact_analysis_prompt
            
            # Prepare messages
            messages = [
                {"role": "user", "content": get_impact_analysis_prompt(news_title)}
            ]
            
            # Log full request
            logger.openai_request(
                model=self.model,
                prompt="",  # We'll use messages instead
                max_tokens=100,
                temperature=0.1,
                messages=messages
            )
            
            response = await self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                max_tokens=100,  # Very limited tokens for analysis
                temperature=0.1
            )
            
            content = response.choices[0].message.content
            usage = response.usage.dict() if response.usage else None
            
            # Log full response
            logger.openai_response(
                model=self.model,
                response_length=len(content),
                usage=usage,
                full_response=content
            )
            
            logger.info(f"Impact analysis completed for: {news_title[:50]}...")
            
            return {"analysis": content}
            
        except Exception as e:
            logger.error(f"Failed to analyze news impact: {e}")
            return {"analysis": "Impact: Neutral | Score: 0.5"}
