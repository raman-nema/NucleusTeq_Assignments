import { useState } from "react";
import Button from "../common/Button";
import { getRole } from "../../utils/storage";

function formatValue(value, fallback) {
  return value ? value.replaceAll("_", " ") : fallback;
}

function IssueCard({
  issue,
  sprintName,
  assigneeName,
  reporterName,
  onEdit,
  onDelete,
}) {
  const role = getRole();
  const [showActionMenu, setShowActionMenu] = useState(false);
  const canManageIssue = role === "ADMIN" || role === "MEMBER";

  return (
    <div className="project-card issue-card">
      <div className="project-info">
        <div className="sprint-card-heading">
          <h3>{issue.title}</h3>
          <span className={`issue-priority priority-${issue.priority}`}>
            {formatValue(issue.priority, "MEDIUM")}
          </span>
        </div>

        <p>{issue.description}</p>

        <div className="sprint-meta">
          <span>{formatValue(issue.status, "TODO")}</span>
          <span>{sprintName || "Sprint"}</span>
          <span>Assignee: {assigneeName || issue.assignee}</span>
          <span>Reporter: {reporterName || issue.reporter}</span>
        </div>
      </div>

      {canManageIssue && (
        <div className="project-actions">
          <div className="project-menu">
            <button
              className="project-menu-toggle"
              type="button"
              aria-label="Issue options"
              aria-expanded={showActionMenu}
              onClick={() => setShowActionMenu((current) => !current)}
            >
              ...
            </button>

            {showActionMenu && (
              <div className="project-menu-list">
                <Button
                  text="Edit"
                  className="project-menu-item"
                  onClick={() => {
                    setShowActionMenu(false);
                    onEdit(issue);
                  }}
                />

                <Button
                  text="Delete"
                  className="project-menu-item project-menu-danger"
                  onClick={() => {
                    setShowActionMenu(false);
                    onDelete(issue.id);
                  }}
                />
              </div>
            )}
          </div>
        </div>
      )}
    </div>
  );
}

export default IssueCard;
