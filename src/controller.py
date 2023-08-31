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


@app.get("/g/{floor_id}")
async def generate_with_id(floor_id: int) -> FileResponse:
    """
    This endpoint generates a floor with the given id and returns it in a FileResponse as a json file.
    @param floor_id id for the floor
    @return: Floor in json file
    """
    generator = Generator(secrets.token_hex(16), "floor.json", floor_id)
    generator.generate()
    path = generator.save()
    return FileResponse(path=path, filename="floor.json")


@app.get("/g")
async def generate() -> FileResponse:
    """
    This endpoint generates a floor with the id zero and returns it as a json file.
    @return: Floor as json file
    """
    generator = Generator(secrets.token_hex(16), "floor.json", 0)
    generator.generate()
    path = generator.save()
    return FileResponse(path=path, filename="floor.json")
