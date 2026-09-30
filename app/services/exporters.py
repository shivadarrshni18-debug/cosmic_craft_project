from datetime import datetime
from pathlib import Path
from urllib.parse import urlparse
from fpdf import FPDF
from app.config import settings

def _local_image(url):
    p=settings.panel_dir/Path(urlparse(url).path).name
    if not p.exists():raise FileNotFoundError(f"Panel image not found: {p.name}")
    return p

def save_pdf(panels,title):
    filename=f"comiccraft-{datetime.now().strftime('%Y%m%d-%H%M%S')}.pdf"; out=settings.export_dir/filename
    pdf=FPDF(); pdf.set_auto_page_break(auto=True,margin=18)
    for p in panels:
        pdf.add_page(); pdf.set_font("Helvetica","B",18); pdf.cell(0,12,text=f"Panel {p.panel_number}: {p.title}",new_x="LMARGIN",new_y="NEXT")
        pdf.image(str(_local_image(p.image_url)),x=15,y=32,w=180); pdf.ln(112)
        pdf.set_x(15); pdf.set_font("Helvetica","B",11); pdf.multi_cell(180,7,text=f"Scene: {p.scene_description}")
        pdf.set_font("Helvetica","",11); pdf.set_x(15); pdf.multi_cell(180,7,text=f"Caption: {p.caption}"); pdf.set_x(15); pdf.multi_cell(180,7,text=f"Narration: {p.narration}"); pdf.set_x(15); pdf.multi_cell(180,7,text=f"Dialogue: {p.dialogue}")
    pdf.output(str(out)); return f"/static/exports/{filename}"
