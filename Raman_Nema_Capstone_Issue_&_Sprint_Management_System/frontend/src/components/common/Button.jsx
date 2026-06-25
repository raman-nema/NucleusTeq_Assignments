// Reusable button component with configurable text, type, and styling.
function Button({ text, type = "button", className = "" }) {
  return (
    <button className={className} type={type}>
      {text}
    </button>
  );
}

export default Button;
