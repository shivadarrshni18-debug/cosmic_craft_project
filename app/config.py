from functools import lru_cache
from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict
BASE_DIR = Path(__file__).resolve().parent.parent
class Settings(BaseSettings):
    app_name: str = "ComicCraft"
    debug: bool = True
    demo_mode: bool = True
    gemini_api_key: str = ""
    gemini_outline_model: str = "gemini-3.6-flash"
    gemini_story_model: str = "gemini-3.6-flash"
    hf_token: str = ""
    hf_provider: str = "auto"
    hf_image_model: str = "black-forest-labs/FLUX.1-schnell"
    model_config = SettingsConfigDict(env_file=BASE_DIR / ".env", env_file_encoding="utf-8", case_sensitive=False, extra="ignore")
    @property
    def static_dir(self): return BASE_DIR / "app" / "static"
    @property
    def template_dir(self): return BASE_DIR / "app" / "templates"
    @property
    def panel_dir(self): return self.static_dir / "panels"
    @property
    def export_dir(self): return self.static_dir / "exports"
@lru_cache
def get_settings():
    s=Settings(); s.panel_dir.mkdir(parents=True,exist_ok=True); s.export_dir.mkdir(parents=True,exist_ok=True); return s
settings=get_settings()
