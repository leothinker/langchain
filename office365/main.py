# main.py
import json
import os
from contextlib import asynccontextmanager
from os import getenv

import requests
import uvicorn
from dotenv import load_dotenv
from fastapi import BackgroundTasks, FastAPI, Request, Response
from fastapi.responses import PlainTextResponse
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


@app.post("/webhook")
async def handle_webhook(request: Request, background: BackgroundTasks):
    if "validationToken" in request.query_params:
        return PlainTextResponse(content=request.query_params["validationToken"])

    payload = await request.json()
    logger.debug(f"🔥 收到 webhook payload: {json.dumps(payload)[:200]}")

    # if payload.get("clientState") != CLIENT_STATE:
    #     logger.warning("clientState 不匹配，可能是测试/伪造请求")
    #     return Response(status_code=400, content="Invalid clientState")

    handle_change(payload)


def handle_change(body: dict):
    """
    这里演示读取最小的字段，你可以在正式环境里再调用 Graph
    再去取完整邮件的详情（subject、from …）。
    """
    logger.info("处理邮件变更")
    for entry in body.get("value", []):
        if entry.get("changeType") != "created":
            continue

        msg_id = entry["resourceData"]["id"]
        subject = entry["resourceData"].get("subject", "(no subject)")
        sender = entry["resourceData"]["from"]["emailAddress"]["address"]
        logger.info(f"📧 模拟邮件 → ID:{msg_id}  Subject:{subject!r}  From:{sender}")
        # TODO：这里可以写入 DB、发到 Slack、调用业务逻辑等


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=APPLICATION_PORT, reload=True)
