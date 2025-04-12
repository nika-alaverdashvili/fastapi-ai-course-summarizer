from datetime import timedelta
from app.schemas.jwt import TokenResponse
from app.utils.security import create_token

def generate_tokens(user) -> TokenResponse:
    """
    Generate access and refresh tokens for a user.
    """
    access_token = create_token(
        data={"sub": user.email, "uuid": str(user.id), "email": user.email},
        expires_delta=timedelta(minutes=2),
        token_type="access"
    )
    refresh_token = create_token(
        data={"sub": user.email, "uuid": str(user.id), "email": user.email},
        expires_delta=timedelta(minutes=15),
        token_type="refresh"
    )
    return TokenResponse.model_validate({
        "access_token": access_token,
        "refresh_token": refresh_token
    })
