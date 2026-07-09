import { useState } from "react";
import InputField from "../common/InputField";
import Button from "../common/Button";
import { validateProject } from "../../utils/validations";

// Return initial form values.
function getInitialFormData(initialData) {
  if (initialData) {
    return {
      name: initialData.name,
      description: initialData.description,
    };
  }

  return {
    name: "",
    description: "",
  };
}

function ProjectForm({ initialData, onSubmit, onCancel, loading }) {
  // Form state
  const [formData, setFormData] = useState(() =>
    getInitialFormData(initialData),
  );

  // Validation errors
  const [errors, setErrors] = useState({});

  // Handle input changes
  const handleChange = (event) => {
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
  };

  // Validate and submit form
  const handleSubmit = (event) => {
    event.preventDefault();

    const validationErrors = validateProject(formData);

    if (Object.keys(validationErrors).length > 0) {
      setErrors(validationErrors);
      return;
    }

    setErrors({});
    onSubmit(formData);
  };

  return (
    <form onSubmit={handleSubmit}>
      {/* Project name */}
      <div className="form-group">
        <InputField
          label="Project Name"
          name="name"
          type="text"
          value={formData.name}
          onChange={handleChange}
        />

        {errors.name && <p className="error-message">{errors.name}</p>}
      </div>

      {/* Project description */}
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

export default ProjectForm;