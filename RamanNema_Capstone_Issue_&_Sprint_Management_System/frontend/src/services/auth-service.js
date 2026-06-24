import apiClient from "./api-client";

// Send registration details to the authentication API.
export const registerUser = async (userData) => {
  const response = await apiClient.post("/auth/register", userData);

  // Return the standardized API response body.
  return response.data;
};
