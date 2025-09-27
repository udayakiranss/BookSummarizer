from fastapi import FastAPI
from api.routes import router
from api.news_routes import router as news_router
from utils.logger import logger

app = FastAPI(
    title='Book-Insight API',
    description='AI-powered book analysis and insights with stock market news',
    version='1.0.0'
)

# Include routers
app.include_router(router, prefix='/api')
app.include_router(news_router, prefix='/api/news', tags=['News'])

# Startup event
@app.on_event("startup")
async def startup_event():
    logger.info("Book-Insight API starting up...")

# Shutdown event
@app.on_event("shutdown")
async def shutdown_event():
    logger.info("Book-Insight API shutting down...")

@app.get('/health')
def health():
    return {'status': 'ok'}