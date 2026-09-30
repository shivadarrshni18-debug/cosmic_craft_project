from app.models import PromptRequest,GenerateResponse
from app.services.gemini_flash import generate_outline
from app.services.gemini_pro import generate_story
from app.services.image_generator import generate_image
from app.services.layout_builder import build_comic_layout
from app.services.exporters import save_pdf

def generate_comic(req):
    outline=generate_outline(req); story=generate_story(req,outline)
    images=[generate_image(p.image_prompt,p.panel_number) for p in story.panels]
    layout=build_comic_layout(story,images); title=f"{req.character_name}'s Comic Adventure"; pdf=save_pdf(layout,title)
    return GenerateResponse(title=title,panels=layout,pdf_url=pdf)
