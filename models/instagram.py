from pydantic import BaseModel
from fastapi import Form


class IgImagePost(BaseModel):
    image_url: str | None = None   # will be filled after upload
    caption: str
    access_token: str
    ig_user_id: str

    @classmethod
    def as_form(
        cls,
        caption: str = Form(""),
        access_token: str = Form(...),
        ig_user_id: str = Form(...)
    ):
        return cls(
            caption=caption,
            access_token=access_token,
            ig_user_id=ig_user_id
        )


class IgVideoPost(BaseModel):
    video_url: str | None = None
    caption: str
    access_token: str
    ig_user_id: str

    @classmethod
    def as_form(
        cls,
        caption: str = Form(""),
        access_token: str = Form(...),
        ig_user_id: str = Form(...)
    ):
        return cls(
            caption=caption,
            access_token=access_token,
            ig_user_id=ig_user_id
        )