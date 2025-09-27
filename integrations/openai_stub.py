import json
import asyncio
from typing import Dict, Any, Optional
from utils.logger import logger

class OpenAIStub:
    """OpenAI API stub that returns hardcoded responses for development and testing."""
    
    def __init__(self):
        self.model = "gpt-3.5-turbo-stub"
        self.max_tokens = 500
        self.temperature = 0.3
        
        # Hardcoded news data for different scenarios
        self.hardcoded_news = {
            1: [
                {
                    "title": "NSE Sensex crosses 75,000 mark for the first time",
                    "summary": "The benchmark Sensex index reached a historic milestone, crossing 75,000 points driven by strong FII inflows and positive corporate earnings.",
                    "impact": "Positive",
                    "relevance_score": 0.95
                }
            ],
            3: [
                {
                    "title": "RBI maintains repo rate at 6.5% in latest policy review",
                    "summary": "The Reserve Bank of India kept the key policy rate unchanged, citing inflation concerns and global economic uncertainty.",
                    "impact": "Neutral",
                    "relevance_score": 0.9
                },
                {
                    "title": "IT sector stocks rally on strong Q3 earnings",
                    "summary": "Major IT companies report better-than-expected quarterly results, leading to a surge in technology stocks.",
                    "impact": "Positive",
                    "relevance_score": 0.85
                },
                {
                    "title": "Banking sector faces headwinds from rising NPAs",
                    "summary": "Public sector banks report increase in non-performing assets, raising concerns about sector stability.",
                    "impact": "Negative",
                    "relevance_score": 0.8
                }
            ],
            5: [
                {
                    "title": "Government announces major infrastructure push worth ₹10 lakh crore",
                    "summary": "Union government unveils comprehensive infrastructure development plan focusing on roads, railways, and digital infrastructure.",
                    "impact": "Positive",
                    "relevance_score": 0.9
                },
                {
                    "title": "Auto sector shows mixed signals with EV adoption",
                    "summary": "Traditional automakers face challenges while EV manufacturers see strong growth in the Indian market.",
                    "impact": "Neutral",
                    "relevance_score": 0.75
                },
                {
                    "title": "Pharma stocks surge on FDA approvals",
                    "summary": "Several Indian pharmaceutical companies receive FDA approvals for new drugs, boosting sector performance.",
                    "impact": "Positive",
                    "relevance_score": 0.8
                },
                {
                    "title": "Real estate sector faces liquidity crunch",
                    "summary": "Real estate developers struggle with funding as banks tighten lending norms for the sector.",
                    "impact": "Negative",
                    "relevance_score": 0.7
                },
                {
                    "title": "FMCG companies report steady growth in rural markets",
                    "summary": "Fast-moving consumer goods companies see consistent growth in rural areas despite economic headwinds.",
                    "impact": "Positive",
                    "relevance_score": 0.75
                }
            ]
        }
    
    async def generate_news(self, limit: int = 5) -> Dict[str, Any]:
        """
        Generate hardcoded Indian stock market news.
        Simulates OpenAI API response with realistic data.
        """
        try:
            logger.integration_flow("OpenAIStub", "generate_news", {"limit": limit})
            
            # Simulate API delay
            await asyncio.sleep(0.5)
            
            # Get appropriate hardcoded data
            if limit in self.hardcoded_news:
                news_items = self.hardcoded_news[limit]
            elif limit < 3:
                news_items = self.hardcoded_news[1]
            elif limit < 5:
                news_items = self.hardcoded_news[3]
            else:
                news_items = self.hardcoded_news[5][:limit]
            
            # Ensure we don't exceed the requested limit
            news_items = news_items[:limit]
            
            # Simulate token usage
            total_tokens = len(json.dumps(news_items)) + 100  # Approximate token count
            
            response = {
                "news_items": news_items,
                "total_count": len(news_items),
                "source": "OpenAI Stub (Hardcoded Data)"
            }
            
            # Prepare mock messages for logging
            mock_messages = [
                {"role": "system", "content": f"Generate {limit} Indian stock market news items"},
                {"role": "user", "content": f"Generate {limit} Indian stock market news items"}
            ]
            
            logger.openai_request(
                model=self.model,
                prompt="",  # We'll use messages instead
                max_tokens=self.max_tokens,
                temperature=self.temperature,
                messages=mock_messages
            )
            
            # Create mock response content
            mock_response = json.dumps(response, indent=2)
            
            logger.openai_response(
                model=self.model,
                response_length=total_tokens,
                usage={
                    "prompt_tokens": 50,
                    "completion_tokens": total_tokens - 50,
                    "total_tokens": total_tokens
                },
                full_response=mock_response
            )
            
            logger.integration_flow("OpenAIStub", "generate_news", response_data=response)
            
            return response
            
        except Exception as e:
            logger.error(f"Error in OpenAI stub: {e}")
            return self._create_fallback_response(limit)
    
    def _create_fallback_response(self, limit: int) -> Dict[str, Any]:
        """Create fallback response when stub fails."""
        logger.warning("Using fallback response in OpenAI stub")
        
        fallback_news = [
            {
                "title": "Market shows mixed signals amid global uncertainty",
                "summary": "Indian stock markets exhibit volatility with mixed sectoral performance.",
                "impact": "Neutral",
                "relevance_score": 0.7
            }
        ]
        
        return {
            "news_items": fallback_news[:limit],
            "total_count": min(len(fallback_news), limit),
            "source": "OpenAI Stub Fallback"
        }
    
    async def analyze_news_impact(self, news_title: str) -> Dict[str, Any]:
        """Analyze the market impact of a specific news item using hardcoded logic."""
        try:
            logger.integration_flow("OpenAIStub", "analyze_news_impact", {"news_title": news_title})
            
            # Simulate API delay
            await asyncio.sleep(0.2)
            
            # Simple hardcoded analysis based on keywords
            title_lower = news_title.lower()
            
            if any(word in title_lower for word in ["surge", "rally", "growth", "positive", "strong", "boost"]):
                impact = "Positive"
                score = 0.8
            elif any(word in title_lower for word in ["decline", "fall", "negative", "weak", "crunch", "headwinds"]):
                impact = "Negative"
                score = 0.7
            else:
                impact = "Neutral"
                score = 0.6
            
            analysis = f"Impact: {impact} | Score: {score}"
            
            logger.openai_response(
                model=self.model,
                response_length=len(analysis),
                usage={
                    "prompt_tokens": 20,
                    "completion_tokens": 10,
                    "total_tokens": 30
                }
            )
            
            logger.integration_flow("OpenAIStub", "analyze_news_impact", response_data={"analysis": analysis})
            
            return {"analysis": analysis}
            
        except Exception as e:
            logger.error(f"Failed to analyze news impact in stub: {e}")
            return {"analysis": "Impact: Neutral | Score: 0.5"}
