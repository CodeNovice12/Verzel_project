import { BrowserRouter, Routes, Route } from "react-router-dom";
import { AuthProvider } from "./domains/auth/AuthContext";
import { LoginPage } from "./domains/auth/LoginPage";
import { RoleSelectPage } from "./domains/auth/RoleSelectPage";
import { ProtectedRoute } from "./domains/auth/ProtectedRoute";
import { useIdleLogout } from "./domains/auth/useIdleLogout";
import { EventsPage } from "./domains/events/EventsPage";
import { ReservationPage } from "./domains/reservations/ReservationPage";
import { MyTicketsPage } from "./domains/tickets/MyTicketsPage";
import { GatePage } from "./domains/gate/GatePage";
import { OrganizerPage } from "./domains/organizer/OrganizerPage";
import { RegisterPage } from "./domains/auth/RegisterPage";

function IdleLogoutWatcher() {
  useIdleLogout();
  return null;
}

function App() {
  return (
    <AuthProvider>
      <BrowserRouter>
        <IdleLogoutWatcher />
        <Routes>
  <Route path="/select-role" element={<RoleSelectPage />} />
  <Route path="/login" element={<LoginPage />} />
  <Route path="/register" element={<RegisterPage />} />

  <Route
    path="/"
    element={
      <ProtectedRoute>
        <EventsPage />
      </ProtectedRoute>
    }
  />

  <Route
    path="/sessions/:sessionId/reserve"
    element={
      <ProtectedRoute allowedRoles={["customer"]}>
        <ReservationPage />
      </ProtectedRoute>
    }
  />

  <Route
    path="/my-tickets"
    element={
      <ProtectedRoute allowedRoles={["customer"]}>
        <MyTicketsPage />
      </ProtectedRoute>
    }
  />

  <Route
    path="/gate"
    element={
      <ProtectedRoute allowedRoles={["gate"]}>
        <GatePage />
      </ProtectedRoute>
    }
  />

  <Route
    path="/organizer"
    element={
      <ProtectedRoute allowedRoles={["organizer"]}>
        <OrganizerPage />
      </ProtectedRoute>
    }
  />
</Routes>
      </BrowserRouter>
    </AuthProvider>
  );
}

export default App;