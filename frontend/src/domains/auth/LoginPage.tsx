import { useState, type FormEvent } from "react";
import { useNavigate, useSearchParams } from "react-router-dom";
import { loginRequest, fetchCurrentUser } from "./api";
import { useAuth } from "./AuthContext";

const roleLabels: Record<string, string> = {
  organizer: "Organizador",
  customer: "Cliente",
  gate: "Portaria",
};

export function LoginPage() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const [isSubmitting, setIsSubmitting] = useState(false);
  const { login } = useAuth();
  const navigate = useNavigate();
  const [searchParams] = useSearchParams();
  const expectedRole = searchParams.get("role");

  async function handleSubmit(e: FormEvent) {
    e.preventDefault();
    setError("");
    setIsSubmitting(true);
    try {
      const token = await loginRequest(email, password);

      if (expectedRole) {
        const user = await fetchCurrentUser(token);
        if (user.role !== expectedRole) {
          setError(
            `Essa conta é de ${roleLabels[user.role]}, não de ${roleLabels[expectedRole]}. Volte e escolha o papel certo.`
          );
          setIsSubmitting(false);
          return;
        }
      }

      await login(token);
      navigate("/");
    } catch (err) {
      setError(err instanceof Error ? err.message : "Erro ao entrar");
    } finally {
      setIsSubmitting(false);
    }
  }

  return (
    <div style={{ maxWidth: 360, margin: "80px auto", fontFamily: "sans-serif" }}>
      <h1>Entrar {expectedRole && `como ${roleLabels[expectedRole]}`}</h1>
      <form onSubmit={handleSubmit}>
        <div style={{ marginBottom: 12 }}>
          <label>E-mail</label>
          <input type="email" value={email} onChange={(e) => setEmail(e.target.value)} required style={{ width: "100%", padding: 8 }} />
        </div>
        <div style={{ marginBottom: 12 }}>
          <label>Senha</label>
          <input type="password" value={password} onChange={(e) => setPassword(e.target.value)} required style={{ width: "100%", padding: 8 }} />
        </div>
        {error && <p style={{ color: "red" }}>{error}</p>}
        <button type="submit" disabled={isSubmitting} style={{ width: "100%", padding: 10 }}>
          {isSubmitting ? "Entrando..." : "Entrar"}
        </button>
      </form>
    </div>
  );
}