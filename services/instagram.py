import os
from dotenv import load_dotenv

load_dotenv()

class InstagramService:
    TOKEN = os.getenv("INSTAGRAM_TOKEN")
    API_IP = os.getenv("INSTAGRAM_API_IP")

    @staticmethod
    def publish(caption: str, hashtags: str, media_path: str):
        """
        TEAM: IMPLEMENT INSTAGRAM API CALL HERE
        Use self.TOKEN and self.API_IP
        """
        print(f"Publishing to Instagram at {InstagramService.API_IP}...")
        
        # Example using requests:
        # response = requests.post(f"http://{InstagramService.API_IP}/v1/media", 
        #                         data={"caption": f"{caption} {hashtags}"},
        #                         headers={"Authorization": f"Bearer {InstagramService.TOKEN}"})
        
        return "Success (Mock)"
