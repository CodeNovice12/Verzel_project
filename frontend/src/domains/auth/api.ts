const API_URL = "http://127.0.0.1:8000";

export async function loginRequest(email: string, password: string): Promise<string> {
  const body = new URLSearchParams();
  body.append("username", email);
  body.append("password", password);

  const res = await fetch(`${API_URL}/auth/login`, {
    method: "POST",
    headers: { "Content-Type": "application/x-www-form-urlencoded" },
    body,
  });

  if (!res.ok) throw new Error("Credenciais inválidas");
  const data = await res.json();
  return data.access_token;
}

export async function registerRequest(
  name: string,
  email: string,
  password: string,
  role: string
) {
  const res = await fetch(`${API_URL}/auth/register`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ name, email, password, role }),
  });

  if (!res.ok) {
    const err = await res.json();
    throw new Error(err.detail || "Erro ao registrar");
  }
  return res.json();
}