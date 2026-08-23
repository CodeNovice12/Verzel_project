from abc import ABC, abstractmethod
from pydantic import BaseModel
import httpx

from app.core.config import settings


class CatalogItem(BaseModel):
    external_ref: str
    title: str
    category: str


class CatalogProvider(ABC):
    @abstractmethod
    async def get_now_playing(self) -> list[CatalogItem]:
        ...


class MockCatalogProvider(CatalogProvider):
    async def get_now_playing(self) -> list[CatalogItem]:
        return [
            CatalogItem(external_ref="tt001", title="Duna: Parte Três", category="filme"),
            CatalogItem(external_ref="tt002", title="A Origem do Mal", category="filme"),
            CatalogItem(external_ref="tt003", title="Show da Virada 2026", category="show"),
        ]


class TMDbCatalogProvider(CatalogProvider):
    async def get_now_playing(self) -> list[CatalogItem]:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                "https://api.themoviedb.org/3/movie/now_playing",
                params={"api_key": settings.tmdb_api_key, "language": "pt-BR"},
            )
            response.raise_for_status()
            data = response.json()

        return [
            CatalogItem(external_ref=str(m["id"]), title=m["title"], category="filme")
            for m in data["results"]
        ]