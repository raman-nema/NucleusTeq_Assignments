// Reusable controlled input field with label, value, and change handling.
function InputField({ label, name, type, value, onChange, className = "" }) {
  return (
    <div className={`input-field ${className}`}>
      <label htmlFor={name}>{label}</label>

      <input
        id={name}
        name={name}
        type={type}
        value={value}
        onChange={onChange}
      />
    </div>
  );
}

export default InputField;