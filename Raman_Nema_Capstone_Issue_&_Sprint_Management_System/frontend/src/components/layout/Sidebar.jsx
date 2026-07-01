import { useNavigate, useLocation } from "react-router-dom";
import { clearStorage, getRole } from "../../utils/storage";

function Sidebar() {
  const navigate = useNavigate();
  const location = useLocation();
  const role = getRole();

  function handleLogout() {
    clearStorage();
    navigate("/login");
  }

  const navItems = [
    { label: "Dashboard", path: "/dashboard" },
    { label: "Projects", path: "/projects" },
    { label: "Sprints", path: "/sprints" },
    { label: "Issues", path: "/issues" },
  ];

  return (
    <aside className="sidebar">
      <div className="sidebar-title">SprintFlow</div>

      <nav className="sidebar-nav">
        {navItems.map((item) => (
          <button
            key={item.path}
            className={`sidebar-link ${location.pathname === item.path ? "active" : ""}`}
            onClick={() => navigate(item.path)}
          >
            {item.label}
          </button>
        ))}
      </nav>

      <div className="sidebar-user">
        <div className="sidebar-user-avatar">
          {role ? role.charAt(0) : "U"}
        </div>
        <div className="sidebar-user-info">
          <span className="sidebar-user-role">{role || "User"}</span>
          <span className="sidebar-user-label">Logged in</span>
        </div>
      </div>

      <button className="sidebar-logout" onClick={handleLogout}>
        Logout
      </button>
    </aside>
  );
}

export default Sidebar;