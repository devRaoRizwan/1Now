import Dropdown from "./Dropdown.jsx";

export function TextField({ label, wide = false, ...inputProps }) {
  return (
    <label className={`field ${wide ? "wide" : ""}`}>
      <span className="field-label">{label}</span>
      {inputProps.rows ? <textarea {...inputProps} /> : <input {...inputProps} />}
    </label>
  );
}

// A <div>, not a <label>: a label would re-open the dropdown when an option is clicked.
export function SelectField({ label, wide = false, ...dropdownProps }) {
  return (
    <div className={`field ${wide ? "wide" : ""}`}>
      <span className="field-label">{label}</span>
      <Dropdown {...dropdownProps} />
    </div>
  );
}
