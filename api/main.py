from fastapi import FastAPI, Request, UploadFile, File, Form, HTTPException
from fastapi.responses import FileResponse, JSONResponse, HTMLResponse, StreamingResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from classes.dunder_bot import DunderBot


class Base(BaseModel):
    user_input: str
    mode: str = "basic"

app = FastAPI()

try:
    dunder_bot = DunderBot()
except Exception as e:
    print(f"Error initializing modules : {e}")


# initialize templates
app.mount("/static", StaticFiles(directory="public/static"), name="static")
templates = Jinja2Templates(directory="public")


@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    """
    Endpoint to render the homepage.
    """
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/api/ask")
def stream_response(input: Base):
    user_input = input.user_input
    mode = input.mode
    if(mode == "optimized_query"):
        print("Running optimized query reponse mode...")
        return StreamingResponse(dunder_bot.answer_this_with_expertise(user_query=user_input))
    if(mode == "agentic"):
        print("Running agentic reponse mode...")
        return StreamingResponse(dunder_bot.answer_this_with_agent(user_query=user_input))
    
    ## default to basic mode 
    print("Running basic reponse mode...")
    return StreamingResponse(dunder_bot.answer_me_this(user_query=user_input))
