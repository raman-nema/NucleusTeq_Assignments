import axios from "axios";

// Shared Axios client configured with the backend API base URL.
const axiosInstance = axios.create({
  baseURL: "http://localhost:8000",
});

export default axiosInstance;
