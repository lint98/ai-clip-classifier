# main.py
from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from app.classify import classify_images
from app.slideshow import generate_slideshow
from fastapi.responses import FileResponse

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/ping")
async def ping():
    return {"message": "pong"}

@app.post("/classify")
async def classify(files: list[UploadFile] = File(...)):
    results = await classify_images(files)
    return {"results": results}

@app.post("/generate-slideshow")
async def generate_slideshow_api(
    files: list[UploadFile] = File(...),
    prompt: str = Form("")
):
    video_path = await generate_slideshow(files, prompt)
    return FileResponse(video_path, media_type="video/mp4", filename="slideshow.mp4")
