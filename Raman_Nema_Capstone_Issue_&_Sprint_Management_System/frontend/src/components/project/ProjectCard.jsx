import Button from "../common/Button";

import { getRole } from "../../utils/storage";

function ProjectCard({ project, onEdit, onDelete }) {
  const role = getRole();

  return (
    <div className="project-card">
      <div className="project-info">
        <h3>{project.name}</h3>
        <p>{project.description}</p>
      </div>

      <div className="project-actions">
        {(role === "ADMIN" || role === "MEMBER") && (
          <Button
            text="Edit"
            className="btn-small btn-edit"
            onClick={() => onEdit(project)}
          />
        )}

        {role === "ADMIN" && (
          <Button
            text="Delete"
            className="btn-small btn-danger"
            onClick={() => onDelete(project.id)}
          />
        )}
      </div>
    </div>
  );
}

export default ProjectCard;
