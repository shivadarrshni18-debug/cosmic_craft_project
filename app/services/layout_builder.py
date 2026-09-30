from app.models import StoryResponse,ComicPanel
def build_comic_layout(story,image_urls):
    if len(story.panels)!=len(image_urls):raise ValueError("Every story panel must have exactly one image.")
    return [ComicPanel(panel_number=p.panel_number,title=p.title,image_url=image_urls[i],scene_description=p.scene_description,caption=p.caption,narration=p.narration,dialogue=p.dialogue,image_prompt=p.image_prompt) for i,p in enumerate(story.panels)]
