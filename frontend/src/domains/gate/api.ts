const API_URL = "http://127.0.0.1:8000";

export interface ValidationResult {
  result: "valid" | "invalid" | "already_used" | "wrong_event";
  message: string;
}

export async function validateTicket(
  code: string,
  sessionId: string,
  token: string
): Promise<ValidationResult> {
  const res = await fetch(`${API_URL}/tickets/validate`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      Authorization: `Bearer ${token}`,
    },
    body: JSON.stringify({ code, session_id: sessionId }),
  });
  if (!res.ok) {
    const err = await res.json();
    throw new Error(err.detail || "Erro ao validar ingresso");
  }
  return res.json();
}