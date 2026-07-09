import { useState } from "react";
import InputField from "../common/InputField";
import Button from "../common/Button";
import { validateIssue } from "../../utils/validations";

function getInitialFormData(initialData, selectedSprintId, sprints, members) {
  const defaultSprintId = selectedSprintId || sprints[0]?.id || "";
  const defaultAssigneeId = members[0]?.id || "";

  if (initialData) {
    return {
      title: initialData.title,
      description: initialData.description,
      assignee: initialData.assignee || defaultAssigneeId,
      sprint_id: initialData.sprint_id || defaultSprintId,
      priority: initialData.priority || "MEDIUM",
      type: initialData.type || "TASK",
      status: initialData.status || "TODO",
    };
  }

  return {
    title: "",
    description: "",
    assignee: defaultAssigneeId,
    sprint_id: defaultSprintId,
    priority: "MEDIUM",
    type: "TASK",
    status: "TODO",
  };
}

function IssueForm({
  initialData,
  sprints,
  members,
  selectedSprintId,
  onSubmit,
  onCancel,
  loading,
}) {
  const [formData, setFormData] = useState(() =>
    getInitialFormData(initialData, selectedSprintId, sprints, members),
  );
  const [errors, setErrors] = useState({});

  function handleChange(event) {
    const { name, value } = event.target;

    setFormData((previous) => ({
      ...previous,
      [name]: value,
    }));

    setErrors((previous) => ({
      ...previous,
      [name]: "",
    }));
  }

  function handleSubmit(event) {
    event.preventDefault();

    const validationErrors = validateIssue(formData);

    if (Object.keys(validationErrors).length > 0) {
      setErrors(validationErrors);
      return;
    }

    setErrors({});
    onSubmit(formData);
  }

  return (
    <form onSubmit={handleSubmit}>
      <div className="form-group">
        <InputField
          label="Issue Title"
          name="title"
          type="text"
          value={formData.title}
          onChange={handleChange}
        />

        {errors.title && <p className="error-message">{errors.title}</p>}
      </div>

      <div className="form-group">
        <label>Description</label>

        <textarea
          className="description-input"
          name="description"
          value={formData.description}
          onChange={handleChange}
          rows="5"
        />

        {errors.description && (
          <p className="error-message">{errors.description}</p>
        )}
      </div>

      <div className="issue-form-grid">
        <div className="form-group">
          <label>Sprint</label>

          <select
            className="search-input"
            name="sprint_id"
            value={formData.sprint_id}
            onChange={handleChange}
          >
            {sprints.map((sprint) => (
              <option key={sprint.id} value={sprint.id}>
                {sprint.name}
              </option>
            ))}
          </select>

          {errors.sprint_id && (
            <p className="error-message">{errors.sprint_id}</p>
          )}
        </div>

        <div className="form-group">
          <label>Assignee</label>

          <select
            className="search-input"
            name="assignee"
            value={formData.assignee}
            onChange={handleChange}
          >
            {members.map((member) => (
              <option key={member.id} value={member.id}>
                {member.name}
              </option>
            ))}
          </select>

          {errors.assignee && (
            <p className="error-message">{errors.assignee}</p>
          )}
        </div>

        <div className="form-group">
          <label>Priority</label>

          <select
            className="search-input"
            name="priority"
            value={formData.priority}
            onChange={handleChange}
          >
            <option value="LOW">Low</option>
            <option value="MEDIUM">Medium</option>
            <option value="HIGH">High</option>
          </select>

          {errors.priority && (
            <p className="error-message">{errors.priority}</p>
          )}
        </div>

        <div className="form-group">
          <label>Type</label>

          <select
            className="search-input"
            name="type"
            value={formData.type}
            onChange={handleChange}
          >
            <option value="TASK">Task</option>
            <option value="BUG">Bug</option>
            <option value="STORY">Story</option>
          </select>

          {errors.type && <p className="error-message">{errors.type}</p>}
        </div>

        <div className="form-group">
          <label>Status</label>

          <select
            className="search-input"
            name="status"
            value={formData.status}
            onChange={handleChange}
          >
            <option value="TODO">Todo</option>
            <option value="IN_PROGRESS">In Progress</option>
            <option value="DONE">Done</option>
          </select>

          {errors.status && <p className="error-message">{errors.status}</p>}
        </div>
      </div>

      <div className="button-group">
        <Button
          type="submit"
          className="btn-success"
          disabled={loading}
          text={loading ? "Saving..." : "Save"}
        />

        <Button type="button" text="Cancel" onClick={onCancel} />
      </div>
    </form>
  );
}

export default IssueForm;
