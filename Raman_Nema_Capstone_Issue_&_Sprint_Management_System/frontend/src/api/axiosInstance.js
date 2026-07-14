import axios from "axios";
import { APP_CONFIG } from "../config/app-config";

// Shared Axios client configured with the backend API base URL.
const axiosInstance = axios.create({
  baseURL: APP_CONFIG.API_BASE_URL,
});

export default axiosInstance;
