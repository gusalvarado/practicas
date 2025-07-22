from fastapi import APIRouter, File, UploadFile
from utils.s3_uploader import upload_file

routes = APIRouter()

@routes.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    content = await file.read()
    key = f"templates/{file.filename}"
    url = upload_file(bucket, key, content)
    return {"url": url}