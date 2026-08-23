const API_URL = "http://127.0.0.1:8000";

export interface TicketData {
  id: string;
  reservation_id: string;
  qr_signature: string;
  status: "valid" | "used";
}

export async function fetchMyTickets(token: string): Promise<TicketData[]> {
  const res = await fetch(`${API_URL}/tickets/me`, {
    headers: { Authorization: `Bearer ${token}` },
  });
  if (!res.ok) throw new Error("Erro ao buscar ingressos");
  return res.json();
}