// Shared Axios client configured with the backend API base URL.
import axios from "axios";

const apiClient = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL,
});

// Export the configured client for all API service calls.
export default apiClient;
