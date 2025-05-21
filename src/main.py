import uvicorn
from fastapi import FastAPI

from routes.routes import *

app = FastAPI()
app.include_router(homepage, prefix="/homepage")


if __name__ == "__main__":
    uvicorn.run("main:app", host="localhost", port=8000, reload=True)
