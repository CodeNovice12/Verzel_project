import { useState, type FormEvent } from "react";
import { useAuth } from "../auth/AuthContext";
import { validateTicket, type ValidationResult } from "./api";

const resultColors: Record<ValidationResult["result"], string> = {
  valid: "#2e7d32",
  invalid: "#c62828",
  already_used: "#f9a825",
  wrong_event: "#c62828",
};

const resultLabels: Record<ValidationResult["result"], string> = {
  valid: "✅ VÁLIDO",
  invalid: "❌ INVÁLIDO",
  already_used: "⚠️ JÁ UTILIZADO",
  wrong_event: "❌ EVENTO ERRADO",
};

export function GatePage() {
  const { token } = useAuth();
  const [code, setCode] = useState("");
  const [sessionId, setSessionId] = useState("");
  const [result, setResult] = useState<ValidationResult | null>(null);
  const [error, setError] = useState("");
  const [isSubmitting, setIsSubmitting] = useState(false);

  async function handleSubmit(e: FormEvent) {
    e.preventDefault();
    if (!token) return;
    setError("");
    setResult(null);
    setIsSubmitting(true);
    try {
      const res = await validateTicket(code, sessionId, token);
      setResult(res);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Erro ao validar");
    } finally {
      setIsSubmitting(false);
    }
  }

  return (
    <div style={{ maxWidth: 500, margin: "40px auto", fontFamily: "sans-serif" }}>
      <h1>Portaria</h1>
      <form onSubmit={handleSubmit}>
        <div style={{ marginBottom: 12 }}>
          <label>Código do ingresso (QR)</label>
          <textarea
            value={code}
            onChange={(e) => setCode(e.target.value)}
            required
            rows={3}
            style={{ width: "100%", padding: 8 }}
            placeholder="Cole ou digite o código do QR"
          />
        </div>
        <div style={{ marginBottom: 12 }}>
          <label>ID da sessão</label>
          <input
            type="text"
            value={sessionId}
            onChange={(e) => setSessionId(e.target.value)}
            required
            style={{ width: "100%", padding: 8 }}
            placeholder="ID da sessão que está validando"
          />
        </div>
        {error && <p style={{ color: "red" }}>{error}</p>}
        <button type="submit" disabled={isSubmitting} style={{ width: "100%", padding: 10 }}>
          {isSubmitting ? "Validando..." : "Validar ingresso"}
        </button>
      </form>

      {result && (
        <div
          style={{
            marginTop: 24,
            padding: 20,
            borderRadius: 8,
            background: resultColors[result.result],
            color: "#fff",
            textAlign: "center",
          }}
        >
          <h2>{resultLabels[result.result]}</h2>
          <p>{result.message}</p>
        </div>
      )}
    </div>
  );
}