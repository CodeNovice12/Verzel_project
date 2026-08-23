import httpx

BASE_URL = "http://127.0.0.1:8000"

# 1. Login como cliente
login_cliente = httpx.post(
    f"{BASE_URL}/auth/login",
    data={"username": "cliente@teste.com", "password": "senha123"},
)
token_cliente = login_cliente.json()["access_token"]

# 2. Pega os tickets do cliente
tickets = httpx.get(
    f"{BASE_URL}/tickets/me",
    headers={"Authorization": f"Bearer {token_cliente}"},
)
print("Tickets do cliente:", tickets.json())

qr_signature = tickets.json()[0]["qr_signature"]
print("\nQR signature extraído:", qr_signature[:50], "...")

# 3. Login como portaria
login_portaria = httpx.post(
    f"{BASE_URL}/auth/login",
    data={"username": "portaria@teste.com", "password": "senha123"},
)
token_portaria = login_portaria.json()["access_token"]

# 4. Valida o ticket (primeira vez - deve dar "valid")
validate1 = httpx.post(
    f"{BASE_URL}/tickets/validate",
    headers={"Authorization": f"Bearer {token_portaria}"},
    json={"code": qr_signature, "session_id": "d78ed368-0692-4120-9904-b9ee06742b2d"},
)
print("\n1ª validação:", validate1.json())

# 5. Valida de novo (segunda vez - deve dar "already_used")
validate2 = httpx.post(
    f"{BASE_URL}/tickets/validate",
    headers={"Authorization": f"Bearer {token_portaria}"},
    json={"code": qr_signature, "session_id": "d78ed368-0692-4120-9904-b9ee06742b2d"},
)
print("2ª validação:", validate2.json())