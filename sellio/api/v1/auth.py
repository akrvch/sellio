from fastapi import APIRouter

router = APIRouter(prefix="/auth", tags=["AuthV1"])


@router.get("/password_hash")
async def sign_in():
    pass
