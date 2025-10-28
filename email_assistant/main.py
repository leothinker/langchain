# main.py
from contextlib import asynccontextmanager
from os import getenv

import ngrok
import uvicorn
from dotenv import load_dotenv
from fastapi import FastAPI, Request, Response
from loguru import logger
from msal import ConfidentialClientApplication

load_dotenv()

NGROK_AUTH_TOKEN = getenv("NGROK_AUTHTOKEN", "")
APPLICATION_PORT = 5000

AZURE_APP_ID = getenv("AZURE_CLIENT_ID", "")
AZURE_APP_TENANT = getenv("AZURE_TENANT_ID", "")
AZURE_APP_SECRET = getenv("AZURE_CLIENT_SECRET", "")
SCOPES = ["https://graph.microsoft.com/.default"]
REDIRECT_URI = getenv("REDIRECT_URI", "")
msal_app = ConfidentialClientApplication(
    client_id=AZURE_APP_ID,
    client_credential=AZURE_APP_SECRET,
    authority=f"https://login.microsoftonline.com/{AZURE_APP_TENANT}/",
)


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
async def webhook(request: Request):
    logger.info("==================webhook triggered==================")

    params = dict(request.query_params)
    if "validationToken" in params:
        token = params["validationToken"]
        logger.info(f"Validation token received: {token}")
        return Response(content=token, media_type="text/plain")

    body = await request.body()
    try:
        body_str = body.decode("utf-8")
    except Exception:
        body_str = str(body)
    logger.info(f"Webhook body: {body_str}")

    return Response(status_code=200)


@app.post("/lifecycle")
def lifecycle(validationToken: str):
    print("==================lifecycle==================")
    if validationToken:
        return Response(content=validationToken, media_type="text/plain")


@app.get("/oauth2/nativeclient")
async def auth_callback(code: str, state: str | None = None):
    # 用 code 换 token 等逻辑
    print("==================auth_callback==================")
    if not code:
        return {"error": "no code in callback"}

    result = msal_app.acquire_token_by_authorization_code(
        code, scopes=SCOPES, redirect_uri=REDIRECT_URI
    )

    if "access_token" in result:
        access_token = result["access_token"]
        refresh_token = result.get("refresh_token")
        print("✅ 授权成功")
        print("access_token:\n", access_token)
        print("refresh_token:\n", refresh_token)
        return {"message": "Logged in", "access_token": access_token}
    else:
        return {
            "error": result.get("error"),
            "error_description": result.get("error_description"),
        }


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=APPLICATION_PORT, reload=True)
