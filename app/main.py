from fastapi import FastAPI, BackgroundTasks, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import os
import subprocess
import uvicorn

app = FastAPI() 
app.mount("/static", StaticFiles(directory="app/static"), name="static") 
templates = Jinja2Templates(directory="app/templates")

@app.get("/") 
def read_root(request: Request): 
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/scrape/")
async def run_scrape(request: Request, background_tasks: BackgroundTasks):
    data = await request.json()
    url = data.get("url")
    if url:
        background_tasks.add_task(subprocess.call, ['python', 'scraper.py', url])
        return {"message": "Scraping started!"}
    return {"message": "URL is required!"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)