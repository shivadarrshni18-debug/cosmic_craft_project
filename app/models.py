from typing import List
from pydantic import BaseModel, Field, field_validator
class PromptRequest(BaseModel):
    story_prompt: str = Field(min_length=5,max_length=1000)
    character_name: str = Field(min_length=1,max_length=80)
    setting: str = Field(min_length=1,max_length=120)
    tone: str = Field(min_length=1,max_length=50)
    art_style: str = Field(min_length=1,max_length=80)
    @field_validator("*")
    @classmethod
    def clean_text(cls,v): return " ".join(v.strip().split())
class PanelOutline(BaseModel):
    panel_number:int; title:str; scene_description:str; image_prompt:str
class OutlineResponse(BaseModel): panels:List[PanelOutline]
class PanelStory(BaseModel):
    panel_number:int; title:str; scene_description:str; caption:str; narration:str; dialogue:str; image_prompt:str
class StoryResponse(BaseModel): panels:List[PanelStory]
class ComicPanel(BaseModel):
    panel_number:int; title:str; image_url:str; scene_description:str; caption:str; narration:str; dialogue:str; image_prompt:str
class GenerateResponse(BaseModel): title:str; panels:List[ComicPanel]; pdf_url:str
