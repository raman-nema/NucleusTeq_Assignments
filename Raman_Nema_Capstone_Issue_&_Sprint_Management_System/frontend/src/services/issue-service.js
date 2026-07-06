import apiClient from "./api-client";

// Create a new issue under a project.
export async function createIssue(projectId, issueData) {
  const response = await apiClient.post(
    `/projects/${projectId}/issues`,
    issueData,
  );

  return response.data;
}

// Fetch all issues for a project.
export async function getProjectIssues(projectId, params = {}) {
  const response = await apiClient.get(`/projects/${projectId}/issues`, {
    params,
  });

  return response.data;
}

// Fetch a single issue.
export async function getIssueById(issueId) {
  const response = await apiClient.get(`/issues/${issueId}`);

  return response.data;
}

// Update an existing issue.
export async function updateIssue(issueId, issueData) {
  const response = await apiClient.put(`/issues/${issueId}`, issueData);

  return response.data;
}

// Delete an issue.
export async function deleteIssue(issueId) {
  const response = await apiClient.delete(`/issues/${issueId}`);

  return response.data;
}

// Add a comment to an issue.
export async function addIssueComment(issueId, commentData) {
  const response = await apiClient.post(`/issues/${issueId}/comments`, commentData);

  return response.data;
}

// Delete a comment from an issue.
export async function deleteIssueComment(issueId, commentId) {
  const response = await apiClient.delete(`/issues/${issueId}/comments/${commentId}`);

  return response.data;
}
