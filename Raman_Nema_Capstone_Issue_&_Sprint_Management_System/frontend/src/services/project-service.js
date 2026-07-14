import apiClient from "./api-client";
import { API_ENDPOINTS } from "../constants/api-endpoints";

// Create a new project.
export async function createProject(projectData) {
  const response = await apiClient.post(API_ENDPOINTS.PROJECTS.BASE, projectData);

  return response.data;
}

// Fetch all projects.
export async function getProjects(params = {}) {
  const response = await apiClient.get(API_ENDPOINTS.PROJECTS.BASE, {
    params,
  });

  return response.data;
}

// Fetch a single project.
export async function getProjectById(projectId) {
  const response = await apiClient.get(API_ENDPOINTS.PROJECTS.BY_ID(projectId));

  return response.data;
}

// Update an existing project.
export async function updateProject(projectId, projectData) {
  const response = await apiClient.put(
    API_ENDPOINTS.PROJECTS.BY_ID(projectId),
    projectData,
  );

  return response.data;
}

// Delete a project.
export async function deleteProject(projectId) {
  const response = await apiClient.delete(API_ENDPOINTS.PROJECTS.BY_ID(projectId));

  return response.data;
}

// Assign a member to a project.
export async function assignMember(projectId, userId) {
  const response = await apiClient.post(API_ENDPOINTS.PROJECTS.MEMBERS(projectId), {
    user_id: userId,
  });
  return response.data;
}

// Remove a member from a project.
export async function removeMember(projectId, userId) {
  const response = await apiClient.delete(
    API_ENDPOINTS.PROJECTS.MEMBER_BY_ID(projectId, userId),
  );
  return response.data;
}
