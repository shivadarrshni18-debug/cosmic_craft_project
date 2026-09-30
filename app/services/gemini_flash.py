from google import genai
from app.config import settings
from app.models import OutlineResponse,PromptRequest

def _demo_outline(r):
    data=[("The Beginning",f"{r.character_name} enters {r.setting} and notices something unusual."),("A Strange Discovery",f"{r.character_name} follows a mysterious clue deeper into {r.setting}."),("The Challenge",f"A surprising obstacle tests {r.character_name}'s courage."),("The Turning Point",f"{r.character_name} discovers a clever way to solve the problem."),("A New Adventure",f"The adventure ends with a memorable discovery and a promise of more.")]
    return OutlineResponse.model_validate({"panels":[{"panel_number":i,"title":t,"scene_description":s,"image_prompt":f"{r.art_style} illustration, {s}, expressive character, cinematic composition, clean comic panel"} for i,(t,s) in enumerate(data,1)]})

def generate_outline(req):
    if settings.demo_mode or not settings.gemini_api_key:return _demo_outline(req)
    client=genai.Client(api_key=settings.gemini_api_key)
    prompt=f"Create exactly 5 connected comic panels. Story: {req.story_prompt}. Main character: {req.character_name}. Setting: {req.setting}. Tone: {req.tone}. Art style: {req.art_style}. Return five panels with title, concrete scene_description, and image_prompt. Preserve visual continuity. Do not include dialogue yet."
    response=client.models.generate_content(model=settings.gemini_outline_model,contents=prompt,config={"response_mime_type":"application/json","response_schema":OutlineResponse.model_json_schema()})
    return OutlineResponse.model_validate_json(response.text)
