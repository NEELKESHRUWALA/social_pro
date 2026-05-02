import requests
import time
from fastapi import HTTPException


class InstagramService:
    BASE_URL = "https://graph.facebook.com/v25.0"

    @staticmethod
    def wait_for_processing(creation_id, token, timeout=300):
        url = f"{InstagramService.BASE_URL}/{creation_id}"
        start = time.time()

        while True:
            res = requests.get(url, params={
                "fields": "status_code",
                "access_token": token
            })

            data = res.json()
            status = data.get("status_code")

            print("Status:", status)

            if status == "FINISHED":
                return True
            elif status == "ERROR":
                return False

            if time.time() - start > timeout:
                return False

            time.sleep(5)

    # ✅ IMAGE (FILE INPUT)
    @staticmethod
    def post_image(ig_user_id: str, token: str, image_url: str, caption: str):

        try:
            # Step 2: Create container
            create_url = f"{InstagramService.BASE_URL}/{ig_user_id}/media"

            create_res = requests.post(create_url, data={
                "image_url": image_url,
                "caption": caption,
                "access_token": token
            })

            create_data = create_res.json()
            print("Create:", create_data)

            creation_id = create_data.get("id")
            if not creation_id:
                raise HTTPException(status_code=400, detail=create_data)

            time.sleep(2)

            # Step 3: Publish
            publish_res = requests.post(
                f"{InstagramService.BASE_URL}/{ig_user_id}/media_publish",
                data={
                    "creation_id": creation_id,
                    "access_token": token
                }
            )

            return publish_res.json()

        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    # ✅ VIDEO (FILE INPUT → REELS)
    @staticmethod
    def post_video(ig_user_id: str, token: str, video_url: str, caption: str):

        try:
            create_res = requests.post(
                f"{InstagramService.BASE_URL}/{ig_user_id}/media",
                data={
                    "video_url": video_url,
                    "caption": caption,
                    "media_type": "REELS",
                    "access_token": token
                }
            )

            create_data = create_res.json()
            print("Create Reel:", create_data)

            creation_id = create_data.get("id")
            if not creation_id:
                raise HTTPException(status_code=400, detail=create_data)

            # Step 3: Wait processing
            if not InstagramService.wait_for_processing(creation_id, token):
                raise HTTPException(status_code=400, detail="Video processing failed")

            # Step 4: Publish
            publish_res = requests.post(
                f"{InstagramService.BASE_URL}/{ig_user_id}/media_publish",
                data={
                    "creation_id": creation_id,
                    "access_token": token
                }
            )

            return publish_res.json()

        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))