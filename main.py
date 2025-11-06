import os
import shutil
from typing import Union
from fastapi import FastAPI, UploadFile
from db import save_image_info, find_closest_images
from vectorizer import get_image_embedding, get_text_embedding
from pydantic import BaseModel, Field

UPLOAD_DIR = "./images/"

app = FastAPI()

class Response(BaseModel):
    embedding: str = Field(
        ...,
        title="Embedding",
        description="Vector embedding as a list of floats in string format",
        example="[-0.0123456789, 0.0234567890, ... "
        )


@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.post("/image_embedding/", response_model=Response, responses={200: {"model": Response}})
async def get_image_vector(file: UploadFile):
    image_bytes = await file.read()
    embedding = get_image_embedding(image_bytes)

    return Response(embedding=embedding)

@app.post("/text_embedding/", response_model=Response, responses={200: {"model": Response}})
async def get_text_vector(text):
    embedding = get_text_embedding(text)

    return {"embedding": embedding}

@app.post("/images/store")
async def upload_image(file: UploadFile):
    file_location = os.path.join(UPLOAD_DIR, file.filename)

    try:
        with open(file_location, "wb+") as file_object:
            shutil.copyfileobj(file.file, file_object)
    except Exception as e:
            return {"message": f"There was an error uploading the file: {e}"}
    finally:
            file.file.seek(0)  # Reset file pointer to the beginning
            image_bytes = await file.read()
            embedding = get_image_embedding(image_bytes)
            save_image_info(file.filename, embedding)
            await file.close() # Ensure the uploaded file is closed

    return {"info": f"file '{file.filename}' saved at '{file_location}'"}

@app.post("/images/closest_by_image")
async def get_closest_images_by_image(file: UploadFile):
    image_bytes = await file.read()
    embedding = get_image_embedding(image_bytes)
    closest_images = find_closest_images(embedding)

    return {"closest_images": closest_images}

@app.get("/images/closest_by_text")
async def get_closest_images_by_text(text: str):
    embedding = get_text_embedding(text)
    closest_images = find_closest_images(embedding)

    return {"closest_images": closest_images}