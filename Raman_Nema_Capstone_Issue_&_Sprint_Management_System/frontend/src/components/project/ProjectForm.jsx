import { useEffect, useState } from "react";
import InputField from "../common/InputField";
import Button from "../common/Button";
import { validateProject } from "../../utils/validations";

function ProjectForm({ initialData, onSubmit, onCancel, loading }) {
  // Store the project form fields.
  const [formData, setFormData] = useState({
    name: "",
    description: "",
  });

  // Store validation errors.
  const [errors, setErrors] = useState({});

  // Populate the form when editing a project.
  useEffect(() => {
    if (initialData) {
      setFormData({
        name: initialData.name,
        description: initialData.description,
      });
    } else {
      setFormData({
        name: "",
        description: "",
      });
    }

    // Clear validation errors whenever the form opens.
    setErrors({});
  }, [initialData]);

  const handleChange = (event) => {
    const { name, value } = event.target;

    // Update the modified field.
    setFormData((previous) => ({
      ...previous,
      [name]: value,
    }));

    // Remove the validation error while typing.
    setErrors((previous) => ({
      ...previous,
      [name]: "",
    }));
  };

  const handleSubmit = (event) => {
    event.preventDefault();

    // Validate the form.
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

      <div className="form-group">
        <label>Description</label>

        <textarea
          name="description"
          value={formData.description}
          onChange={handleChange}
          rows="5"
        />

        {errors.description && (
          <p className="error-message">{errors.description}</p>
        )}
      </div>

      <div className="button-group">
        <Button
          type="submit"
          disabled={loading}
          text={loading ? "Saving..." : "Save"}
        />

        <Button type="button" text="Cancel" onClick={onCancel} />
      </div>
    </form>
  );
}

export default ProjectForm;
