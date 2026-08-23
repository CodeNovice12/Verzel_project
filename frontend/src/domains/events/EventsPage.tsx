import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { fetchEvents, type EventData } from "./api";
import { useAuth } from "../auth/AuthContext";

function formatDate(iso: string) {
  return new Date(iso).toLocaleString("pt-BR", {
    day: "2-digit",
    month: "2-digit",
    year: "numeric",
    hour: "2-digit",
    minute: "2-digit",
  });
}

export function EventsPage() {
  const [events, setEvents] = useState<EventData[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState("");
  const { user, logout } = useAuth();

  useEffect(() => {
    fetchEvents()
      .then(setEvents)
      .catch(() => setError("Erro ao carregar eventos"))
      .finally(() => setIsLoading(false));
  }, []);

  return (
    <div style={{ maxWidth: 700, margin: "40px auto", fontFamily: "sans-serif" }}>
      <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center" }}>
        <h1>Eventos</h1>
        <div>
          <span style={{ marginRight: 12 }}>
            {user?.name} ({user?.role})
          </span>
          {user?.role === "customer" && (
            <Link to="/my-tickets" style={{ marginRight: 12 }}>
              Meus ingressos
            </Link>
          )}
          {user?.role === "gate" && (
            <Link to="/gate" style={{ marginRight: 12 }}>
              Portaria
            </Link>
          )}
          {user?.role === "organizer" && (
            <Link to="/organizer" style={{ marginRight: 12 }}>
              Painel do organizador
            </Link>
          )}
          <button onClick={logout}>Sair</button>
        </div>
      </div>

      {isLoading && <p>Carregando...</p>}
      {error && <p style={{ color: "red" }}>{error}</p>}

      {events.map((event) => (
        <div
          key={event.id}
          style={{ border: "1px solid #ccc", borderRadius: 8, padding: 16, marginTop: 16 }}
        >
          <h2>{event.title}</h2>
          <p style={{ color: "#666" }}>{event.category}</p>

          {event.sessions.length === 0 && <p>Nenhuma sessão publicada ainda.</p>}

          {event.sessions.map((session) => (
            <div
              key={session.id}
              style={{
                display: "flex",
                justifyContent: "space-between",
                alignItems: "center",
                padding: "8px 0",
                borderTop: "1px solid #eee",
              }}
            >
              <div>
                <strong>{session.venue}</strong>
                <br />
                <span>{formatDate(session.starts_at)}</span> — R$ {session.price}
              </div>
              {user?.role === "customer" && (
                <Link to={`/sessions/${session.id}/reserve`}>
                  <button>Reservar</button>
                </Link>
              )}
            </div>
          ))}
        </div>
      ))}
    </div>
  );
}