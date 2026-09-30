from fastapi.testclient import TestClient
from app.main import app
client=TestClient(app)
def test_home():
    r=client.get("/"); assert r.status_code==200 and "ComicCraft" in r.text
def test_health():
    r=client.get("/health"); assert r.status_code==200 and r.json()["status"]=="ok"
def test_json_generation_demo():
    p={"story_prompt":"A brave fox explores an enchanted forest.","character_name":"Finn","setting":"Enchanted forest","tone":"Funny","art_style":"Comic book"}
    r=client.post("/generate-comic/json",json=p); assert r.status_code==200; d=r.json(); assert len(d["panels"])==5; assert d["pdf_url"].startswith("/static/exports/")
