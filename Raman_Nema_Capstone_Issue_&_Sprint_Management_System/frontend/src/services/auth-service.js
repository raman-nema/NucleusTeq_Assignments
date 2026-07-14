import apiClient from "./api-client";
import { API_ENDPOINTS } from "../constants/api-endpoints";
import { TOKEN_KEY } from "../constants/auth-constants";
import { encodePasswordPayload } from "../utils/password-encoding";

// Send registration details to the authentication API.
export async function registerUser(userData) {
  const response = await apiClient.post(
    API_ENDPOINTS.AUTH.REGISTER,
    encodePasswordPayload(userData),
  );

  return response.data;
}

// Send login credentials to the authentication API.
export async function loginUser(userData) {
  const response = await apiClient.post(
    API_ENDPOINTS.AUTH.LOGIN,
    encodePasswordPayload(userData),
  );

  return response.data;
}
export async function logoutUser() {
  const token = localStorage.getItem(TOKEN_KEY);

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
