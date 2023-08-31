import os
import secrets
from fastapi import FastAPI
from starlette.responses import FileResponse

import globals
from generators.generator import Generator

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Test"}


@app.get("/g")
async def generate():
    """
    This endpoint generates a floor and returns it in a FileResponse as a json file.
    @return: Floor in json format
    """
    generator = Generator(secrets.token_hex(16), "floor.json")
    generator.generate()
    path = generator.save()
    return FileResponse(path=path, filename="floor.json")
