# web_interface.py
# FastAPI app for interactive DSPy llms.txt generation with descriptive save filenames
#
# Functional Purpose:
#   - Accept a GitHub repo URL input
#   - Generate llms.txt content using DSPy pipeline (synchronously)
#   - Display generated content for preview
#   - Save content to disk with filename derived from repo URL on user action

import re
from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import uvicorn

from generate_llms import generate_llms_txt_for_dspy

app = FastAPI()
templates = Jinja2Templates(directory="templates")


def repo_url_to_filename(repo_url: str) -> str:
    """
    Convert a GitHub repo URL to a safe filename.

    E.g., 'https://github.com/stanfordnlp/dspy' -> 'stanfordnlp_dspy_llms.txt'
    """
    parts = repo_url.rstrip("/").split("/")
    if len(parts) < 2:
        raise ValueError("Invalid repo URL format.")
    owner = parts[-2]
    repo = parts[-1]
    safe_name = re.sub(r"[^a-zA-Z0-9_]+", "_", f"{owner}_{repo}")
    return f"{safe_name}_llms.txt"


@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    # Initial page load with empty form
    return templates.TemplateResponse(
        "index.html",
        {"request": request, "result": None, "error": None, "saved": False},
    )


@app.post("/generate", response_class=HTMLResponse)
def generate(request: Request, repo_url: str = Form(...)):
    """
    Handle Generate button:
    - Run DSPy pipeline to generate llms.txt content for given repo URL
    - Return content for display without saving
    """
    try:
        result = generate_llms_txt_for_dspy(repo_url=repo_url)
        llms_content = result.llms_txt_content
        return templates.TemplateResponse(
            "index.html",
            {
                "request": request,
                "result": llms_content,
                "error": None,
                "saved": False,
                "repo_url": repo_url,  # pass repo_url back for Save form
            },
        )
    except Exception as e:
        return templates.TemplateResponse(
            "index.html",
            {
                "request": request,
                "result": None,
                "error": str(e),
                "saved": False,
                "repo_url": repo_url,
            },
        )


@app.post("/save", response_class=HTMLResponse)
def save(
    request: Request, llms_txt_content: str = Form(...), repo_url: str = Form(...)
):
    """
    Handle Save button:
    - Save the displayed llms.txt content to disk with filename based on repo URL
    - Show success or error message
    """
    try:
        filename = repo_url_to_filename(repo_url)
        with open(filename, "w") as f:
            f.write(llms_txt_content)
        message = f"Saved llms.txt as {filename}!"
        return templates.TemplateResponse(
            "index.html",
            {
                "request": request,
                "result": llms_txt_content,
                "error": None,
                "saved": True,
                "message": message,
                "repo_url": repo_url,
            },
        )
    except Exception as e:
        return templates.TemplateResponse(
            "index.html",
            {
                "request": request,
                "result": llms_txt_content,
                "error": str(e),
                "saved": False,
                "repo_url": repo_url,
            },
        )


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
