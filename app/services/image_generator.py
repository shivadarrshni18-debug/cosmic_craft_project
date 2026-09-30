import io,re,uuid
from pathlib import Path
from PIL import Image,ImageDraw
from huggingface_hub import InferenceClient
from app.config import settings

def _safe_name(s): return (re.sub(r"[^a-zA-Z0-9]+","-",s.lower()).strip("-")[:50] or "panel")+"-"+uuid.uuid4().hex[:8]+".png"
def _demo_image(prompt,path):
    img=Image.new("RGB",(1200,760),"white"); d=ImageDraw.Draw(img)
    d.rounded_rectangle((35,35,1165,725),radius=30,outline="black",width=8)
    d.ellipse((90,120,360,390),outline="black",width=8); d.ellipse((175,180,205,210),fill="black"); d.ellipse((275,180,305,210),fill="black")
    d.arc((170,205,310,330),10,170,fill="black",width=7); d.polygon([(180,120),(130,55),(225,105)],outline="black"); d.polygon([(290,120),(340,55),(335,150)],outline="black")
    d.rounded_rectangle((430,160,1060,420),radius=25,outline="black",width=7); d.text((470,210),"COMICCRAFT DEMO",fill="black"); d.text((470,270),prompt[:100],fill="black"); d.text((90,620),"Demo illustration — add HF_TOKEN for AI images.",fill="black"); img.save(path,"PNG")
def generate_image(prompt,panel_number=1):
    name=_safe_name(f"panel-{panel_number}-{prompt}"); path=settings.panel_dir/name
    if settings.demo_mode or not settings.hf_token:_demo_image(prompt,path)
    else:
        client=InferenceClient(provider=settings.hf_provider,api_key=settings.hf_token); image=client.text_to_image(prompt=prompt,model=settings.hf_image_model)
        if not isinstance(image,Image.Image):image=Image.open(io.BytesIO(image))
        image.convert("RGB").save(path,"PNG")
    return f"/static/panels/{name}"
