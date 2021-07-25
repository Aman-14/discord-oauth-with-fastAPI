from fastapi import Request

from models import User


async def fetch_user(req: Request):
    print(req.session)
    try:
        user_id = int(req.session.get("data").get("user_id"))
    except (AttributeError, ValueError, TypeError):
        return None
    return await User.find_one({"user_id": user_id})
