export function formatDisplayDate(value) {
  if (!value) return "Not set";

  return new Date(value).toLocaleDateString("en-IN", {
    day: "2-digit",
    month: "short",
    year: "numeric",
  });
}
