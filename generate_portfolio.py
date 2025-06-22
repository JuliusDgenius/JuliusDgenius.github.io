import json
from datetime import datetime, timezone
from pathlib import Path
from jinja2 import Environment, FileSystemLoader
from weasyprint import HTML, CSS
import shutil
import os

# Configuration
TEMPLATE_DIR = Path("templates")
OUTPUT_DIR = Path("output")
DATA_FILE = Path("portfolio-julius.json")

def generate_resume_pdf(env, data):
    """Generate a PDF version of the resume from a print-specific HTML template."""
    print_template = env.get_template("resume_print.html")
    # The base_url is important for weasyprint to find the CSS files
    html_content = print_template.render(**data)
    html = HTML(string=html_content, base_url=str(Path.cwd()))
    
    pdf_path = OUTPUT_DIR / "resume.pdf"
    
    html.write_pdf(target=pdf_path)
    print(f"Successfully generated {pdf_path}")

def copy_resume_pdf():
    src = OUTPUT_DIR / "resume.pdf"
    if src.exists():
        shutil.copy2(src, Path("resume.pdf"))
        print(f"Copied {src} to project root.")

def load_data():
    """Loads portfolio data and adds generated context."""
    with DATA_FILE.open(encoding="utf-8") as f:
        data = json.load(f)
    
    data.update({
        "current_year": datetime.now(tz=timezone.utc).year,
        "base_url": "file://" + str(Path.cwd() / OUTPUT_DIR)
    })
    
    if "social_links" in data:
        for link in data["social_links"]:
            if link.get("svg_path"):
                svg_path = Path(link["svg_path"])
                if svg_path.exists():
                    link["svg_data"] = svg_path.read_text(encoding="utf-8")
    return data

def generate_files(env, data):
    """Generates the main HTML files (index and on-screen resume)."""
    OUTPUT_DIR.mkdir(exist_ok=True)
    
    templates = {
        "index_template.html": "index.html",
        "resume_template.html": "resume.html"
    }
    
    for template_name, output_name in templates.items():
        template = env.get_template(template_name)
        output_path = OUTPUT_DIR / output_name
        output_path.write_text(template.render(**data), encoding="utf-8")
        print(f"Generated {output_path}")

def copy_assets():
    """Copies static assets to the output directory."""
    assets = ['css', 'js', 'portfolio_media', 'img']
    for asset in assets:
        src = Path(asset)
        if src.exists():
            dest = OUTPUT_DIR / asset
            if dest.exists():
                shutil.rmtree(dest)
            shutil.copytree(src, dest)
    print("Copied static assets to output directory.")

def cleanup_backups(directory: Path, keep: int = 5):
    """
    Deletes old backup files in a directory, keeping only a specified number of the most recent ones.
    """
    # Find all backup files using glob
    backup_files = sorted(
        directory.glob('*.bak*'),
        key=os.path.getmtime,
        reverse=True
    )

    # Check if there are more files than we want to keep
    if len(backup_files) > keep:
        # Determine which files to delete
        files_to_delete = backup_files[keep:]

        print(f"Found {len(backup_files)} backup files. Deleting {len(files_to_delete)} oldest files...")

        # Delete the old files
        for f in files_to_delete:
            try:
                f.unlink()
                print(f"  - Deleted {f.name}")
            except OSError as e:
                print(f"Error deleting file {f.name}: {e}")

        print("Backup cleanup complete.")
    else:
        print(f"Found {len(backup_files)} backup files. No cleanup needed.")

if __name__ == "__main__":
    # Initialize Jinja2 environment
    jinja_env = Environment(
        loader=FileSystemLoader(TEMPLATE_DIR),
        autoescape=True,
        trim_blocks=True,
        lstrip_blocks=True
    )
    
    # Load data
    portfolio_data = load_data()
    
    # Generate on-screen HTML files
    generate_files(jinja_env, portfolio_data)
    
    # Copy static assets
    copy_assets()
    
    # Generate the PDF from the print-specific template
    generate_resume_pdf(jinja_env, portfolio_data)
    
    # Copy the final PDF to the project root
    copy_resume_pdf()

    # Clean up old backup files
    cleanup_backups(OUTPUT_DIR)
