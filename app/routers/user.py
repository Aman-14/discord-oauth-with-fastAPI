from fastapi import APIRouter, Depends

from app.dependencies import fetch_user
from app.models import User

router = APIRouter(
    prefix="/user"
)


@router.get("/")
async def get_user(user: User = Depends(fetch_user)):
    print(user)
    return user
