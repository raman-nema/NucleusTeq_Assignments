import apiClient from "./api-client";

export async function getAdminDashboard(params = {}) {
  const response = await apiClient.get("/admin/dashboard", {
    params,
  });

  return response.data;
}

export async function updateDashboardUser(userId, userData) {
  const response = await apiClient.put(`/admin/users/${userId}`, userData);

  return response.data;
}
