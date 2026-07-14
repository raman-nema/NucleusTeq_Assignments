import apiClient from "./api-client";
import { API_ENDPOINTS } from "../constants/api-endpoints";

// Create a new issue under a project.
export async function createIssue(projectId, issueData) {
  const response = await apiClient.post(
    API_ENDPOINTS.PROJECTS.ISSUES(projectId),
    issueData,
  );

  return response.data;
}

// Fetch all issues for a project.
export async function getProjectIssues(projectId, params = {}) {
  const response = await apiClient.get(API_ENDPOINTS.PROJECTS.ISSUES(projectId), {
    params,
  });

  return response.data;
}

// Fetch a single issue.
export async function getIssueById(issueId) {
  const response = await apiClient.get(API_ENDPOINTS.ISSUES.BY_ID(issueId));

  return response.data;
}

// Update an existing issue.
export async function updateIssue(issueId, issueData) {
  const response = await apiClient.put(
    API_ENDPOINTS.ISSUES.BY_ID(issueId),
    issueData,
  );

  return response.data;
}

// Delete an issue.
export async function deleteIssue(issueId) {
  const response = await apiClient.delete(API_ENDPOINTS.ISSUES.BY_ID(issueId));

  return response.data;
}

// Add a comment to an issue.
export async function addIssueComment(issueId, commentData) {
  const response = await apiClient.post(
    API_ENDPOINTS.ISSUES.COMMENTS(issueId),
    commentData,
  );

  return response.data;
}

// Update a comment on an issue.
export async function updateIssueComment(issueId, commentId, commentData) {
  const response = await apiClient.put(
    API_ENDPOINTS.ISSUES.COMMENT_BY_ID(issueId, commentId),
    commentData,
  );

  return response.data;
}

// Delete a comment from an issue.
export async function deleteIssueComment(issueId, commentId) {
  const response = await apiClient.delete(
    API_ENDPOINTS.ISSUES.COMMENT_BY_ID(issueId, commentId),
  );

  return response.data;
}
