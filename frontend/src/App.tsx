import { BrowserRouter, Routes, Route } from "react-router-dom";
import { AuthProvider } from "./domains/auth/AuthContext";
import { LoginPage } from "./domains/auth/LoginPage";
import { ProtectedRoute } from "./domains/auth/ProtectedRoute";
import { EventsPage } from "./domains/events/EventsPage";
import { ReservationPage } from "./domains/reservations/ReservationPage";
import { MyTicketsPage } from "./domains/tickets/MyTicketsPage";
import { GatePage } from "./domains/gate/GatePage";
import { OrganizerPage } from "./domains/organizer/OrganizerPage";

function App() {
  return (
    <AuthProvider>
      <BrowserRouter>
        <Routes>
          <Route path="/login" element={<LoginPage />} />
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