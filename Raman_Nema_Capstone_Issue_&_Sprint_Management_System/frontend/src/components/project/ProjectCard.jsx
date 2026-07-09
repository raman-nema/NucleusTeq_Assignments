import { useState } from "react";
import Button from "../common/Button";
import { getRole } from "../../utils/storage";

function ProjectCard({
  project,
  onEdit,
  onDelete,
  onViewSprints,
  onAssignMember,
  onRemoveMember,
}) {
  // Get logged-in user's role
  const role = getRole();

  // Component state
  const [memberId, setMemberId] = useState("");
  const [showMemberForm, setShowMemberForm] = useState(false);
  const [showMembers, setShowMembers] = useState(false);
  const [showActionMenu, setShowActionMenu] = useState(false);

  // Assign a member to the project
  function handleAssignMember(event) {
    event.preventDefault();

    const trimmedMemberId = memberId.trim();

    if (!trimmedMemberId) {
      return;
    }

    onAssignMember(project.id, trimmedMemberId);
    setMemberId("");
    setShowMemberForm(false);
  }

  // Toggle member assignment form
  function handleToggleMemberForm() {
    setShowMemberForm((current) => !current);
    setShowMembers(false);
    setShowActionMenu(false);
  }

  // Toggle project members list
  function handleToggleMembers() {
    setShowMembers((current) => !current);
    setShowMemberForm(false);
    setShowActionMenu(false);
  }

  return (
    <div className="project-card">
      <div className="project-info">
        {/* Project details */}
        <h3>{project.name}</h3>
        <p>{project.description}</p>

        {/* Member management (Admin only) */}
        {role === "ADMIN" && (showMemberForm || showMembers) && (
          <div className="member-manager">
            {showMemberForm && (
              <form className="member-form" onSubmit={handleAssignMember}>
                <input
                  className="member-input"
                  type="text"
                  value={memberId}
                  placeholder="Member user ID"
                  onChange={(event) => setMemberId(event.target.value)}
                />

                <Button
                  type="submit"
                  text="Save"
                  className="btn-small btn-success"
                  disabled={!memberId.trim()}
                />

                <Button
                  text="Cancel"
                  className="btn-small btn-muted"
                  onClick={() => {
                    setMemberId("");
                    setShowMemberForm(false);
                  }}
                />
              </form>
            )}

            {/* Members list */}
            {showMembers && (
              <div className="member-list">
                {project.members?.length > 0 ? (
                  project.members.map((member) => (
                    <div className="member-item" key={member.id}>
                      <span className="member-details">
                        <span className="member-name">{member.name}</span>
                        <span className="member-meta">
                          <small>{member.role}</small>
                          {member.id === project.created_by && (
                            <strong className="member-tag">Creator</strong>
                          )}
                        </span>
                      </span>

                      {/* Allow removing non-creator members */}
                      {member.id !== project.created_by && (
                        <Button
                          text="Remove"
                          className="btn-small btn-remove"
                          onClick={() => onRemoveMember(project.id, member.id)}
                        />
                      )}
                    </div>
                  ))
                ) : (
                  <p className="empty-members">No members assigned.</p>
                )}
              </div>
            )}
          </div>
        )}
      </div>

      <div className="project-actions">
        {/* Action menu for Admin and Member */}
        {(role === "ADMIN" || role === "MEMBER") && (
          <div className="project-menu">
            <button
              className="project-menu-toggle"
              type="button"
              aria-label="Project options"
              aria-expanded={showActionMenu}
              onClick={() => setShowActionMenu((current) => !current)}
            >
              ...
            </button>

            {/* Project actions */}
            {showActionMenu && (
              <div className="project-menu-list">
                <Button
                  text="Edit"
                  className="project-menu-item"
                  onClick={() => {
                    setShowActionMenu(false);
                    onEdit(project);
                  }}
                />

                <Button
                  text="View Sprints"
                  className="project-menu-item"
                  onClick={() => {
                    setShowActionMenu(false);
                    onViewSprints(project.id);
                  }}
                />

                {role === "ADMIN" && (
                  <>
                    <Button
                      text={showMembers ? "Hide Members" : "View Members"}
                      className="project-menu-item"
                      onClick={handleToggleMembers}
                    />

                    <Button
                      text="Assign Member"
                      className="project-menu-item"
                      onClick={handleToggleMemberForm}
                    />

                    <Button
                      text="Delete"
                      className="project-menu-item project-menu-danger"
                      onClick={() => {
                        setShowActionMenu(false);
                        onDelete(project.id);
                      }}
                    />
                  </>
                )}
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  );
}

export default ProjectCard;
