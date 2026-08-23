const API_URL = "http://127.0.0.1:8000";

export interface CatalogItem {
  external_ref: string;
  title: string;
  category: string;
}

export async function fetchCatalog(): Promise<CatalogItem[]> {
  const res = await fetch(`${API_URL}/events/catalog`);
  if (!res.ok) throw new Error("Erro ao buscar catálogo");
  return res.json();
}

export async function createEvent(
  title: string,
  externalRef: string,
  category: string,
  token: string
) {
  const res = await fetch(`${API_URL}/events`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      Authorization: `Bearer ${token}`,
    },
    body: JSON.stringify({ title, external_ref: externalRef, category }),
  });
  if (!res.ok) {
    const err = await res.json();
    throw new Error(err.detail || "Erro ao criar evento");
  }
  return res.json();
}

export async function createSession(
  eventId: string,
  data: { starts_at: string; venue: string; capacity: number; price: string; mode: string },
  token: string
) {
  const res = await fetch(`${API_URL}/events/${eventId}/sessions`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      Authorization: `Bearer ${token}`,
    },
    body: JSON.stringify(data),
  });
  if (!res.ok) {
    const err = await res.json();
    throw new Error(err.detail || "Erro ao criar sessão");
  }
  return res.json();
}