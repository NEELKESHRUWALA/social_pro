from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import shutil
import os
from fastapi import FastAPI, UploadFile, File, Depends, HTTPException

from models.facebook import *
from services.YouTubeUploaderBase import YouTubeUploaderBase
from services.facebook_service import FacebookService
from services.instagram import InstagramService
from services.file_upload import *
from models.instagram import *


app = FastAPI(title="Social Pro Backend")

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# Enable CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/api/analytics")
async def get_analytics():
    return {
        "reach": [12000, 19000, 15000, 25000, 22000, 30000, 35000],
        "engagement": [40, 25, 15, 20],
        "stats": {
            "total_reach": "128.4K",
            "engagement_rate": "4.8%",
            "video_views": "85.2K",
            "new_followers": "+2.4K"
        }
    }



@app.post("/fb/text_post")
async def fb_text_post(data: FbTextPost):
    return FacebookService.post_text(
        page_id=data.page_id,
        access_token=data.access_token,
        text=data.text
    )

@app.post("/fb/image_post")
async def fb_image_post(data: FbImagePost = Depends(FbImagePost.as_form),file: UploadFile = File(...)):
    return FacebookService.post_image(
        page_id=data.page_id,
        access_token=data.access_token,
        file=file,
        caption=data.caption
    )

@app.post("/fb/video_post")
async def fb_video_post(data: FbVideoPost = Depends(FbVideoPost.as_form),file: UploadFile = File(...)):
    return FacebookService.post_video(
        page_id=data.page_id,
        access_token=data.access_token,
        file=file,
        description=data.description
    )


@app.post("/ig/image_post")
async def ig_image_post(data: IgImagePost = Depends(IgImagePost.as_form),file: UploadFile = File(...)):
    filename = file.filename
    extension = filename.split(".")[-1]

    uploaded_name = upload_file_main(
        file.file,
        filename,
        extension
    )

    if uploaded_name:
        data.image_url = f"https://novaoffice.novasoftwares.com/WA01/uploads/{uploaded_name}"

        return InstagramService.post_image(
            ig_user_id=data.ig_user_id,
            token=data.access_token,
            image_url=data.image_url,
            caption=data.caption
        )
    raise HTTPException(status_code=500, detail="Failed to Post on Instagram")

@app.post("/ig/video_post")
async def ig_video_post(data: IgVideoPost = Depends(IgVideoPost.as_form),file: UploadFile = File(...)):
    # video_url = save_upload_file(file)
    filename = file.filename
    extension = filename.split(".")[-1]

    uploaded_name = upload_file_main(
        file.file,
        filename,
        extension
    )

    if uploaded_name:
        data.image_url = f"https://novaoffice.novasoftwares.com/WA01/uploads/{uploaded_name}"

        return InstagramService.post_video(
            ig_user_id=data.ig_user_id,
            token=data.access_token,
            video_url=data.video_url,
            caption=data.caption
        )
    raise HTTPException(status_code=500, detail="Failed to Post on Instagram")


@app.post("/yt/upload")
async def yt_upload_video(
    video: UploadFile = File(...),
    client_json: UploadFile = File(...),
    title: str = Form(...),
    description: str = Form(...),
    tags: str = Form("")
):
    try:
        # Save files
        video_path = os.path.join(UPLOAD_DIR, video.filename)
        with open(video_path, "wb") as f:
            shutil.copyfileobj(video.file, f)

        client_path = os.path.join(UPLOAD_DIR, "client.json")
        with open(client_path, "wb") as f:
            shutil.copyfileobj(client_json.file, f)

        # Initialize uploader
        uploader = YouTubeUploaderBase(client_path)

        # Upload
        response = uploader.upload(
            file_path=video_path,
            title=title,
            description=description,
            category_id="22",
            privacy="public",
            tags=tags.split(",") if tags else []
        )

        return {
            "message": "Uploaded successfully",
            "video_id": response["id"]
        }

    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
