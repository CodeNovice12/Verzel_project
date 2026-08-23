import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { QRCodeSVG } from "qrcode.react";
import { useAuth } from "../auth/AuthContext";
import { fetchMyTickets, type TicketData } from "./api";

export function MyTicketsPage() {
  const { token } = useAuth();
  const navigate = useNavigate();
  const [tickets, setTickets] = useState<TicketData[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    if (!token) return;
    fetchMyTickets(token)
      .then(setTickets)
      .catch(() => setError("Erro ao carregar ingressos"))
      .finally(() => setIsLoading(false));
  }, [token]);

  return (
    <div style={{ maxWidth: 500, margin: "40px auto", fontFamily: "sans-serif" }}>
      <button onClick={() => navigate("/")}>← Voltar</button>
      <h1>Meus ingressos</h1>

      {isLoading && <p>Carregando...</p>}
      {error && <p style={{ color: "red" }}>{error}</p>}
      {!isLoading && tickets.length === 0 && <p>Você ainda não tem ingressos.</p>}

      {tickets.map((ticket) => (
        <div
          key={ticket.id}
          style={{
            border: "1px solid #ccc",
            borderRadius: 8,
            padding: 16,
            marginTop: 16,
            textAlign: "center",
          }}
        >
          <QRCodeSVG value={ticket.qr_signature} size={180} />
          <p style={{ marginTop: 8 }}>
            Status: <strong>{ticket.status === "valid" ? "Válido" : "Utilizado"}</strong>
          </p>
        </div>
      ))}
    </div>
  );
}