from fastapi import APIRouter, Request

from app.core import Discord
from app.main import oauth
from app.models import User

router = APIRouter(
    prefix="/auth"
)


@router.get("/")
async def auth(req: Request):
    redirect_uri = req.url_for("redirect")
    return await oauth.discord.authorize_redirect(req, redirect_uri)


@router.get("/redirect")
async def redirect(request: Request):
    payload = await oauth.discord.authorize_access_token(request)
    res = await oauth.discord.get(f"{Discord.BASE_URL}/users/@me", token=payload)
    user = res.json()
    request.session.update({"data": {"user_id": user.get("id")}})
    user.update(payload)
    await User.create(
        user_id=user["id"],
        access_token=user["access_token"],
        refresh_token=user["refresh_token"]
    )
    return payload
