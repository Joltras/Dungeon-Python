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
    generator = Generator(secrets.token_hex(16), "floor.json")
    generator.generate()
    generator.save()
    path = os.path.join(Globals.APPLICATION_PATH, "generation/floor.json")
    return FileResponse(path=path, filename="floor.json")
