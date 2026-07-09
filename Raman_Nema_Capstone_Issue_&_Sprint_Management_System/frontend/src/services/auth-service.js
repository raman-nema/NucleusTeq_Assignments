import apiClient from "./api-client";

// Send registration details to the authentication API.
export async function registerUser(userData) {
  const response = await apiClient.post("/auth/register", userData);

  return response.data;
}

// Send login credentials to the authentication API.
export async function loginUser(userData) {
  const response = await apiClient.post("/auth/login", userData);

  return response.data;
}
