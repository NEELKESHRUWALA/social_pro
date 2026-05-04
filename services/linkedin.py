import os
from dotenv import load_dotenv

load_dotenv()

class LinkedInService:
    TOKEN = os.getenv("LINKEDIN_TOKEN")
    API_IP = os.getenv("LINKEDIN_API_IP")

    @staticmethod
    def publish(caption: str, hashtags: str, media_path: str):
        """
        TEAM: IMPLEMENT LINKEDIN API CALL HERE
        Use self.TOKEN and self.API_IP
        """
        print(f"Publishing to LinkedIn at {LinkedInService.API_IP}...")
        return "Success (Mock)"
