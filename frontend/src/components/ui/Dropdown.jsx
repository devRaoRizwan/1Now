import { useEffect, useRef, useState } from "react";
import Icon from "./Icon.jsx";

// A styled replacement for <select>. Options: { value, label, description?, icon? }.
export default function Dropdown({ value, options, onChange, placeholder = "Select…", variant = "field", placement = "bottom", ariaLabel }) {
  const [open, setOpen] = useState(false);
  const [active, setActive] = useState(0);
  const root = useRef(null);

  const selectedIndex = options.findIndex((option) => String(option.value) === String(value));
  const selected = options[selectedIndex];

  useEffect(() => {
    if (!open) return undefined;
    const closeOnOutsideClick = (event) => !root.current?.contains(event.target) && setOpen(false);
    document.addEventListener("mousedown", closeOnOutsideClick);
    return () => document.removeEventListener("mousedown", closeOnOutsideClick);
  }, [open]);

  function openMenu() {
    setActive(Math.max(selectedIndex, 0));
    setOpen(true);
  }

  function choose(option) {
    onChange(option.value);
    setOpen(false);
  }

  function handleKeyDown(event) {
    const keys = {
      ArrowDown: () => (open ? setActive((index) => Math.min(options.length - 1, index + 1)) : openMenu()),
      ArrowUp: () => (open ? setActive((index) => Math.max(0, index - 1)) : openMenu()),
      Enter: () => (open ? choose(options[active]) : openMenu()),
      " ": () => (open ? choose(options[active]) : openMenu()),
      Escape: () => setOpen(false),
      Tab: () => setOpen(false),
    };
    const action = keys[event.key];
    if (!action) return;
    if (event.key !== "Tab") event.preventDefault();
    if (event.key === "Escape" && open) event.stopPropagation();
    action();
  }

  return (
    <div className={`dropdown dropdown-${variant} ${open ? "open" : ""}`} ref={root}>
      <button
        type="button"
        className="dropdown-trigger"
        aria-haspopup="listbox"
        aria-expanded={open}
        aria-label={ariaLabel}
        onClick={() => (open ? setOpen(false) : openMenu())}
        onKeyDown={handleKeyDown}
      >
        {selected?.icon}
        <span className="dropdown-text">
          <span className={selected ? "dropdown-label" : "dropdown-placeholder"}>{selected?.label ?? placeholder}</span>
          {variant === "account" && selected?.description && <span className="dropdown-description">{selected.description}</span>}
        </span>
        <Icon name="chevron" size={12} className="dropdown-chevron" />
      </button>

      {open && (
        <ul className={`dropdown-menu ${placement}`} role="listbox">
          {options.map((option, index) => (
            <li
              key={option.value}
              role="option"
              aria-selected={index === selectedIndex}
              className={`dropdown-option ${index === active ? "active" : ""} ${index === selectedIndex ? "selected" : ""}`}
              onMouseEnter={() => setActive(index)}
              onMouseDown={(event) => {
                event.preventDefault();
                choose(option);
              }}
            >
              {option.icon}
              <span className="dropdown-text">
                <span className="dropdown-label">{option.label}</span>
                {option.description && <span className="dropdown-description">{option.description}</span>}
              </span>
              {index === selectedIndex && <Icon name="check" size={14} className="dropdown-check" />}
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}
