import apiClient from "./api-client";
import { API_ENDPOINTS } from "../constants/api-endpoints";

// Create a new sprint under a project.
export async function createSprint(projectId, sprintData) {
  const response = await apiClient.post(
    API_ENDPOINTS.PROJECTS.SPRINTS(projectId),
    sprintData,
  );

  return response.data;
}

// Fetch all sprints for a project.
export async function getProjectSprints(projectId, params = {}) {
  const response = await apiClient.get(API_ENDPOINTS.PROJECTS.SPRINTS(projectId), {
    params,
  });

  return response.data;
}

// Fetch a single sprint.
export async function getSprintById(sprintId) {
  const response = await apiClient.get(API_ENDPOINTS.SPRINTS.BY_ID(sprintId));

  return response.data;
}

// Update an existing sprint.
export async function updateSprint(sprintId, sprintData) {
  const response = await apiClient.put(
    API_ENDPOINTS.SPRINTS.BY_ID(sprintId),
    sprintData,
  );

  return response.data;
}

// Delete a sprint.
export async function deleteSprint(sprintId) {
  const response = await apiClient.delete(API_ENDPOINTS.SPRINTS.BY_ID(sprintId));

  return response.data;
}
