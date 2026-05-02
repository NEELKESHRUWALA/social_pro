import requests
import json

def upload_file(file,file_name,extension):
    nova_url = "https://novaoffice.novasoftwares.com/service.aspx"

    # 🔹 Same JSON as Flutter
    data_param = json.dumps({
        "folderName": "uploads",
        "description": "social media uploads",
        "MasterId": "1",
        "DetId": "1",
        "extension": extension,
        "filename": file_name
    })

    # 🔹 Same query params
    params = {
        "ApiVer": "1",
        "DeviceId": "0",
        "AppId": "WA01",
        "Lat": "0",
        "Lng": "0",
        "Control": "Upload",
        "data": data_param,
        "filename": file_name,
        "folderName": "uploads"
    }

    response = requests.post(nova_url, params=params, files=file)

    print("Status:", response.status_code)
    print("Response:", response.text)

    if response.status_code == 200:
        res = response.json()
        if res.get("success"):
            return res.get("data", {}).get("filename")
        else:
            print("Upload failed:", res.get("message"))
            return None
    else:
        print("Server error:", response.status_code)
        return None

# file_path = r"C:\Users\USM\Downloads\Diwali__1777014202.png"
#
# files = {
#     "file": ("Diwali__1777014202.png", open(file_path, "rb"), "image/jpeg")
# }
#
# result = upload_file(
#     file=files,
#     file_name="Diwali__1777014202.png",
#     extension=".png"
# )
#
# print("Uploaded filename:", result)


def upload_file_main(file_obj, file_name, extension):
    nova_url = "https://novaoffice.novasoftwares.com/service.aspx"

    data_param = json.dumps({
        "folderName": "uploads",
        "description": "social media uploads",
        "MasterId": 1,
        "DetId": 1,
        "extension": extension,
        "filename": file_name
    })

    params = {
        "ApiVer": "1",
        "DeviceId": "0",
        "AppId": "WA01",
        "Lat": "0",
        "Lng": "0",
        "Control": "Upload",
        "data": data_param,
        "filename": file_name,
        "folderName": "uploads"
    }

    files = {
        "file": (file_name, file_obj, "application/octet-stream")
    }

    response = requests.post(nova_url, params=params, files=files)

    if response.status_code == 200:
        res = response.json()
        if res.get("success"):
            return res.get("data", {}).get("filename")

    return None
