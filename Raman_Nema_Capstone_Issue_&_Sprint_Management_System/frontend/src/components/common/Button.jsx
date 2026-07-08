// Reusable button component with configurable text, type and styling.
function Button({
  text,
  type = "button",
  className,
  onClick,
  disabled = false,
}) {
  return (
    <button
      className={className}
      type={type}
      onClick={onClick}
      disabled={disabled}
    >
      {text}
    </button>
  );
}

export default Button;
