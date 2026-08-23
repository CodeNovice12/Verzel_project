from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.domains.auth.repository import UserRepository
from app.domains.auth.schemas import UserCreate, UserOut, Token
from app.domains.auth.service import AuthService

from app.domains.auth.dependencies import get_current_user
from app.domains.auth.models import User

# ... resto do arquivo

router = APIRouter(prefix="/auth", tags=["auth"])


def get_auth_service(db: AsyncSession = Depends(get_db)) -> AuthService:
    return AuthService(UserRepository(db))


@router.post("/register", response_model=UserOut, status_code=201)
async def register(data: UserCreate, service: AuthService = Depends(get_auth_service)):
    return await service.register(data)


@router.post("/login", response_model=Token)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    service: AuthService = Depends(get_auth_service),
):
    token = await service.authenticate(form_data.username, form_data.password)
    return Token(access_token=token)

@router.get("/me", response_model=UserOut)
async def me(current_user: User = Depends(get_current_user)):
    return current_user
