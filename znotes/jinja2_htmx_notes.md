# Jinja
## Jinja documentation
https://jinja.palletsprojects.com/en/stable/

## Installation
pip install Jinja2

### Dependencies
These will be installed automatically when installing Jinja.
* MarkupSafe escapes untrusted input when rendering templates to avoid injection attacks.

# aiofiles
Is it the Modern Best Practice to Work with Jinja2?

## No need for aiofiles
No. You do not need aiofiles to render Jinja2 templates in FastAPI, and using them together is actually an outdated anti-pattern.FastAPI includes a built-in helper module called FastAPI.templating.Jinja2Templates. Under the hood, this module handles template loading and rendering via a starlette utility that uses an internal thread pool executor. It automatically prevents the template reading process from blocking your main asyncio event loop.

## When to Use aiofiles?
While you should avoid it for Jinja2 templates, aiofiles is still the industry standard best practice in FastAPI for:
* File Uploads: Saving user-uploaded binary data (like images or PDFs) directly to your local server storage.
* Log Parsing: Reading system log files on the fly to display inside an internal dashboard tool.
* Configuration Files: Loading custom dynamic JSON or YAML files from disk during active runtime.

## Modern production setup
When using Jinja2 with FastAPI, you should use standard synchronous syntax for rendering. FastAPI manages the underlying thread safety perfectly behind the scenes:

```python
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

app = FastAPI()

# 1. Define the template directory
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse) # response_class no hizo falta en el test V0
async def read_item(request: Request):
    # 2. Correct modern practice (No aiofiles, no manual file opening)
    return templates.TemplateResponse(
        name="index.html", 
        # context={"request": request, "title": "My Production POC"} # AG No me anduvo
        request={"request": request, "title": "My Production POC"}
        
    )
```
# Dev and Prod setup
Building a FastAPI + Jinja2 + HTMX stack is highly efficient because the architecture remains unified. Your frontend lives directly inside your backend repository as HTML files, drastically simplifying the infrastructure.
------------------------------
## 1. The Core Architecture
The architecture relies on HTML Fragment Swapping instead of JSON APIs.

* Initial Request: The browser requests a page. FastAPI reads a base Jinja2 template and renders a complete HTML page.
* User Interaction: The user clicks an HTMX-powered button. HTMX sends an AJAX request to FastAPI.
* Partial Response: FastAPI renders a tiny Jinja2 partial template (just the specific HTML fragment that changed) and sends it back.
* The Swap: HTMX instantly swaps that fragment into the existing page without reloading.

## Recommended Directory Structure

my_project/
├── app/
│   ├── __init__.py
│   ├── main.py                # FastAPI app & routing
│   ├── static/                # Static assets (CSS, JS)
│   │   └── css/
│   │       └── styles.css
│   └── templates/             # Jinja2 Templates
│       ├── base.html          # Global layout (head, navbar, footer)
│       ├── index.html         # Main page content
│       └── partials/          # HTMX-specific snippets
│           └── click_result.html
├── requirements.txt
└── Dockerfile

------------------------------
## 2. The Code Setup (FastAPI + Jinja2 + HTMX)
### app/templates/base.html (The Shell)
Include HTMX via a CDN or local static file in your head element.

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>{% block title %}My App{% endblock %}</title>
    <!-- HTMX CDN -->
    <script src="https://unpkg.com"></script>
</head>
<body>
    <nav>My Production Navbar</nav>
    <main>
        {% block content %}{% endblock %}
    </main>
</body>
</html>
```

### app/templates/index.html (The Page)
This page embeds an HTMX attribute (hx-get). When the button is clicked, HTMX targets the <div> with ID result-box.

```html
{% extends "base.html" %}

{% block content %}
<h1>Welcome to the Dashboard</h1>

<button hx-get="/clicked" hx-target="#result-box" hx-swap="innerHTML">
    Click Me Dynamically!
</button>

<div id="result-box">
    <!-- HTMX will inject the server response here -->
</div>
{% endblock %}
```

### app/templates/partials/click_result.html (The Fragment)
This is a raw fragment, not a full HTML document.

```html
<p style="color: green;">Success! Loaded via HTMX at {{ timestamp }}</p>
```

### app/app/main.py (The Backend Backend)

```python
from datetime import datetime
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

app = FastAPI()

# Mount static files (for custom CSS/JS assets)
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# Setup Jinja templates
templates = Jinja2Templates(directory="app/templates")

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/clicked", response_class=HTMLResponse)
async def clicked(request: Request):
    now = datetime.now().strftime("%H:%M:%S")
    # Return ONLY the partial fragment, not the whole page!
    return templates.TemplateResponse("partials/click_result.html", {"request": request, "timestamp": now})

```


------------------------------
## 3. Development Environment Setup
During development, you want rapid iteration without manually restarting servers or refreshing the browser.

* Hot Reloading: Run your application using Uvicorn with the --reload flag and specify the templates directory so it watches your HTML files for changes:

uvicorn app.main:app --reload --reload-dir app

* Template Auto-Reload: You can explicitly force Jinja2 to reload modified files by modifying your instantiation line:

```python
templates = Jinja2Templates(directory="app/templates")
templates.env.auto_reload = True  # Ensures templates refresh instantly on save
```

* CSS Compilation: If you use Tailwind CSS, run the Tailwind CLI watcher concurrently in a separate terminal to compile your CSS into app/static/css/styles.css automatically on file changes.

------------------------------
## 4. Production Environment Setup
Production requires optimization for speed, security, and handling multiple concurrent connections.

* Production WSGI/ASGI Server: Never use --reload in production. Run using Gunicorn wrapping Uvicorn workers to scale across multiple CPU cores:

gunicorn app.main:app -w 4 -k uvicorn.workers.UvicornWorker -b 0.0.0.0:8000

* Self-Host HTMX: Do not use the CDN link (unpkg.com) in production. Download the htmx.min.js file, put it into your app/static/js/ directory, and load it locally. This removes an external network point-of-failure and guarantees your JS file cannot be modified upstream.
* Static File Caching & CDN: FastAPI's StaticFiles is fine for development, but in production, place a reverse proxy like Nginx, Cloudflare, or an AWS CloudFront distribution in front of your FastAPI server. Let Nginx/Cloudflare serve your CSS, JS, and image assets directly. This completely prevents static asset bandwidth from consuming Python server CPU cycles.
* Enable Gzip Compression: Install the standard GzipMiddleware in your FastAPI setup to compress the HTML fragments before sending them over the wire, optimizing network performance:

```python
from fastapi.middleware.gzip import GzipMiddleware
app.add_middleware(GzipMiddleware, minimum_size=1000)
```
