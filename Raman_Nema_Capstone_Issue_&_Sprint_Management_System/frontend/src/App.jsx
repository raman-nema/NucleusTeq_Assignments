import { BrowserRouter, Routes, Route } from "react-router-dom";

import LoginPage from "./pages/LoginPage";
import RegisterPage from "./pages/RegisterPage";
import ProjectPage from "./pages/ProjectPage";
import DashboardPage from "./pages/DashboardPage";
import Layout from "./components/layout/Layout";

function App() {
  return (
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
          element={<Layout><h1 style={{ padding: "32px 24px" }}>Sprints — coming soon</h1></Layout>}
        />
        <Route
          path="/issues"
          element={<Layout><h1 style={{ padding: "32px 24px" }}>Issues — coming soon</h1></Layout>}
        />
      </Routes>
    </BrowserRouter>
  );
}

export default App;