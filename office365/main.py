# main.py
from contextlib import asynccontextmanager
from os import getenv

import uvicorn
from dotenv import load_dotenv
from fastapi import FastAPI
from loguru import logger

import ngrok

load_dotenv()

NGROK_AUTH_TOKEN = getenv("NGROK_AUTHTOKEN", "")
APPLICATION_PORT = 5000


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Setting up Ngrok Endpoint")
    ngrok.set_auth_token(NGROK_AUTH_TOKEN)
    ngrok.forward(
        addr=APPLICATION_PORT,
    )
    yield
    logger.info("Tearing Down Ngrok Endpoint")
    ngrok.disconnect()


app = FastAPI(lifespan=lifespan)


@app.get("/")
async def root():
    return {"message": "Hello World"}


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=APPLICATION_PORT, reload=True)
