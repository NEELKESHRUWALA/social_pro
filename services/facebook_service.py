import requests
from fastapi import HTTPException, UploadFile


class FacebookService:
    BASE_URL = "https://graph.facebook.com/v25.0"

    @staticmethod
    def _handle_response(response):
        try:
            res_json = response.json()
        except Exception:
            raise HTTPException(status_code=500, detail="Invalid response from Facebook")

        if response.status_code != 200:
            raise HTTPException(
                status_code=response.status_code,
                detail=res_json
            )

        return res_json

    @staticmethod
    def post_text(page_id: str, access_token: str, text: str):
        url = f"{FacebookService.BASE_URL}/{page_id}/feed"

        payload = {
            "message": text,
            "access_token": access_token
        }

        try:
            response = requests.post(url, data=payload)
            return FacebookService._handle_response(response)

        except requests.exceptions.RequestException as e:
            raise HTTPException(status_code=500, detail=str(e))


    @staticmethod
    def post_image(page_id: str, access_token: str, file: UploadFile, caption: str):
        url = f"{FacebookService.BASE_URL}/{page_id}/photos"

        try:
            files = {
                "source": (file.filename, file.file, file.content_type)
            }

            data = {
                "caption": caption,
                "access_token": access_token
            }

            response = requests.post(url, files=files, data=data)
            return FacebookService._handle_response(response)

        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))


    @staticmethod
    def post_video(page_id: str, access_token: str, file: UploadFile, description: str):
        url = f"{FacebookService.BASE_URL}/{page_id}/videos"

        try:
            files = {
                "source": (file.filename, file.file, file.content_type)
            }

            data = {
                "description": description,
                "access_token": access_token
            }

            response = requests.post(url, files=files, data=data)
            return FacebookService._handle_response(response)

        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
