class YouTubeUploaderBase:
    def __init__(self, client_secrets_file, token_file="token.json"):
        self.client_secrets_file = client_secrets_file
        self.token_file = token_file
        self.scopes = ["https://www.googleapis.com/auth/youtube.upload"]
        self.youtube = self.authenticate()

    def authenticate(self):
        from google.oauth2.credentials import Credentials
        from google_auth_oauthlib.flow import InstalledAppFlow
        from google.auth.transport.requests import Request
        from googleapiclient.discovery import build
        import os

        creds = None

        if os.path.exists(self.token_file):
            creds = Credentials.from_authorized_user_file(
                self.token_file, self.scopes
            )

        if not creds or not creds.valid:
            if creds and creds.expired:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    self.client_secrets_file,
                    self.scopes
                )
                creds = flow.run_local_server(port=8080)

            with open(self.token_file, "w") as f:
                f.write(creds.to_json())

        return build("youtube", "v3", credentials=creds)

    def upload(self, file_path, title, description, category_id, privacy, tags):
        from googleapiclient.http import MediaFileUpload

        request = self.youtube.videos().insert(
            part="snippet,status",
            body={
                "snippet": {
                    "title": title,
                    "description": description,
                    "tags": tags,
                    "categoryId": category_id
                },
                "status": {
                    "privacyStatus": privacy
                }
            },
            media_body=MediaFileUpload(file_path, resumable=True)
        )

        response = None
        while response is None:
            status, response = request.next_chunk()
            if status:
                print(f"{int(status.progress()*100)}% uploaded")

        return response