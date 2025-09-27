from fastapi import FastAPI
from api.routes import router
app = FastAPI(title='FastAPI OpenAI Template')
app.include_router(router, prefix='/api')

@app.get('/health')
def health():
    return {'status': 'ok'}