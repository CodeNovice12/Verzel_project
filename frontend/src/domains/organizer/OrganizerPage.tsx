import { useEffect, useState, type FormEvent } from "react";
import { useNavigate } from "react-router-dom";
import { useAuth } from "../auth/AuthContext";
import { fetchEvents, type EventData } from "../events/api";
import { fetchCatalog, createEvent, createSession, type CatalogItem } from "./api";

export function OrganizerPage() {
  const { token, user } = useAuth();
  const navigate = useNavigate();

  const [catalog, setCatalog] = useState<CatalogItem[]>([]);
  const [myEvents, setMyEvents] = useState<EventData[]>([]);
  const [selectedItem, setSelectedItem] = useState<CatalogItem | null>(null);
  const [error, setError] = useState("");
  const [message, setMessage] = useState("");

  // formulário de sessão (por evento selecionado)
  const [sessionEventId, setSessionEventId] = useState<string | null>(null);
  const [venue, setVenue] = useState("");
  const [startsAt, setStartsAt] = useState("");
  const [capacity, setCapacity] = useState(20);
  const [price, setPrice] = useState("30.00");
  const [mode, setMode] = useState<"seat_map" | "quantity">("seat_map");

  async function loadData() {
    const [catalogData, eventsData] = await Promise.all([fetchCatalog(), fetchEvents()]);
    setCatalog(catalogData);
    setMyEvents(eventsData.filter((e) => e.organizer_id === user?.id));
  }

  useEffect(() => {
    loadData().catch(() => setError("Erro ao carregar dados"));
  }, []);

  async function handleCreateEvent(e: FormEvent) {
    e.preventDefault();
    if (!token || !selectedItem) return;
    setError("");
    setMessage("");
    try {
      await createEvent(selectedItem.title, selectedItem.external_ref, selectedItem.category, token);
      setMessage("Evento criado com sucesso!");
      setSelectedItem(null);
      await loadData();
    } catch (err) {
      setError(err instanceof Error ? err.message : "Erro ao criar evento");
    }
  }

  async function handleCreateSession(e: FormEvent) {
    e.preventDefault();
    if (!token || !sessionEventId) return;
    setError("");
    setMessage("");
    try {
      await createSession(
        sessionEventId,
        { starts_at: startsAt, venue, capacity, price, mode },
        token
      );
      setMessage("Sessão criada com sucesso!");
      setSessionEventId(null);
      await loadData();
    } catch (err) {
      setError(err instanceof Error ? err.message : "Erro ao criar sessão");
    }
  }

  return (
    <div style={{ maxWidth: 600, margin: "40px auto", fontFamily: "sans-serif" }}>
      <button onClick={() => navigate("/")}>← Voltar</button>
      <h1>Painel do organizador</h1>
      {error && <p style={{ color: "red" }}>{error}</p>}
      {message && <p style={{ color: "green" }}>{message}</p>}

      <h2>Criar evento a partir do catálogo</h2>
      <form onSubmit={handleCreateEvent}>
        <select
          value={selectedItem?.external_ref ?? ""}
          onChange={(e) =>
            setSelectedItem(catalog.find((c) => c.external_ref === e.target.value) ?? null)
          }
          required
          style={{ width: "100%", padding: 8, marginBottom: 8 }}
        >
          <option value="">-- selecione --</option>
          {catalog.map((item) => (
            <option key={item.external_ref} value={item.external_ref}>
              {item.title} ({item.category})
            </option>
          ))}
        </select>
        <button type="submit" disabled={!selectedItem}>
          Criar evento
        </button>
      </form>

      <h2 style={{ marginTop: 32 }}>Meus eventos</h2>
      {myEvents.map((event) => (
        <div key={event.id} style={{ border: "1px solid #ccc", padding: 12, marginBottom: 12 }}>
          <strong>{event.title}</strong> ({event.sessions.length} sessão(ões))
          <br />
          <button onClick={() => setSessionEventId(event.id)} style={{ marginTop: 8 }}>
            + Adicionar sessão
          </button>

          {sessionEventId === event.id && (
            <form onSubmit={handleCreateSession} style={{ marginTop: 12 }}>
              <input
                placeholder="Local (ex: Sala 1)"
                value={venue}
                onChange={(e) => setVenue(e.target.value)}
                required
                style={{ width: "100%", padding: 6, marginBottom: 6 }}
              />
              <input
                type="datetime-local"
                value={startsAt}
                onChange={(e) => setStartsAt(e.target.value)}
                required
                style={{ width: "100%", padding: 6, marginBottom: 6 }}
              />
              <input
                type="number"
                placeholder="Capacidade"
                value={capacity}
                onChange={(e) => setCapacity(Number(e.target.value))}
                required
                style={{ width: "100%", padding: 6, marginBottom: 6 }}
              />
              <input
                placeholder="Preço (ex: 30.00)"
                value={price}
                onChange={(e) => setPrice(e.target.value)}
                required
                style={{ width: "100%", padding: 6, marginBottom: 6 }}
              />
              <select
                value={mode}
                onChange={(e) => setMode(e.target.value as "seat_map" | "quantity")}
                style={{ width: "100%", padding: 6, marginBottom: 6 }}
              >
                <option value="seat_map">Mapa de assentos</option>
                <option value="quantity">Quantidade (pista)</option>
              </select>
              <button type="submit">Salvar sessão</button>
            </form>
          )}
        </div>
      ))}
    </div>
  );
}