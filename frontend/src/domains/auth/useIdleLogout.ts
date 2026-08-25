import { useEffect, useRef } from "react";
import { useNavigate } from "react-router-dom";
import { useAuth } from "./AuthContext";

const TIMEOUT_MS = 10 * 1000; 

export function useIdleLogout() {
  const { user, logout } = useAuth();
  const navigate = useNavigate();
  const timerRef = useRef<number | null>(null);

  useEffect(() => {
    if (!user) return;

    function resetTimer() {
      if (timerRef.current) window.clearTimeout(timerRef.current);
      timerRef.current = window.setTimeout(() => {
        logout();
        navigate("/select-role");
      }, TIMEOUT_MS);
    }

    const events = ["mousemove", "keydown", "click", "scroll"];
    events.forEach((ev) => window.addEventListener(ev, resetTimer));
    resetTimer();

    return () => {
      events.forEach((ev) => window.removeEventListener(ev, resetTimer));
      if (timerRef.current) window.clearTimeout(timerRef.current);
    };
  }, [user]);
}