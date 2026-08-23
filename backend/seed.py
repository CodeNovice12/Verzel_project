"""
Script de seed - popula dados de teste conforme exigido pelo edital:
1 organizador, 2 clientes, 1 usuário de portaria, e 1 evento publicado
com sessão de ingressos disponíveis.

Uso: com o backend rodando (uvicorn app.main:app --reload), execute:
    python seed.py
"""
import httpx

BASE_URL = "http://127.0.0.1:8000"


def register(client: httpx.Client, name: str, email: str, password: str, role: str):
    resp = client.post(
        f"{BASE_URL}/auth/register",
        json={"name": name, "email": email, "password": password, "role": role},
    )
    if resp.status_code == 201:
        print(f"✅ Criado: {email} ({role})")
    elif resp.status_code == 409:
        print(f"⏭  Já existe: {email}")
    else:
        print(f"⚠️  Erro ao criar {email}: {resp.status_code} {resp.text}")
    return resp


def login(client: httpx.Client, email: str, password: str) -> str:
    resp = client.post(
        f"{BASE_URL}/auth/login",
        data={"username": email, "password": password},
    )
    resp.raise_for_status()
    return resp.json()["access_token"]


def main():
    with httpx.Client() as client:
        print("== Criando usuários de teste ==")
        register(client, "Lucas Organizador", "organizador@teste.com", "senha123", "organizer")
        register(client, "Cliente Um", "cliente@teste.com", "senha123", "customer")
        register(client, "Cliente Dois", "cliente2@teste.com", "senha123", "customer")
        register(client, "Portaria Verzel", "portaria@teste.com", "senha123", "gate")

        print("\n== Criando evento e sessão publicados ==")
        token_organizer = login(client, "organizador@teste.com", "senha123")
        headers = {"Authorization": f"Bearer {token_organizer}"}

        event_resp = client.post(
            f"{BASE_URL}/events",
            headers=headers,
            json={
                "title": "Duna: Parte Três",
                "external_ref": "tt001",
                "category": "filme",
            },
        )
        if event_resp.status_code == 201:
            event = event_resp.json()
            print(f"✅ Evento criado: {event['id']} - {event['title']}")

            session_resp = client.post(
                f"{BASE_URL}/events/{event['id']}/sessions",
                headers=headers,
                json={
                    "starts_at": "2026-09-20T20:00:00-03:00",
                    "venue": "Cinema Verzel - Sala 2",
                    "capacity": 30,
                    "price": "40.00",
                    "mode": "seat_map",
                },
            )
            if session_resp.status_code == 201:
                session = session_resp.json()
                print(f"✅ Sessão criada: {session['id']} - 30 assentos disponíveis (A1-C10)")
            else:
                print(f"⚠️  Erro ao criar sessão: {session_resp.status_code} {session_resp.text}")
        else:
            print(f"⚠️  Erro ao criar evento (ou já existe): {event_resp.status_code} {event_resp.text}")

    print("\n== Seed finalizado ==")
    print("\nCredenciais de teste:")
    print("  Organizador : organizador@teste.com / senha123")
    print("  Cliente 1   : cliente@teste.com / senha123")
    print("  Cliente 2   : cliente2@teste.com / senha123")
    print("  Portaria    : portaria@teste.com / senha123")


if __name__ == "__main__":
    main()