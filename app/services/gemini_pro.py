from google import genai
from app.config import settings
from app.models import OutlineResponse,PromptRequest,StoryResponse

def _demo_story(r,o):
    return StoryResponse.model_validate({"panels":[{"panel_number":p.panel_number,"title":p.title,"scene_description":p.scene_description,"caption":f"Meanwhile, in {r.setting}...","narration":f"{r.character_name} takes a careful step forward. The {r.tone.lower()} adventure becomes more exciting.","dialogue":f"{r.character_name}: I have a feeling this is only the beginning!","image_prompt":p.image_prompt} for p in o.panels]})

def generate_story(req,outline):
    if settings.demo_mode or not settings.gemini_api_key:return _demo_story(req,outline)
    client=genai.Client(api_key=settings.gemini_api_key)
    prompt=f"Expand this five-panel comic into polished narration and dialogue. Story: {req.story_prompt}. Character: {req.character_name}. Setting: {req.setting}. Tone: {req.tone}. Art style: {req.art_style}. Outline: {outline.model_dump_json()}. For every panel create scene_description, caption, narration, dialogue and refined image_prompt. Keep continuity consistent."
    response=client.models.generate_content(model=settings.gemini_story_model,contents=prompt,config={"response_mime_type":"application/json","response_schema":StoryResponse.model_json_schema()})
    return StoryResponse.model_validate_json(response.text)
