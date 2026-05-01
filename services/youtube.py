import os
from dotenv import load_dotenv

load_dotenv()

class YouTubeService:
    TOKEN = os.getenv("YOUTUBE_TOKEN")
    API_IP = os.getenv("YOUTUBE_API_IP")

    @staticmethod
    def publish(caption: str, hashtags: str, media_path: str):
        """
        TEAM: IMPLEMENT YOUTUBE API CALL HERE
        Use self.TOKEN and self.API_IP
        Note: YouTube only accepts video media.
        """
        print(f"Publishing to YouTube at {YouTubeService.API_IP}...")
        return "Success (Mock)"
