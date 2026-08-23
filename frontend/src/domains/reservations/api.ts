const API_URL = "http://127.0.0.1:8000";

export interface ReservationData {
  id: string;
  session_id: string;
  customer_id: string;
  seat_id: string | null;
  quantity: number | null;
  status: string;
}

export interface PaymentResult {
  reservation_id: string;
  status: string;
  message: string;
  ticket_id: string | null;
}

export async function fetchSeats(sessionId: string, token: string) {
  const res = await fetch(`${API_URL}/reservations/sessions/${sessionId}/seats`, {
    headers: { Authorization: `Bearer ${token}` },
  });
  if (!res.ok) throw new Error("Erro ao buscar assentos");
  return res.json();
}

export async function createReservation(
  sessionId: string,
  seatId: string,
  token: string
): Promise<ReservationData> {
  const res = await fetch(`${API_URL}/reservations`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      Authorization: `Bearer ${token}`,
    },
    body: JSON.stringify({ session_id: sessionId, seat_id: seatId }),
  });
  if (!res.ok) {
    const err = await res.json();
    throw new Error(err.detail || "Erro ao reservar");
  }
  return res.json();
}

export async function payReservation(
  reservationId: string,
  token: string
): Promise<PaymentResult> {
  const res = await fetch(`${API_URL}/reservations/${reservationId}/pay`, {
    method: "POST",
    headers: { Authorization: `Bearer ${token}` },
  });
  if (!res.ok) {
    const err = await res.json();
    throw new Error(err.detail || "Erro ao processar pagamento");
  }
  return res.json();
}