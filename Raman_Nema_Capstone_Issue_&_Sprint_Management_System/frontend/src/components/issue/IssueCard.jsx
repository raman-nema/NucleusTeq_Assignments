import { useState } from "react";
import Button from "../common/Button";
import { getRole, getUserName } from "../../utils/storage";

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
  onAddComment,
  onDeleteComment,
}) {
  const role = getRole();
  const currentUserName = getUserName();
  const [showActionMenu, setShowActionMenu] = useState(false);
  const [showComments, setShowComments] = useState(false);
  const [commentText, setCommentText] = useState("");
  const [submittingComment, setSubmittingComment] = useState(false);
  const canManageIssue = role === "ADMIN" || role === "MEMBER";
  const comments = issue.comments || [];

  async function handleAddComment(event) {
    event.preventDefault();

    const trimmedText = commentText.trim();

    if (!trimmedText || submittingComment || !onAddComment) {
      return;
    }

    setSubmittingComment(true);

    try {
      await onAddComment(issue.id, trimmedText);
      setCommentText("");
    } finally {
      setSubmittingComment(false);
    }
  }

  return (
    <div className="project-card issue-card">
      <div className="project-info">
        <div className="sprint-card-heading">
          <h3>{issue.title}</h3>
          <div className="issue-badges">
            <span className="issue-type">{formatValue(issue.type, "TASK")}</span>
            <span className={`issue-priority priority-${issue.priority}`}>
              {formatValue(issue.priority, "MEDIUM")}
            </span>
          </div>
        </div>

        <p>{issue.description}</p>

        <div className="sprint-meta">
          <span>{formatValue(issue.status, "TODO")}</span>
          <span>{sprintName || "Sprint"}</span>
          <span>Assignee: {assigneeName || issue.assignee}</span>
          <span>Reporter: {reporterName || issue.reporter}</span>
        </div>

        {showComments && (
          <div className="issue-comments-section">
            <div className="issue-comments-list">
              {comments.length > 0 ? (
                comments.map((comment, index) => (
                  <div key={`${comment.user_id}-${index}`} className="issue-comment-item">
                    <div className="issue-comment-header">
                      <strong>{comment.user_name || "Unknown"}</strong>
                      {comment.user_name === currentUserName && onDeleteComment && (
                        <button
                          className="issue-comment-delete"
                          type="button"
                          onClick={() => onDeleteComment(issue.id, comment.id)}
                        >
                          Delete
                        </button>
                      )}
                    </div>
                    <p className="issue-comment-text">{comment.text}</p>
                  </div>
                ))
              ) : (
                <p className="empty-comments">No comments yet.</p>
              )}
            </div>

            <form className="issue-comment-form" onSubmit={handleAddComment}>
              <textarea
                className="issue-comment-textarea"
                value={commentText}
                onChange={(event) => setCommentText(event.target.value)}
                placeholder="Write a comment"
                rows={3}
              />

              <div className="issue-comment-actions">
                <button
                  className="btn-success issue-comment-submit"
                  type="submit"
                  disabled={submittingComment}
                >
                  {submittingComment ? "Adding..." : "Add comment"}
                </button>
              </div>
            </form>
          </div>
        )}
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
                  text="Comments"
                  className="project-menu-item"
                  onClick={() => {
                    setShowActionMenu(false);
                    setShowComments((current) => !current);
                  }}
                />

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
