const PASSWORD_ENCODING_PREFIX = "encoded:";

export function encodePassword(password) {
  const bytes = new TextEncoder().encode(password);
  const binary = Array.from(bytes, (byte) => String.fromCharCode(byte)).join("");

  return `${PASSWORD_ENCODING_PREFIX}${btoa(binary)}`;
}

export function encodePasswordPayload(userData) {
  return {
    ...userData,
    password: encodePassword(userData.password),
  };
}
