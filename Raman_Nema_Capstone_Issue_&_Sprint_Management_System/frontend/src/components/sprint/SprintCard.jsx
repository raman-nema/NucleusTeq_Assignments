import { useState } from "react";
import Button from "../common/Button";
import { getRole } from "../../utils/storage";

// Format date for display
function formatDate(value) {
  if (!value) return "Not set";

  return new Date(value).toLocaleDateString("en-IN", {
    day: "2-digit",
    month: "short",
    year: "numeric",
  });
}

// Format sprint status
function formatStatus(status) {
  const labels = {
    PLANNED: "Planned",
    ACTIVE: "In Progress",
    IN_PROGRESS: "In Progress",
    COMPLETED: "Done",
    DONE: "Done",
  };

  return labels[status] || "Planned";
}

function getStatusClass(status) {
  const statusClass = {
    PLANNED: "status-planned",
    ACTIVE: "status-progress",
    IN_PROGRESS: "status-progress",
    COMPLETED: "status-done",
    DONE: "status-done",
  };

  return statusClass[status] || "status-planned";
}

function SprintCard({ sprint, projectName, onEdit, onDelete, onViewIssues }) {
  // Get current user role
  const role = getRole();

  // Component state
  const [showActionMenu, setShowActionMenu] = useState(false);

  // Check sprint management permission
  const canManageSprint = role === "ADMIN" || role === "MEMBER";

  return (
    <div className="project-card sprint-card">
      <div className="project-info">
        {/* Sprint details */}
        <div className="sprint-card-heading">
          <h3>{sprint.name}</h3>
          <span className={`sprint-status ${getStatusClass(sprint.status)}`}>
            {formatStatus(sprint.status)}
          </span>
        </div>

        <p>{sprint.goal}</p>

        {/* Sprint metadata */}
        <div className="sprint-meta">
          <span>{projectName || "Project"}</span>
          <span>Start: {formatDate(sprint.start_date)}</span>
          <span>End: {formatDate(sprint.end_date)}</span>
        </div>
      </div>

      <div className="project-actions">
        <div className="project-menu">
          <button
            className="project-menu-toggle"
            type="button"
            aria-label="Sprint options"
            aria-expanded={showActionMenu}
            onClick={() => setShowActionMenu((current) => !current)}
          >
            ...
          </button>

          {/* Sprint actions */}
          {showActionMenu && (
            <div className="project-menu-list">
              {canManageSprint && (
                <Button
                  text="Edit"
                  className="project-menu-item"
                  onClick={() => {
                    setShowActionMenu(false);
                    onEdit(sprint);
                  }}
                />
              )}

              <Button
                text="View Issues"
                className="project-menu-item"
                onClick={() => {
                  setShowActionMenu(false);
                  onViewIssues(sprint);
                }}
              />

              {canManageSprint && (
                <Button
                  text="Delete"
                  className="project-menu-item project-menu-danger"
                  onClick={() => {
                    setShowActionMenu(false);
                    onDelete(sprint.id);
                  }}
                />
              )}
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

export default SprintCard;
