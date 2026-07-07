import { useEffect, useMemo, useState } from "react";
import { useNavigate } from "react-router-dom";

import {
  getAdminDashboard,
  updateDashboardUser,
} from "../services/admin-service";
import { getRole } from "../utils/storage";

import "../styles/DashboardPage.css";

function formatDate(value) {
  if (!value) {
    return "Not available";
  }

  return new Date(value).toLocaleString();
}

function DashboardPage() {
  const navigate = useNavigate();
  const role = getRole();
  const [dashboard, setDashboard] = useState({
    totals: {
      projects: 0,
      sprints: 0,
      issues: 0,
      users: 0,
    },
    users: [],
  });
  const [searchTerm, setSearchTerm] = useState("");
  const [editingUserId, setEditingUserId] = useState(null);
  const [editFormData, setEditFormData] = useState({
    name: "",
    email: "",
  });
  const [editErrors, setEditErrors] = useState({});
  const [savingUser, setSavingUser] = useState(false);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  const totalCards = useMemo(
    () => [
      {
        label: "Total Projects",
        value: dashboard.totals.projects,
        path: "/projects",
      },
      {
        label: "Total Sprints",
        value: dashboard.totals.sprints,
        path: "/sprints",
      },
      {
        label: "Total Issues",
        value: dashboard.totals.issues,
        path: "/issues",
      },
      {
        label: "Total Users",
        value: dashboard.totals.users,
        path: null,
      },
    ],
    [dashboard.totals],
  );

  useEffect(() => {
    if (role !== "ADMIN") {
      setLoading(false);
      setError("Only admin users can access the dashboard.");
      return;
    }

    loadDashboard();
  }, [role]);

  async function loadDashboard(params = {}) {
    setLoading(true);
    setError("");

    try {
      const response = await getAdminDashboard(params);
      setDashboard(response.data);
    } catch (error) {
      setError(error.response?.data?.message || "Unable to load dashboard.");
    } finally {
      setLoading(false);
    }
  }

  function handleSearch(event) {
    event.preventDefault();

    loadDashboard(searchTerm.trim() ? { search: searchTerm.trim() } : {});
  }

  function handleClearSearch() {
    setSearchTerm("");
    loadDashboard();
  }

  function handleEditUser(user) {
    setEditingUserId(user.id);
    setEditFormData({
      name: user.name,
      email: user.email,
    });
    setEditErrors({});
  }

  function handleCancelEdit() {
    setEditingUserId(null);
    setEditFormData({
      name: "",
      email: "",
    });
    setEditErrors({});
  }

  function handleEditChange(event) {
    const { name, value } = event.target;

    setEditFormData((previous) => ({
      ...previous,
      [name]: value,
    }));

    setEditErrors((previous) => ({
      ...previous,
      [name]: "",
    }));
  }

  function validateEditForm() {
    const errors = {};

    if (!editFormData.name.trim()) {
      errors.name = "Name is required.";
    } else if (editFormData.name.trim().length < 3) {
      errors.name = "Name must be at least 3 characters.";
    } else if (editFormData.name.trim().length > 50) {
      errors.name = "Name cannot exceed 50 characters.";
    }

    if (!editFormData.email.trim()) {
      errors.email = "Email is required.";
    } else if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(editFormData.email)) {
      errors.email = "Enter a valid email address.";
    } else if (!editFormData.email.endsWith("@company.com")) {
      errors.email = "Only @company.com email addresses are allowed.";
    }

    return errors;
  }

  async function handleSaveUser(userId) {
    const validationErrors = validateEditForm();

    if (Object.keys(validationErrors).length > 0) {
      setEditErrors(validationErrors);
      return;
    }

    setSavingUser(true);
    setError("");

    try {
      const response = await updateDashboardUser(userId, {
        name: editFormData.name.trim(),
        email: editFormData.email.trim(),
      });

      setDashboard((previous) => ({
        ...previous,
        users: previous.users.map((user) =>
          user.id === userId ? response.data : user,
        ),
      }));

      handleCancelEdit();
    } catch (error) {
      setError(error.response?.data?.message || "Unable to update user.");
    } finally {
      setSavingUser(false);
    }
  }

  return (
    <div className="dashboard-page">
      <div className="dashboard-container">
        <h1>Users</h1>

        {loading && <p>Loading dashboard...</p>}
        {error && <p className="error-message">{error}</p>}

        {!loading && !error && (
          <>
            <div className="dashboard-stats">
              {totalCards.map((card) => (
                <button
                  key={card.label}
                  className={`dashboard-stat-card ${card.path ? "" : "static"}`}
                  type="button"
                  onClick={() => card.path && navigate(card.path)}
                >
                  <span>{card.label}</span>
                  <strong>{card.value}</strong>
                </button>
              ))}
            </div>

            <section className="dashboard-users">
              <div className="dashboard-section-header">
                <h2>Users</h2>

                <form className="dashboard-search" onSubmit={handleSearch}>
                  <input
                    className="dashboard-search-input"
                    type="text"
                    value={searchTerm}
                    placeholder="Search by name or user ID"
                    onChange={(event) => setSearchTerm(event.target.value)}
                  />

                  <button type="submit">Search</button>
                  <button
                    type="button"
                    className="muted"
                    onClick={handleClearSearch}
                  >
                    Clear
                  </button>
                </form>
              </div>

              <div className="dashboard-table-wrap">
                <table className="dashboard-table">
                  <thead>
                    <tr>
                      <th>User ID</th>
                      <th>Name</th>
                      <th>Email</th>
                      <th>Role</th>
                      <th>Created At</th>
                      <th>Actions</th>
                    </tr>
                  </thead>
                  <tbody>
                    {dashboard.users.length > 0 ? (
                      dashboard.users.map((user) => (
                        <tr key={user.id}>
                          <td className="user-id">{user.id}</td>
                          <td>
                            {editingUserId === user.id ? (
                              <>
                                <input
                                  className="dashboard-edit-input"
                                  name="name"
                                  type="text"
                                  value={editFormData.name}
                                  onChange={handleEditChange}
                                />
                                {editErrors.name && (
                                  <span className="dashboard-field-error">
                                    {editErrors.name}
                                  </span>
                                )}
                              </>
                            ) : (
                              user.name
                            )}
                          </td>
                          <td>
                            {editingUserId === user.id ? (
                              <>
                                <input
                                  className="dashboard-edit-input"
                                  name="email"
                                  type="email"
                                  value={editFormData.email}
                                  onChange={handleEditChange}
                                />
                                {editErrors.email && (
                                  <span className="dashboard-field-error">
                                    {editErrors.email}
                                  </span>
                                )}
                              </>
                            ) : (
                              user.email
                            )}
                          </td>
                          <td>
                            <span className={`role-chip role-${user.role}`}>
                              {user.role}
                            </span>
                          </td>
                          <td>{formatDate(user.created_at)}</td>
                          <td>
                            {editingUserId === user.id ? (
                              <div className="dashboard-row-actions">
                                <button
                                  type="button"
                                  onClick={() => handleSaveUser(user.id)}
                                  disabled={savingUser}
                                >
                                  {savingUser ? "Saving..." : "Save"}
                                </button>
                                <button
                                  type="button"
                                  className="muted"
                                  onClick={handleCancelEdit}
                                  disabled={savingUser}
                                >
                                  Cancel
                                </button>
                              </div>
                            ) : (
                              <button
                                type="button"
                                className="dashboard-edit-button"
                                onClick={() => handleEditUser(user)}
                              >
                                Edit
                              </button>
                            )}
                          </td>
                        </tr>
                      ))
                    ) : (
                      <tr>
                        <td colSpan="6" className="empty-table">
                          No users found.
                        </td>
                      </tr>
                    )}
                  </tbody>
                </table>
              </div>
            </section>
          </>
        )}
      </div>
    </div>
  );
}

export default DashboardPage;
