import {
  TOKEN_KEY,
  ROLE_KEY,
  USER_NAME_KEY,
} from "../constants/auth-constants";

export function saveToken(token) {
  // Store the login token so authenticated API calls can reuse it.
  localStorage.setItem(TOKEN_KEY, token);
}

export function getToken() {
  return localStorage.getItem(TOKEN_KEY);
}

export function removeToken() {
  // Remove the saved token when the user logs out or the session expires.
  localStorage.removeItem(TOKEN_KEY);
}

export function saveRole(role) {
  // Persist the user role for role-based routing and UI decisions.
  localStorage.setItem(ROLE_KEY, role);
}

export function getRole() {
  return localStorage.getItem(ROLE_KEY);
}

export function saveUserName(name) {
  localStorage.setItem(USER_NAME_KEY, name);
}

export function getUserName() {
  return localStorage.getItem(USER_NAME_KEY);
}

export function clearStorage() {
  // Clear all local session data during logout.
  localStorage.clear();
}
