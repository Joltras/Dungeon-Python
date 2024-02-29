import secrets

from fastapi import FastAPI
from starlette.responses import FileResponse

import globals
from generators.generator import Generator

app = FastAPI()
_file_name = globals.DEFAULT_FLOOR_NAME + globals.JSON_SUFFIX


@app.get("/")
async def root():
    return {"message": "Test"}


@app.get("/gen/{floor_id}")
async def generate_with_id(floor_id: int) -> FileResponse:
    """
    This endpoint generates a floor with the given id and returns it in a FileResponse as a json file.
    @param floor_id id for the floor
    @return: Floor in json file
    """
    generator = Generator(
        seed=secrets.token_hex(16), output_file_name=_file_name, stage_id=floor_id
    )
    generator.generate()
    path = generator.save()
    return FileResponse(path=path, filename=_file_name)


@app.get("/gen/{floor_id}/{seed}")
async def generate_with_id_and_seed(floor_id: int, seed: str) -> FileResponse:
    """
    This endpoint generates a floor with the given id and seed and returns it in a FileResponse as a json file.
    @param floor_id: id for the floor
    @param seed: seed for the floor
    @return: Floor in json file
    """
    generator = Generator(seed=seed, output_file_name=_file_name, stage_id=floor_id)
    generator.generate()
    path = generator.save()
    return FileResponse(path=path, filename=_file_name)


@app.get("/gen")
async def generate() -> FileResponse:
    """
    This endpoint generates a floor with the id zero and returns it as a json file.
    @return: Floor as json file
    """
    generator = Generator(
        seed=secrets.token_hex(16), output_file_name=_file_name, stage_id=0
    )
    generator.generate()
    path = generator.save()
    return FileResponse(path=path, filename=_file_name)
