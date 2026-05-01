from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import os
from typing import List

# Import our simple platform services
from services.instagram import InstagramService
from services.facebook import FacebookService
from services.linkedin import LinkedInService
from services.youtube import YouTubeService

app = FastAPI(title="Social Pro Backend")

# Enable CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/api/publish")
async def publish(
    caption: str = Form(...),
    hashtags: str = Form(""),
    platforms: str = Form(...), # JSON string or comma-separated
    media: UploadFile = File(None)
):
    """
    Unified endpoint to publish to multiple platforms.
    Your team just needs to fill the tokens in .env
    """
    target_platforms = platforms.split(",")
    results = []
    
    # Handle media saving
    media_path = None
    if media:
        if not os.path.exists("uploads"):
            os.makedirs("uploads")
        media_path = os.path.join("uploads", media.filename)
        with open(media_path, "wb") as f:
            f.write(await media.read())

    # --- TEAM: INTEGRATE REAL API CALLS HERE ---
    for platform in target_platforms:
        p = platform.strip().lower()
        status = "Unknown Platform"
        
        if p == "instagram":
            status = InstagramService.publish(caption, hashtags, media_path)
        elif p == "facebook":
            status = FacebookService.publish(caption, hashtags, media_path)
        elif p == "linkedin":
            status = LinkedInService.publish(caption, hashtags, media_path)
        elif p == "youtube":
            status = YouTubeService.publish(caption, hashtags, media_path)
            
        results.append({"platform": p, "status": status})

    return {
        "message": "Publishing process initiated",
        "details": results
    }

@app.get("/api/analytics")
async def get_analytics():
    """
    Returns data for the Dashboard charts.
    """
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

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
