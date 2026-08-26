import { useState, type FormEvent } from "react";
import { Link, useNavigate, useSearchParams } from "react-router-dom";
import { User, Mail, Lock, Loader2, Ticket, CheckCircle2, AlertCircle } from "lucide-react";
import { registerRequest } from "./api";

export function RegisterPage() {
  const [name, setName] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");

  const [error, setError] = useState("");
  const [message, setMessage] = useState("");
  const [isSubmitting, setIsSubmitting] = useState(false);

  const navigate = useNavigate();
  const [searchParams] = useSearchParams();

  const role = searchParams.get("role") || "customer";

  async function handleSubmit(e: FormEvent) {
    e.preventDefault();

    setError("");
    setMessage("");

    if (password !== confirmPassword) {
      setError("As senhas não coincidem.");
      return;
    }

    if (password.length < 6) {
      setError("A senha deve possuir pelo menos 6 caracteres.");
      return;
    }

    setIsSubmitting(true);

    try {
      await registerRequest(name, email, password, role);

      setMessage("Cadastro realizado com sucesso! Redirecionando...");

      setTimeout(() => {
        navigate(`/login?role=${role}`);
      }, 1200);
    } catch (err) {
      setError(
        err instanceof Error ? err.message : "Erro ao realizar cadastro"
      );
    } finally {
      setIsSubmitting(false);
    }
  }

  return (
    <div className="min-h-screen grid lg:grid-cols-2 bg-slate-50 text-slate-900">
      {/* Coluna Visual (Esquerda) */}
      <div className="hidden lg:flex flex-col justify-between bg-slate-900 p-12 text-white">
        <div className="flex items-center gap-2 font-bold text-2xl tracking-wide">
          <Ticket className="h-7 w-7 text-indigo-400" />
          <span>Verzel<span className="text-indigo-400">Events</span></span>
        </div>
        <div>
          <blockquote className="text-xl font-medium leading-relaxed mb-4">
            "Gerencie seus ingressos, acesse eventos e acompanhe suas portarias em um único lugar."
          </blockquote>
          <p className="text-sm text-slate-400">Sistema Integrado de Gestão de Eventos</p>
        </div>
        <div className="text-xs text-slate-500">
          © {new Date().getFullYear()} Verzel. Todos os direitos reservados.
        </div>
      </div>

      {/* Coluna do Formulário (Direita) */}
      <div className="flex items-center justify-center p-6 sm:p-12">
        <div className="w-full max-w-md space-y-8">
          <div>
            <h1 className="text-3xl font-bold tracking-tight text-slate-900">Criar conta</h1>
            <p className="text-slate-500 text-sm mt-2">
              Cadastre-se como <span className="font-semibold text-slate-700">{role === "customer" ? "cliente" : role}</span> para ter acesso à plataforma.
            </p>
          </div>

          <form onSubmit={handleSubmit} className="space-y-4">
            {/* Nome */}
            <div>
              <label className="block text-sm font-medium text-slate-700 mb-1">Nome completo</label>
              <div className="relative">
                <User className="absolute left-3 top-3 h-5 w-5 text-slate-400" />
                <input
                  type="text"
                  value={name}
                  onChange={(e) => setName(e.target.value)}
                  required
                  placeholder="Seu nome"
                  className="w-full rounded-lg border border-slate-300 bg-white py-2.5 pl-10 pr-4 text-sm focus:border-indigo-500 focus:outline-none focus:ring-2 focus:ring-indigo-500/20 transition-all"
                />
              </div>
            </div>

            {/* E-mail */}
            <div>
              <label className="block text-sm font-medium text-slate-700 mb-1">E-mail</label>
              <div className="relative">
                <Mail className="absolute left-3 top-3 h-5 w-5 text-slate-400" />
                <input
                  type="email"
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  required
                  placeholder="seu@email.com"
                  className="w-full rounded-lg border border-slate-300 bg-white py-2.5 pl-10 pr-4 text-sm focus:border-indigo-500 focus:outline-none focus:ring-2 focus:ring-indigo-500/20 transition-all"
                />
              </div>
            </div>

            {/* Senha */}
            <div>
              <label className="block text-sm font-medium text-slate-700 mb-1">Senha</label>
              <div className="relative">
                <Lock className="absolute left-3 top-3 h-5 w-5 text-slate-400" />
                <input
                  type="password"
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  required
                  placeholder="Mínimo de 6 caracteres"
                  className="w-full rounded-lg border border-slate-300 bg-white py-2.5 pl-10 pr-4 text-sm focus:border-indigo-500 focus:outline-none focus:ring-2 focus:ring-indigo-500/20 transition-all"
                />
              </div>
            </div>

            {/* Confirmar Senha */}
            <div>
              <label className="block text-sm font-medium text-slate-700 mb-1">Confirmar senha</label>
              <div className="relative">
                <Lock className="absolute left-3 top-3 h-5 w-5 text-slate-400" />
                <input
                  type="password"
                  value={confirmPassword}
                  onChange={(e) => setConfirmPassword(e.target.value)}
                  required
                  placeholder="Digite a senha novamente"
                  className="w-full rounded-lg border border-slate-300 bg-white py-2.5 pl-10 pr-4 text-sm focus:border-indigo-500 focus:outline-none focus:ring-2 focus:ring-indigo-500/20 transition-all"
                />
              </div>
            </div>

            {/* Alertas */}
            {error && (
              <div className="flex items-center gap-2 rounded-lg bg-red-50 p-3 text-sm text-red-600 border border-red-200">
                <AlertCircle className="h-4 w-4 shrink-0" />
                <span>{error}</span>
              </div>
            )}

            {message && (
              <div className="flex items-center gap-2 rounded-lg bg-emerald-50 p-3 text-sm text-emerald-600 border border-emerald-200">
                <CheckCircle2 className="h-4 w-4 shrink-0" />
                <span>{message}</span>
              </div>
            )}

            {/* Botão de Envio */}
            <button
              type="submit"
              disabled={isSubmitting}
              className="w-full rounded-lg bg-indigo-600 py-2.5 px-4 text-sm font-semibold text-white shadow-md hover:bg-indigo-500 focus:outline-none focus:ring-2 focus:ring-indigo-500/50 disabled:opacity-50 transition-all flex items-center justify-center gap-2"
            >
              {isSubmitting ? (
                <>
                  <Loader2 className="h-4 w-4 animate-spin" />
                  Criando conta...
                </>
              ) : (
                "Criar conta"
              )}
            </button>
          </form>

          <p className="text-center text-sm text-slate-600">
            Já possui uma conta?{" "}
            <Link to={`/login?role=${role}`} className="font-semibold text-indigo-600 hover:text-indigo-500">
              Entrar
            </Link>
          </p>
        </div>
      </div>
    </div>
  );
}