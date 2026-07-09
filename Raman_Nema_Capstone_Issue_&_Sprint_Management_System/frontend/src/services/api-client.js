import axios from "axios";
import { API_ENDPOINTS } from "../constants/api-endpoints";

const apiClient = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL,
});

// Attach the access token to every authenticated request.
apiClient.interceptors.request.use((config) => {
  const token = localStorage.getItem("access_token");

  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }

  return config;
});

const AUTH_ROUTES = [
  API_ENDPOINTS.AUTH.LOGIN,
  API_ENDPOINTS.AUTH.REGISTER,
];

// Redirect to login on protected-route 401 responses.
apiClient.interceptors.response.use(
  (response) => response,
  (error) => {
    const requestUrl = error.config?.url || "";
    const isAuthRequest = AUTH_ROUTES.some((route) =>
      requestUrl.endsWith(route),
    );

    if (error.response?.status === 401 && !isAuthRequest) {
      localStorage.clear();
      window.location.replace("/login");
    }
    return Promise.reject(error);
  }
);

export default apiClient;
