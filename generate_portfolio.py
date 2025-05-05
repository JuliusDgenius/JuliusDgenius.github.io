import json
from datetime import datetime, timezone
from pathlib import Path
from jinja2 import Environment, FileSystemLoader  # <-- Add this import
import shutil

# Configuration
TEMPLATE_DIR = Path("templates")
OUTPUT_DIR = Path("output")
DATA_FILE = Path("portfolio-julius.json")

def load_data():
    with DATA_FILE.open(encoding="utf-8") as f:
        data = json.load(f)
    
    data.update({
        "current_year": datetime.now(tz=timezone.utc).year,
        "generated_at": datetime.now().isoformat()
    })
    
    if "social_links" in data:
        for link in data["social_links"]:
            if link.get("svg_path"):
                svg_path = Path(link["svg_path"])
                if svg_path.exists():
                    link["svg_data"] = svg_path.read_text(encoding="utf-8")
    return data

def generate_files():
    # Initialize Jinja2 environment
    env = Environment(  # <-- Properly declared env variable
        loader=FileSystemLoader(TEMPLATE_DIR),
        autoescape=True,
        trim_blocks=True,
        lstrip_blocks=True
    )
    
    data = load_data()
    
    OUTPUT_DIR.mkdir(exist_ok=True)
    
    templates = {
        "index_template.html": "index.html",
        "resume_template.html": "resume.html"
    }
    
    for template_name, output_name in templates.items():
        template = env.get_template(template_name)
        output_path = OUTPUT_DIR / output_name
        
        if output_path.exists():
            backup = output_path.with_suffix(f".bak{datetime.now().strftime('%Y%m%d%H%M%S')}")
            try:
                output_path.rename(backup)
            except FileNotFoundError:
                print(f"Could not backup {output_path}")
        
        with output_path.open("w", encoding="utf-8") as f:
            f.write(template.render(**data))

# Add this after generating files
def copy_assets():
    """Copy static assets to output directory"""
    assets = ['css', 'js', 'portfolio_media', 'img']
    for asset in assets:
        src = Path(asset)
        if src.exists():
            dest = OUTPUT_DIR / asset
            if dest.exists():
                shutil.rmtree(dest)
            shutil.copytree(src, dest)

if __name__ == "__main__":
    generate_files()
    copy_assets()
    print("Generation complete!")