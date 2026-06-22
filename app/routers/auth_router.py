from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.user import UserCreate, UserLogin
from app.services.auth_services import (
    create_user,
    authenticate_user,
    create_access_token
)

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)

@router.post("/signup")
def signup(user: UserCreate, db: Session = Depends(get_db)):

    new_user = create_user(
        db,
        user.name,
        user.email,
        user.password
    )

    if not new_user:
        raise HTTPException(400, "Email already exists")

    return {"message": "User created successfully"}

@router.post("/signin")
def signin(
    user: UserLogin,
    db: Session = Depends(get_db)
):
    authenticated_user = authenticate_user(
        db,
        user.email,
        user.password
    )

    if not authenticated_user:
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )

    token = create_access_token(
        {"sub": authenticated_user.email}
    )

    return {
        "message": "Signed In Successfully",
        "data": {
            "name": authenticated_user.name,
            "email": authenticated_user.email
        },
        "code": 200,
        "access_token": token,
        "token_type": "bearer"
    }