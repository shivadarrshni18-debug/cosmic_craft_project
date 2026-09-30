# ComicCraft — AI Comic Story Creator

ComicCraft is a FastAPI + Jinja2 application that turns a story idea into a five-panel comic. The pipeline is: structured Gemini outline → Gemini narration/dialogue → Hugging Face text-to-image illustrations → layout binding → FPDF PDF export.

The original documentation uses legacy `google-generativeai`, Gemini 1.5 names and local Diffusers. This implementation uses the current `google-genai` SDK and hosted Hugging Face Inference Providers, with model IDs configurable through `.env`. See the included documentation notes below.

## Run on Windows

1. Open this folder in VS Code.
2. Terminal → New Terminal.
3. Create and activate a virtual environment:

```powershell
py -3.11 -m venv .venv
.venv\Scripts\Activate.ps1
```

If PowerShell blocks activation, use Command Prompt:

```bat
.venv\Scripts\activate.bat
```

4. Install:

```powershell
python -m pip install --upgrade pip
pip install -r requirements.txt
```

5. Copy `.env.example` to `.env`. Keep `DEMO_MODE=true` for the first test.
6. Start:

```powershell
python -m uvicorn app.main:app --reload
```

Open http://127.0.0.1:8000 and http://127.0.0.1:8000/docs.

## Demo test

Use prompt `A brave fox discovers a glowing library in an enchanted forest.`, character `Finn`, and any dropdown values. Demo mode creates five local placeholder images and a real PDF, so the complete app can be tested without API keys.

## Real AI

Set in `.env`:

```env
DEMO_MODE=false
GEMINI_API_KEY=your_google_ai_studio_key
HF_TOKEN=your_hugging_face_token
GEMINI_OUTLINE_MODEL=gemini-3.6-flash
GEMINI_STORY_MODEL=gemini-3.6-flash
HF_PROVIDER=auto
HF_IMAGE_MODEL=black-forest-labs/FLUX.1-schnell
```

If your account exposes another current Gemini model, change the model IDs. Never put a real API key into source code or commit `.env`.

## API

`POST /generate-comic/json` accepts:

```json
{"story_prompt":"A brave fox explores an enchanted forest.","character_name":"Finn","setting":"Enchanted forest","tone":"Funny","art_style":"Comic book"}
```

`POST /test-image` accepts `{"prompt":"A cheerful fox in a magical forest, comic book style"}`.

## Tests

```powershell
pytest -q
```

## Troubleshooting

If imports fail, activate `.venv` and rerun `pip install -r requirements.txt`. If real AI calls fail while demo mode works, check the API keys, network, model IDs, and provider availability. You can always return to `DEMO_MODE=true` while testing the UI.
