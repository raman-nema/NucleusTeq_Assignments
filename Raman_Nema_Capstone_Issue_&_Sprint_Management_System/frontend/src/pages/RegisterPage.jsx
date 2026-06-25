
import { useState } from "react";

import InputField from "../components/common/InputField";
import Button from "../components/common/Button";

import { registerUser } from "../services/auth-service";

import "../styles/RegisterPage.css";

function RegisterPage() {
  // Stores all registration form values in one state object.
  const [formData, setFormData] = useState({
    name: "",
    email: "",
    password: "",
    role: "MEMBER",
  });

  // Updates the matching form field based on the input's name attribute.
  const handleChange = (event) => {
    const { name, value } = event.target;

    setFormData((previousData) => ({
      ...previousData,
      [name]: value,
    }));
  };

  // Sends the registration request and resets the form after success.
  const handleSubmit = async (event) => {
    event.preventDefault();

    try {
      const response = await registerUser(formData);

      alert(response.message);

      setFormData({
        name: "",
        email: "",
        password: "",
        role: "MEMBER",
      });
    } catch (error) {
      const message = error.response?.data?.message || "Registration Failed";

      alert(message);

      console.error(error);
    }
  };

  // what actually needed to be rendered in the screen
  return (
    <div className="register-page">
      <div className="register-card">
        <h1 className="app-title">SprintFlow</h1>

        <form onSubmit={handleSubmit}>
          <div className="form-group">
            <InputField
              label="Name"
              name="name"
              type="text"
              value={formData.name}
              onChange={handleChange}
            />
          </div>
          <div className="form-group">
            <InputField
              label="Email"
              name="email"
              type="email"
              value={formData.email}
              onChange={handleChange}
            />
          </div>
          <div className="form-group">
            <InputField
              label="Password"
              name="password"
              type="password"
              value={formData.password}
              onChange={handleChange}
            />
          </div>
          <div className="form-group">
            <label>Role</label>
            {/* Allows new users to choose the role assigned to their account. */}
            <select name="role" value={formData.role} onChange={handleChange}>
              <option value="MEMBER">Member</option>
              <option value="VIEWER">Viewer</option>
            </select>
          </div>
          <Button text="Register" type="submit" />
        </form>
      </div>
    </div>
  );
}

export default RegisterPage;