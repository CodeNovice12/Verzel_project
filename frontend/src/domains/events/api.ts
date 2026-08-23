const API_URL = "http://127.0.0.1:8000";

export interface SessionData {
  id: string;
  event_id: string;
  starts_at: string;
  venue: string;
  capacity: number;
  price: string;
  mode: "seat_map" | "quantity";
}

export interface EventData {
  id: string;
  organizer_id: string;
  title: string;
  external_ref: string | null;
  category: string;
  sessions: SessionData[];
}

export async function fetchEvents(): Promise<EventData[]> {
  const res = await fetch(`${API_URL}/events`);
  if (!res.ok) throw new Error("Erro ao buscar eventos");
  return res.json();
}