import { useState } from "react";
import { useNavigate } from "react-router-dom";

import InputField from "../components/common/InputField";
import Button from "../components/common/Button";

import { loginUser } from "../services/auth-service";
import { saveToken, saveRole, saveUserName } from "../utils/storage";
import { validateLogin } from "../../src/utils/validations";

import "../styles/LoginPage.css";

function LoginPage() {
  const navigate = useNavigate();

  // Form and UI state
  const [formData, setFormData] = useState({ email: "", password: "" });
  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState("");
  const [error, setError] = useState("");
  const [errors, setErrors] = useState({});
  const [showPassword, setShowPassword] = useState(false);

  // Update form fields
  const handleChange = (event) => {
    const { name, value } = event.target;
    setFormData((prev) => ({ ...prev, [name]: value }));
  };

  // Validate and submit login form
  const handleSubmit = async (event) => {
    event.preventDefault();
    setMessage("");
    setError("");

    const validationErrors = validateLogin(formData);

    if (Object.keys(validationErrors).length > 0) {
      setErrors(validationErrors);
      return;
    }

    setErrors({});
    setLoading(true);

    try {
      const response = await loginUser(formData);

      // Store user session
      saveToken(response.data.access_token);
      saveUserName(response.data.name);
      saveRole(response.data.role);

      setMessage(response.message);
      navigate("/projects");
    } catch (error) {
      setError(error.response?.data?.message || "Unable to login.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="login-page">
      <div className="login-card">
        {/* Login header */}
        <h1 className="app-title">SprintFlow</h1>
        <p className="page-subtitle">Welcome back! Please sign in.</p>

        <form onSubmit={handleSubmit}>
          {/* Email field */}
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

          {/* Password field */}
          <div className="form-group">
            <div className="password-wrapper">
              <InputField
                label="Password"
                name="password"
                type={showPassword ? "text" : "password"}
                value={formData.password}
                onChange={handleChange}
              />

              {/* Toggle password visibility */}
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

          {/* Success and error messages */}
          {message && <p className="success-message">{message}</p>}
          {error && <p className="error-message">{error}</p>}

          {/* Login button */}
          <Button
            type="submit"
            disabled={loading}
            text={loading ? "Logging in..." : "Login"}
          />
        </form>

        {/* Registration link */}
        <p className="auth-switch">
          Don't have an account?{" "}
          <span className="auth-link" onClick={() => navigate("/register")}>
            Register
          </span>
        </p>
      </div>
    </div>
  );
}

export default LoginPage;
