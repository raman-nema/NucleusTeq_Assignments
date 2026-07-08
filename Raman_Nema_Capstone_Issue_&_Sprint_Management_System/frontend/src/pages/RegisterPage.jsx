import { useState } from "react";
import { useNavigate } from "react-router-dom";

import InputField from "../components/common/InputField";
import Button from "../components/common/Button";

import { registerUser } from "../services/auth-service";
import { useNotification } from "../context/useNotification";

import "../styles/auth-register-styles";

import { validateRegister } from "../../src/utils/validations";

function RegisterPage() {
  const navigate = useNavigate();
  const { showNotification } = useNotification();

  // Keep all registration form fields in one state object.
  const [formData, setFormData] = useState({
    name: "",
    email: "",
    password: "",
    role: "MEMBER",
  });

  const [errors, setErrors] = useState({});
  const [showPassword, setShowPassword] = useState(false);

  const handleChange = (event) => {
    const { name, value } = event.target;
    // Update the field that changed while preserving the other form values.
    setFormData((prev) => ({ ...prev, [name]: value }));
  };

  const handleSubmit = async (event) => {
    event.preventDefault();

    // Validate all form fields.
    const validationErrors = validateRegister(formData);

    if (Object.keys(validationErrors).length > 0) {
      setErrors(validationErrors);
      return;
    }

    // Clear previous validation errors.
    setErrors({});

    try {
      // Send the completed form data to the backend registration endpoint.
      const response = await registerUser(formData);
      showNotification(response.message);
      // Reset the form after successful registration.
      setFormData({ name: "", email: "", password: "", role: "MEMBER" });
    } catch (error) {
      // Show the backend error message when available.
      const message = error.response?.data?.message || "Registration Failed";
      showNotification(message, "error");
      console.error(error);
    }
  };

  return (
    <div className="register-page">
      <div className="register-card">
        <h1 className="app-title">SprintFlow</h1>
        <p className="page-subtitle">Create your account to get started</p>

        <form onSubmit={handleSubmit}>
          <div className="form-group">
            <InputField
              label="Name"
              name="name"
              type="text"
              value={formData.name}
              onChange={handleChange}
            />
            {errors.name && <p className="error-message">{errors.name}</p>}
          </div>

          <div className="form-group">
            <InputField
              label="Email"
              name="email"
              type="email"
              value={formData.email}
              onChange={handleChange}
            />
            {errors.email && <p className="error-message">{errors.email}</p>}
          </div>

          <div className="form-group">
            <div className="password-wrapper">
              <InputField
                label="Password"
                name="password"
                type={showPassword ? "text" : "password"}
                value={formData.password}
                onChange={handleChange}
              />
              <button
                type="button"
                className="password-toggle"
                onClick={() => setShowPassword((prev) => !prev)}
                aria-label={showPassword ? "Hide password" : "Show password"}
              >
                {showPassword ? "Hide" : "Show"}
              </button>
            </div>
            {errors.password && (
              <p className="error-message">{errors.password}</p>
            )}
          </div>

          <div className="form-group">
            <label>Role</label>
            <div className="select-wrapper">
              <select name="role" value={formData.role} onChange={handleChange}>
                <option value="#">Select a role</option>
                <option value="MEMBER">Member</option>
                <option value="VIEWER">Viewer</option>
              </select>
              {errors.role && <p className="error-message">{errors.role}</p>}
            </div>
          </div>

          <Button text="Register" type="submit" />
        </form>

        <p className="auth-switch">
          Already have an account?{" "}
          <span className="auth-link" onClick={() => navigate("/login")}>
            {/* Navigate existing users to the login page. */}
            Login
          </span>
        </p>
      </div>
    </div>
  );
}

export default RegisterPage;
