import { useEffect, useState } from "react";
import { useParams, useNavigate } from "react-router-dom";
import { useAuth } from "../auth/AuthContext";
import { fetchSeats, createReservation, payReservation } from "./api";

interface Seat {
  id: string;
  code: string;
  status: "available" | "reserved" | "sold";
}

export function ReservationPage() {
  const { sessionId } = useParams<{ sessionId: string }>();
  const { token } = useAuth();
  const navigate = useNavigate();

  const [seats, setSeats] = useState<Seat[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState("");
  const [step, setStep] = useState<"choosing" | "paying" | "done">("choosing");
  const [reservationId, setReservationId] = useState<string | null>(null);
  const [paymentMessage, setPaymentMessage] = useState("");

  useEffect(() => {
    if (!sessionId || !token) return;
    fetchSeats(sessionId, token)
      .then(setSeats)
      .catch(() => setError("Erro ao carregar assentos"))
      .finally(() => setIsLoading(false));
  }, [sessionId, token]);

  async function handleReserve(seatId: string) {
    if (!sessionId || !token) return;
    setError("");
    try {
      const reservation = await createReservation(sessionId, seatId, token);
      setReservationId(reservation.id);
      setStep("paying");
    } catch (err) {
      setError(err instanceof Error ? err.message : "Erro ao reservar");
    }
  }

  async function handlePay() {
    if (!reservationId || !token) return;
    setError("");
    try {
      const result = await payReservation(reservationId, token);
      setPaymentMessage(result.message);
      setStep("done");
    } catch (err) {
      setError(err instanceof Error ? err.message : "Erro no pagamento");
    }
  }

  if (isLoading) return <p>Carregando assentos...</p>;

  return (
    <div style={{ maxWidth: 500, margin: "40px auto", fontFamily: "sans-serif" }}>
      <button onClick={() => navigate("/")}>← Voltar</button>
      <h1>Reservar assento</h1>
      {error && <p style={{ color: "red" }}>{error}</p>}

      {step === "choosing" && (
        <div style={{ display: "grid", gridTemplateColumns: "repeat(5, 1fr)", gap: 8 }}>
          {seats.map((seat) => (
            <button
              key={seat.id}
              disabled={seat.status !== "available"}
              onClick={() => handleReserve(seat.id)}
              style={{
                padding: 12,
                background: seat.status === "available" ? "#fff" : "#eee",
                color: seat.status === "available" ? "#000" : "#999",
                cursor: seat.status === "available" ? "pointer" : "not-allowed",
              }}
            >
              {seat.code}
            </button>
          ))}
        </div>
      )}

      {step === "paying" && (
        <div>
          <p>Assento reservado! Confirme o pagamento (simulado):</p>
          <button onClick={handlePay}>Pagar agora</button>
        </div>
      )}

      {step === "done" && (
        <div>
          <p>{paymentMessage}</p>
          <button onClick={() => navigate("/my-tickets")}>Ver meus ingressos</button>
        </div>
      )}
    </div>
  );
}