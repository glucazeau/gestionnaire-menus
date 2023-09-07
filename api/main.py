from fastapi import FastAPI

from dish import list_dishes
from season import list_seasons

app = FastAPI()


@app.get("/dishes")
async def get_dishes():
    return list_dishes()


@app.get("/seasons")
async def seasons():
    return list_seasons()
