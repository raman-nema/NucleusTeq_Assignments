import { useState } from "react";
import InputField from "../common/InputField";
import Button from "../common/Button";
import { validateSprint } from "../../utils/validations";

// Format date for date input field
function formatDateInput(value) {
  if (!value) return "";

  return value.slice(0, 10);
}

// Return initial form values
function getInitialFormData(initialData) {
  if (initialData) {
    return {
      name: initialData.name,
      goal: initialData.goal,
      start_date: formatDateInput(initialData.start_date),
      end_date: formatDateInput(initialData.end_date),
      status: initialData.status || "PLANNED",
    };
  }

  return {
    name: "",
    goal: "",
    start_date: "",
    end_date: "",
    status: "PLANNED",
  };
}

function SprintForm({ initialData, onSubmit, onCancel, loading }) {
  // Form state
  const [formData, setFormData] = useState(() =>
    getInitialFormData(initialData),
  );

  // Validation errors
  const [errors, setErrors] = useState({});

  // Handle field updates
  function handleChange(event) {
    const { name, value } = event.target;

    setFormData((previous) => ({
      ...previous,
      [name]: value,
    }));

    // Clear field error on input
    setErrors((previous) => ({
      ...previous,
      [name]: "",
    }));
  }

  // Validate and submit form
  function handleSubmit(event) {
    event.preventDefault();

    const validationErrors = validateSprint(formData);

    if (Object.keys(validationErrors).length > 0) {
      setErrors(validationErrors);
      return;
    }

    setErrors({});
    onSubmit(formData);
  }

  return (
    <form onSubmit={handleSubmit}>
      {/* Sprint name */}
      <div className="form-group">
        <InputField
          label="Sprint Name"
          name="name"
          type="text"
          value={formData.name}
          onChange={handleChange}
        />

        {errors.name && <p className="error-message">{errors.name}</p>}
      </div>

      {/* Sprint goal */}
      <div className="form-group">
        <label>Goal</label>

        <textarea
          className="description-input"
          name="goal"
          value={formData.goal}
          onChange={handleChange}
          rows="5"
        />

        {errors.goal && <p className="error-message">{errors.goal}</p>}
      </div>

      {/* Sprint dates and status */}
      <div className="sprint-date-grid">
        <div className="form-group">
          <InputField
            label="Start Date"
            name="start_date"
            type="date"
            value={formData.start_date}
            onChange={handleChange}
          />

          {errors.start_date && (
            <p className="error-message">{errors.start_date}</p>
          )}
        </div>

        <div className="form-group">
          <InputField
            label="End Date"
            name="end_date"
            type="date"
            value={formData.end_date}
            onChange={handleChange}
          />

          {errors.end_date && (
            <p className="error-message">{errors.end_date}</p>
          )}
        </div>

        <div className="form-group">
          <label>Status</label>

          <select
            className="search-input"
            name="status"
            value={formData.status}
            onChange={handleChange}
          >
            <option value="PLANNED">Planned</option>
            <option value="ACTIVE">In Progress</option>
            <option value="COMPLETED">Done</option>
          </select>

          {errors.status && <p className="error-message">{errors.status}</p>}
        </div>
      </div>

      {/* Form actions */}
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

export default SprintForm;
