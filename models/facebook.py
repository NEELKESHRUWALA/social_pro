from pydantic import BaseModel
from fastapi import Form


class FbTextPost(BaseModel):
    text: str
    access_token: str
    page_id: str


class FbImagePost(BaseModel):
    caption: str
    access_token: str
    page_id: str

    @classmethod
    def as_form(
        cls,
        caption: str = Form(""),
        access_token: str = Form(...),
        page_id: str = Form(...)
    ):
        return cls(
            caption=caption,
            access_token=access_token,
            page_id=page_id
        )


class FbVideoPost(BaseModel):
    description: str
    access_token: str
    page_id: str

    @classmethod
    def as_form(
        cls,
        description: str = Form(""),
        access_token: str = Form(...),
        page_id: str = Form(...)
    ):
        return cls(
            description=description,
            access_token=access_token,
            page_id=page_id
        )
