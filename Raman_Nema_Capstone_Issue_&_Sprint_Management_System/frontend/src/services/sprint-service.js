import apiClient from "./api-client";

// Create a new sprint under a project.
export async function createSprint(projectId, sprintData) {
  const response = await apiClient.post(
    `/projects/${projectId}/sprints`,
    sprintData,
  );

  return response.data;
}

// Fetch all sprints for a project.
export async function getProjectSprints(projectId) {
  const response = await apiClient.get(`/projects/${projectId}/sprints`);

  return response.data;
}

// Fetch a single sprint.
export async function getSprintById(sprintId) {
  const response = await apiClient.get(`/sprints/${sprintId}`);

  return response.data;
}

// Update an existing sprint.
export async function updateSprint(sprintId, sprintData) {
  const response = await apiClient.put(`/sprints/${sprintId}`, sprintData);

  return response.data;
}

// Delete a sprint.
export async function deleteSprint(sprintId) {
  const response = await apiClient.delete(`/sprints/${sprintId}`);

  return response.data;
}
