from fastapi import APIRouter


# --- ROUTE from MAIN FastAPI APP
# remember to include this module in main.py
router = APIRouter()

@router.get("/auth/")
async def get_user():
    return {"user": "authenticated"}
