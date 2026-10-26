from fastapi import APIRouter

router = APIRouter(prefix="/api/auth", tags=["Authentication"])

@router.get("/status")
def auth_status():
    return {
        "enabled": False,
        "message": "Authentication is not enabled in this hackathon MVP. Add verified login and authorization before using real client data."
    }
