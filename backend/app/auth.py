from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session

from .database import get_db
from .models import User
from .security import decode_access_token

bearer_scheme = HTTPBearer()

def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
    db: Session = Depends(get_db)
) -> User:

    token = credentials.credentials
    subject = decode_access_token(token)

    if not subject:
        raise HTTPException(
            status_code=401,
            detail="Invalid or expired access token"
        )

    user = db.query(User).filter(User.id == int(subject)).first()

    if not user:
        raise HTTPException(
            status_code=401,
            detail="User no longer exists"
        )

    return user