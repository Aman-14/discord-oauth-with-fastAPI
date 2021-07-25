from datetime import timedelta

import decouple
from authlib.integrations.starlette_client import OAuth
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse, RedirectResponse
from starlette.config import Config

from app.core import Redis, Discord, db
from app.routers import auth, user
from app.starlette_session import SessionMiddleware
from app.starlette_session.backends import BackendType

app = FastAPI()
config = Config(".env")
oauth = OAuth(config)

oauth.register(Discord.NAME, **Discord.OAUTH_APP_CONFIG)


@app.on_event("startup")
async def on_startup():
    await Redis.init()
    db.connect()
    app.add_middleware(
        SessionMiddleware,
        secret_key=decouple.config("SESSION_SECRET"),
        cookie_name="cookie.sid",
        backend_type=BackendType.aioRedis,
        backend_client=Redis.pool,
        max_age=int(timedelta(days=3).total_seconds())
    )
    app.include_router(auth.router)
    app.include_router(user.router)


@app.get("/clear")
async def clear_session(request: Request):
    request.session.clear()
    return JSONResponse({"session": request.session})


@app.get("/view")
def view_session(request: Request) -> JSONResponse:
    return JSONResponse({"session": request.session})


@app.get("/")
async def root():
    return RedirectResponse(url="auth")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000)  # noqa
