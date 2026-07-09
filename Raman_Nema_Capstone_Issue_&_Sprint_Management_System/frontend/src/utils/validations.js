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

/**
 * Validate the sprint form fields.
 */
export function validateSprint(formData) {
  const errors = {};
  const allowedStatuses = ["PLANNED", "ACTIVE", "COMPLETED"];

  if (!formData.name.trim()) {
    errors.name = "Sprint name is required.";
  } else if (formData.name.trim().length < 3) {
    errors.name = "Sprint name must be at least 3 characters.";
  } else if (formData.name.trim().length > 100) {
    errors.name = "Sprint name cannot exceed 100 characters.";
  }

  if (!formData.goal.trim()) {
    errors.goal = "Sprint goal is required.";
  } else if (formData.goal.trim().length < 10) {
    errors.goal = "Sprint goal must be at least 10 characters.";
  } else if (formData.goal.trim().length > 500) {
    errors.goal = "Sprint goal cannot exceed 500 characters.";
  }

  if (!formData.start_date) {
    errors.start_date = "Start date is required.";
  }

  if (!formData.end_date) {
    errors.end_date = "End date is required.";
  }

  if (
    formData.start_date &&
    formData.end_date &&
    formData.end_date < formData.start_date
  ) {
    errors.end_date = "End date cannot be before the start date.";
  }

  if (!allowedStatuses.includes(formData.status)) {
    errors.status = "Please select a valid sprint status.";
  }

  return errors;
}
