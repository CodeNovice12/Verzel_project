from fastapi import HTTPException, status

from app.domains.auth.models import User
from app.domains.auth.repository import UserRepository
from app.domains.auth.schemas import UserCreate
from app.domains.auth.security import hash_password, verify_password, create_access_token


class AuthService:
    def __init__(self, repository: UserRepository):
        self.repository = repository

    async def register(self, data: UserCreate) -> User:
        existing = await self.repository.get_by_email(data.email)
        if existing:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="E-mail já cadastrado",
            )
        user = User(
            name=data.name,
            email=data.email,
            password_hash=hash_password(data.password),
            role=data.role,
        )
        return await self.repository.create(user)

    async def authenticate(self, email: str, password: str) -> str:
        user = await self.repository.get_by_email(email)
        if not user or not verify_password(password, user.password_hash):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Credenciais inválidas",
            )
        return create_access_token(subject=str(user.id), role=user.role.value)