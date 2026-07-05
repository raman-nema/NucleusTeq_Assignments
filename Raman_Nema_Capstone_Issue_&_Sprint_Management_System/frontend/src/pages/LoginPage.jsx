import { useState } from "react";
import { useNavigate } from "react-router-dom";

import InputField from "../components/common/InputField";
import Button from "../components/common/Button";

import { loginUser } from "../services/auth-service";
import { saveToken, saveRole, saveUserName } from "../utils/storage";
import { validateLogin } from "../../src/utils/validations";
import { useNotification } from "../context/useNotification";

import "../styles/LoginPage.css";

function LoginPage() {
  const navigate = useNavigate();
  const { showNotification } = useNotification();

  // Form and UI state
  const [formData, setFormData] = useState({ email: "", password: "" });
  const [loading, setLoading] = useState(false); // prevents multipole loading req
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

      showNotification(response.message);
      navigate("/projects");
    } catch (error) {
      const message = error.response?.data?.message || "Unable to login.";
      setError(message);
      showNotification(message, "error");
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
