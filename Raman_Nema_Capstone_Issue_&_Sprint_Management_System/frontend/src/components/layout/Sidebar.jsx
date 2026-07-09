import { useNavigate, useLocation } from "react-router-dom";
import { clearStorage, getRole, getUserName } from "../../utils/storage";
import { ADMIN_NAV_ITEMS, NAV_ITEMS, ROUTES } from "../../constants/navigation";

function Sidebar() {
  const navigate = useNavigate();
  const location = useLocation();
  const role = getRole();
  const userName = getUserName();

  function handleLogout() {
    clearStorage();
    navigate("/login");
  }

  function getNavigationTarget(path) {
    const shouldKeepSprintContext =
      (location.pathname === ROUTES.SPRINTS && path === ROUTES.ISSUES) ||
      (location.pathname === ROUTES.ISSUES && path === ROUTES.SPRINTS);

    if (!shouldKeepSprintContext) {
      return path;
    }

    const currentParams = new URLSearchParams(location.search);
    const targetParams = new URLSearchParams();
    const projectId = currentParams.get("projectId");
    const sprintId = currentParams.get("sprintId");

    if (projectId) {
      targetParams.set("projectId", projectId);
    }

    if (sprintId) {
      targetParams.set("sprintId", sprintId);
    }

    const queryString = targetParams.toString();

    return queryString ? `${path}?${queryString}` : path;
  }

  const navItems = role === "ADMIN" ? ADMIN_NAV_ITEMS : NAV_ITEMS;

  return (
    <aside className="sidebar">
      <div className="sidebar-title">SprintFlow</div>

      <nav className="sidebar-nav">
        {navItems.map((item) => (
          <button
            key={item.path}
            className={`sidebar-link ${location.pathname === item.path ? "active" : ""}`}
            onClick={() => navigate(getNavigationTarget(item.path))}
          >
            {item.label}
          </button>
        ))}
      </nav>

      <div className="sidebar-user">
        <div className="sidebar-user-avatar">
          {userName ? userName.charAt(0).toUpperCase() : "U"}
        </div>
        <div className="sidebar-user-info">
          <span className="sidebar-user-name">{userName || "User"}</span>
          <span className="sidebar-user-role">{role || "Role"}</span>
        </div>
      </div>

      <button className="sidebar-logout" onClick={handleLogout}>
        Logout
      </button>
    </aside>
  );
}

export default Sidebar;
