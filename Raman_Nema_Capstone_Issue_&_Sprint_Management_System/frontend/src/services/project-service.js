import apiClient from "./api-client";

// Create a new project.
export async function createProject(projectData) {
  const response = await apiClient.post("/projects", projectData);

  return response.data;
}

// Fetch all projects.
export async function getProjects() {
  const response = await apiClient.get("/projects");

  return response.data;
}

// Fetch a single project.
export async function getProjectById(projectId) {
  const response = await apiClient.get(`/projects/${projectId}`);

  return response.data;
}

// Update an existing project.
export async function updateProject(projectId, projectData) {
  const response = await apiClient.put(`/projects/${projectId}`, projectData);

  return response.data;
}

// Delete a project.
export async function deleteProject(projectId) {
  const response = await apiClient.delete(`/projects/${projectId}`);

  return response.data;
}
