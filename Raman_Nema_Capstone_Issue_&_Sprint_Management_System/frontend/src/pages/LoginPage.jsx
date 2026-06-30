import { useState } from "react";
import { useNavigate } from "react-router-dom";

import InputField from "../components/common/InputField";
import Button from "../components/common/Button";

import { loginUser } from "../services/auth-service";
import { saveToken, saveRole } from "../utils/storage";
import { validateLogin } from "../../src/utils/validations";

import "../styles/LoginPage.css";

function LoginPage() {
  const navigate = useNavigate();

  // Keep login form values and UI feedback in local component state.
  const [formData, setFormData] = useState({ email: "", password: "" });
  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState("");
  const [error, setError] = useState("");
  const [errors, setErrors] = useState({});

  const handleChange = (event) => {
    const { name, value } = event.target;
    // Update only the input field that changed.
    setFormData((prev) => ({ ...prev, [name]: value }));
  };

  const handleSubmit = async (event) => {
    event.preventDefault();
    // Reset previous success and error messages.
    setMessage("");
    setError("");

    // Validate all form fields.
    const validationErrors = validateLogin(formData);

    if (Object.keys(validationErrors).length > 0) {
      setErrors(validationErrors);
      return;
    }

    // Clear previous validation errors.
    setErrors({});

    setLoading(true);

    try {
      // Send credentials to the backend and receive the login response.
      const response = await loginUser(formData);
      // Save session details for authenticated requests and role-based access.
      saveToken(response.data.access_token);
      saveRole(response.data.role);
      setMessage(response.message);

      navigate("/projects");

    } catch (error) {
      // Show the backend error message when login fails.
      setError(error.response?.data?.message || "Unable to login.");
    } finally {
      // Re-enable the login button after the request finishes.
      setLoading(false);
    }
  };

  return (
    <div className="login-page">
      <div className="login-card">
        <h1 className="app-title">SprintFlow</h1>
        <p className="page-subtitle">Welcome back! Please sign in.</p>

        <form onSubmit={handleSubmit}>
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
            <InputField
              label="Password"
              name="password"
              type="password"
              value={formData.password}
              onChange={handleChange}
            />
            {errors.password && (
              <p className="error-message">{errors.password}</p>
            )}
          </div>

          {message && <p className="success-message">{message}</p>}
          {error && <p className="error-message">{error}</p>}

          <Button
            type="submit"
            disabled={loading}
            text={loading ? "Logging in..." : "Login"}
          />
        </form>

        <p className="auth-switch">
          Don't have an account?{" "}
          <span className="auth-link" onClick={() => navigate("/register")}>
            {/* Navigate new users to the registration page. */}
            Register
          </span>
        </p>
      </div>
    </div>
  );
}

export default LoginPage;
