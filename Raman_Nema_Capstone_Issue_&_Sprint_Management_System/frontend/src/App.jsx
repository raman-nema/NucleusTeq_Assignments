import { BrowserRouter, Routes, Route } from "react-router-dom";

import LoginPage from "./pages/LoginPage";
import RegisterPage from "./pages/RegisterPage";
import ProjectPage from "./pages/ProjectPage";
import SprintPage from "./pages/SprintPage";
import IssuePage from "./pages/IssuePage";
import DashboardPage from "./pages/DashboardPage";
import Layout from "./components/layout/Layout";
import { NotificationProvider } from "./context/NotificationContext";

function App() {
  return (
    <NotificationProvider>
      <BrowserRouter>
        <Routes>
          <Route path="/" element={<LoginPage />} />
          <Route path="/login" element={<LoginPage />} />
          <Route path="/register" element={<RegisterPage />} />
          <Route
            path="/dashboard"
            element={<Layout><DashboardPage /></Layout>}
          />
          <Route
            path="/projects"
            element={<Layout><ProjectPage /></Layout>}
          />
          <Route
            path="/sprints"
            element={<Layout><SprintPage /></Layout>}
          />
          <Route
            path="/issues"
            element={<Layout><IssuePage /></Layout>}
          />
        </Routes>
      </BrowserRouter>
    </NotificationProvider>
  );
}

export default App;
