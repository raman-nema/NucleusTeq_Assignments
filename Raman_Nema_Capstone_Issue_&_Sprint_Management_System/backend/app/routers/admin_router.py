from fastapi import APIRouter
from fastapi import Depends
from app.dependencies.authorization import require_admin

router = APIRouter(prefix="/admin", tags=["Admin"])


@router.get("/dashboard")
def admin_dashboard(current_user=Depends(require_admin)):
    return {
        "success": True,
        "message": "Welcome to Admin Dashboard",
        "data": {
            "name": current_user["name"],
            "email": current_user["email"],
            "role": current_user["role"],
        },
    }
