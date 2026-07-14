import {
  ROLE_KEY,
  TOKEN_KEY,
  USER_NAME_KEY,
} from "../constants/auth-constants";

export function logout() {
  localStorage.removeItem(TOKEN_KEY);
  localStorage.removeItem(ROLE_KEY);
  localStorage.removeItem(USER_NAME_KEY);
}
