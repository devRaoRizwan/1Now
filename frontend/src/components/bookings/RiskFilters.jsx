import { RISK_FILTERS } from "../../constants/labels.js";

export default function RiskFilters({ value, counts, onChange }) {
  return (
    <div className="filters" role="tablist" aria-label="Filter by risk">
      {RISK_FILTERS.map((filter) => (
        <button
          key={filter.value}
          role="tab"
          aria-selected={value === filter.value}
          className={`filter-capsule ${value === filter.value ? "active" : ""}`}
          onClick={() => onChange(filter.value)}
        >
          {filter.label}
          <span className="filter-count">{counts[filter.value]}</span>
        </button>
      ))}
    </div>
  );
}
