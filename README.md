# Portfolio Website Generator

This project is a Python-based static site generator that creates a personal portfolio website from a single `JSON` data file. It uses the Jinja2 templating engine to inject your data into HTML templates and generates a clean, professional, and responsive portfolio website, including a downloadable PDF version of your resume.

## Features

- **Data-Driven Content:** All portfolio content (personal info, work experience, projects, skills, etc.) is managed in a simple `portfolio-julius.json` file.
- **Static Site Generation:** Generates a full static website to the `output/` directory, which can be easily deployed to any static hosting service (like GitHub Pages).
- **HTML & PDF Resumes:** Creates both a web-viewable resume (`resume.html`) and a print-optimized PDF version (`resume.pdf`).
- **Automatic Asset Handling:** Automatically copies all necessary static assets (CSS, JS, images) to the output directory.
- **Easy to Customize:** Built with Jinja2 templates, making it easy to change the layout and design.

## Project Structure

```
.
├── output/                   # Generated website files
├── portfolio_media/          # Your profile picture and project images
├── templates/                # Jinja2 HTML templates
│   ├── index_template.html   # Main page template
│   └── resume_template.html  # Resume page template
├── generate_portfolio.py     # The main Python script to run
├── portfolio-julius.json     # Your personal data file
├── requirements.txt          # Python dependencies
└── README.md                 # This file
```

## Getting Started

### Prerequisites

- Python 3.7+
- `pip` for installing packages

### 1. Clone the Repository

```bash
git clone <your-repository-url>
cd <repository-directory>
```

### 2. Set Up a Virtual Environment (Recommended)

```bash
# For Linux/macOS
python3 -m venv .venv
source .venv/bin/activate

# For Windows
python -m venv .venv
.\.venv\Scripts\activate
```

### 3. Install Dependencies

Install the required Python packages using `pip`.

```bash
pip install -r requirements.txt
```

### 4. Customize Your Data

Open the `portfolio-julius.json` file and replace the placeholder content with your own personal information. This includes your name, contact details, work experience, projects, skills, and more.

Make sure to add your images (profile picture, project screenshots) to the `portfolio_media/` directory and update the paths in the JSON file accordingly.

### 5. Generate Your Portfolio

Run the generator script from the root of the project directory.

```bash
python generate_portfolio.py
```

The script will:
1.  Read your data from `portfolio-julius.json`.
2.  Generate `index.html` and `resume.html` in the `output/` directory.
3.  Copy all required static assets into `output/`.
4.  Generate a `resume.pdf` file in the `output/` directory and copy it to the project root.

### 6. View Your Portfolio

Open the `output/index.html` file in your web browser to see your generated portfolio website.

## Deployment

Since the `output/` directory contains a fully static website, you can deploy it to any static hosting provider. A popular and free option is **GitHub Pages**.

To deploy with GitHub Pages:
1. Push your generated `output/` directory to a repository on GitHub.
2. In your repository's settings, go to the "Pages" section.
3. Select the branch and the `/output` folder (or `/docs` if you move the files) as the source for your GitHub Pages site.

Inspired by: Corey Shafer.