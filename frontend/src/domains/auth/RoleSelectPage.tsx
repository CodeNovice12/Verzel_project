import { Link } from "react-router-dom";

const roles = [
  { key: "organizer", label: "Organizador", desc: "Crio e gerencio eventos" },
  { key: "customer", label: "Cliente", desc: "Compro e uso ingressos" },
  { key: "gate", label: "Portaria", desc: "Valido ingressos na entrada" },
];

export function RoleSelectPage() {
  return (
    <div style={{ maxWidth: 500, margin: "80px auto", fontFamily: "sans-serif", textAlign: "center" }}>
      <h1>Entrar como</h1>
      <div style={{ display: "flex", flexDirection: "column", gap: 12 }}>
        {roles.map((r) => (
          <Link
            key={r.key}
            to={`/login?role=${r.key}`}
            style={{
              display: "block",
              padding: 20,
              border: "1px solid #ccc",
              borderRadius: 8,
              textDecoration: "none",
              color: "inherit",
            }}
          >
            <strong>{r.label}</strong>
            <p style={{ margin: "4px 0 0", color: "#888" }}>{r.desc}</p>
          </Link>
        ))}
      </div>
    </div>
  );
}