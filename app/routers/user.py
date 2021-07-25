from fastapi import APIRouter, Depends

from dependencies import fetch_user
from models import User

router = APIRouter(
    prefix="/user"
)


@router.get("/")
async def get_user(user: User = Depends(fetch_user)):
    print(user)
    return user
