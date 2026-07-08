export const API_ENDPOINTS = {
  AUTH: {
    REGISTER: "/auth/register",
    LOGIN: "/auth/login",
    LOGOUT: "/auth/logout",
  },
  PROJECTS: {
    BASE: "/projects",
    BY_ID: (projectId) => `/projects/${projectId}`,
    MEMBERS: (projectId) => `/projects/${projectId}/members`,
    MEMBER_BY_ID: (projectId, userId) => `/projects/${projectId}/members/${userId}`,
    SPRINTS: (projectId) => `/projects/${projectId}/sprints`,
    ISSUES: (projectId) => `/projects/${projectId}/issues`,
  },
  SPRINTS: {
    BY_ID: (sprintId) => `/sprints/${sprintId}`,
  },
  ISSUES: {
    BY_ID: (issueId) => `/issues/${issueId}`,
    COMMENTS: (issueId) => `/issues/${issueId}/comments`,
    COMMENT_BY_ID: (issueId, commentId) => `/issues/${issueId}/comments/${commentId}`,
  },
};
