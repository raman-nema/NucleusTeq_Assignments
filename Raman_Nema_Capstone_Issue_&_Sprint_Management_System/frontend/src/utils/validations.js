/**
 * Validate the registration form.
 * Returns an object containing validation errors.
 */
export function validateRegister(formData) {
  const errors = {};

  // Name Validation
  if (!formData.name.trim()) {
    errors.name = "Name is required.";
  } else if (formData.name.trim().length < 3) {
    errors.name = "Name must be at least 3 characters.";
  } else if (formData.name.trim().length > 50) {
    errors.name = "Name cannot exceed 50 characters.";
  }

  // Email Validation

  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

  const allowedDomain = "@company.com";

  if (!formData.email.trim()) {
    errors.email = "Email is required.";
  } else if (!emailRegex.test(formData.email)) {
    errors.email = "Please enter a valid email address.";
  } else if (!formData.email.endsWith(allowedDomain)) {
    errors.email = `Only ${allowedDomain} email addresses are allowed.`;
  }

  // Password Validation
  const passwordRegex =
    /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&]).{8,20}$/;

  if (!formData.password) {
    errors.password = "Password is required.";
  } else if (!passwordRegex.test(formData.password)) {
    errors.password =
      "Password must be 8-20 characters long and contain an uppercase letter, lowercase letter, number and special character.";
  }

  // Role Validation
  if (formData.role !== "MEMBER" && formData.role !== "VIEWER") {
    errors.role = "Please select a valid role.";
  }

  return errors;
}
/**
 * Validate the login form.
 * Returns an object containing validation errors.
 */
export function validateLogin(formData) {
  const errors = {};

  // Email Validation
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

  const allowedDomain = "@company.com";

  if (!formData.email.trim()) {
    errors.email = "Email is required.";
  } else if (!emailRegex.test(formData.email)) {
    errors.email = "Please enter a valid email address.";
  } else if (!formData.email.endsWith(allowedDomain)) {
    errors.email = `Only ${allowedDomain} email addresses are allowed.`;
  }

  // Password Validation
  if (!formData.password) {
    errors.password = "Password is required.";
  } else if (formData.password.length < 8) {
    errors.password = "Password must be at least 8 characters.";
  }

  return errors;
}

/**
 * Validate the project form fields.
 */
export function validateProject(formData) {
  const errors = {};

  if (!formData.name.trim()) {
    errors.name = "Project name is required.";
  } else if (formData.name.trim().length < 3) {
    errors.name = "Project name must be at least 3 characters.";
  } else if (formData.name.trim().length > 100) {
    errors.name = "Project name cannot exceed 100 characters.";
  }

  if (!formData.description.trim()) {
    errors.description = "Project description is required.";
  } else if (formData.description.trim().length < 10) {
    errors.description = "Project description must be at least 10 characters.";
  } else if (formData.description.trim().length > 500) {
    errors.description = "Project description cannot exceed 500 characters.";
  }

  return errors;
}
