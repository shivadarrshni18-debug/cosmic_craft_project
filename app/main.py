from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from app.config import settings
from app.routes import router
@asynccontextmanager
async def lifespan(app):
    settings.panel_dir.mkdir(parents=True,exist_ok=True); settings.export_dir.mkdir(parents=True,exist_ok=True); yield
app=FastAPI(title=settings.app_name,description="AI comic story creator using Gemini and Hugging Face image generation.",version="1.0.0",lifespan=lifespan)
app.mount("/static",StaticFiles(directory=str(settings.static_dir)),name="static"); app.include_router(router)
