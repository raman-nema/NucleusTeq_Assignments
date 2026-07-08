import apiClient from "./api-client";
import { API_ENDPOINTS } from "../constants/api-endpoints";

// Send registration details to the authentication API.
export async function registerUser(userData) {
  const response = await apiClient.post(API_ENDPOINTS.AUTH.REGISTER, userData);

  return response.data;
}

// Send login credentials to the authentication API.
export async function loginUser(userData) {
  const response = await apiClient.post(API_ENDPOINTS.AUTH.LOGIN, userData);

  return response.data;
}
export async function logoutUser() {
  const token = localStorage.getItem("token");

  const response = await apiClient.post(
    API_ENDPOINTS.AUTH.LOGOUT,
    {},
    {
      headers: {
        Authorization: `Bearer ${token}`,
      },
    },
  );

  return response.data;
}
