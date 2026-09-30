from fastapi import APIRouter,Form,HTTPException,Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from app.config import settings
from app.models import PromptRequest
from app.services.comic_service import generate_comic
from app.services.image_generator import generate_image
router=APIRouter(); templates=Jinja2Templates(directory=str(settings.template_dir))
@router.get("/",response_class=HTMLResponse)
async def home(request:Request):return templates.TemplateResponse(request=request,name="index.html",context={"title":settings.app_name})
@router.post("/generate",response_class=HTMLResponse)
async def generate(request:Request,story_prompt:str=Form(...),character_name:str=Form(...),setting:str=Form(...),tone:str=Form(...),art_style:str=Form(...)):
    try:
        result=generate_comic(PromptRequest(story_prompt=story_prompt,character_name=character_name,setting=setting,tone=tone,art_style=art_style))
        return templates.TemplateResponse(request=request,name="comic_preview.html",context={"title":result.title,"result":result,"demo_mode":settings.demo_mode})
    except Exception as exc:return templates.TemplateResponse(request=request,name="error.html",context={"error":str(exc)},status_code=500)
@router.post("/generate-comic/json")
async def generate_json(payload:PromptRequest):
    try:return generate_comic(payload)
    except Exception as exc:raise HTTPException(status_code=500,detail=str(exc)) from exc
@router.post("/test-image")
async def test_image(payload:dict):
    prompt=str(payload.get("prompt","")).strip()
    if len(prompt)<3:raise HTTPException(status_code=422,detail="prompt must contain at least 3 characters")
    try:return {"image_url":generate_image(prompt)}
    except Exception as exc:raise HTTPException(status_code=500,detail=str(exc)) from exc
@router.get("/export-success",response_class=HTMLResponse)
async def export_success(request:Request):return templates.TemplateResponse(request=request,name="export_success.html",context={})
@router.get("/health")
async def health():return {"status":"ok","demo_mode":settings.demo_mode}
