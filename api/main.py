from fastapi import FastAPI, Request, UploadFile, File, Form, HTTPException
from fastapi.responses import FileResponse, JSONResponse, HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles


app = FastAPI()

# initialize templates
app.mount("/static", StaticFiles(directory="public/static"), name="static")
templates = Jinja2Templates(directory="public")


@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    """
    Endpoint to render the homepage.
    """
    return templates.TemplateResponse("index.html", {"request": request})
