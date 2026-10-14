import { useState } from "react";
import { OPEN_STATUSES, RISK_FILTERS } from "../../constants/labels.js";
import BookingGroup from "./BookingGroup.jsx";
import RiskFilters from "./RiskFilters.jsx";

const matchesFilter = (filter) => (booking) => filter === "all" || booking.risk_level === filter;

export default function BookingList({ bookings, selectedId, onSelect }) {
  const [filter, setFilter] = useState("all");

  const counts = Object.fromEntries(
    RISK_FILTERS.map(({ value }) => [value, bookings.filter(matchesFilter(value)).length]),
  );
  const visible = bookings.filter(matchesFilter(filter));
  const waiting = visible.filter((booking) => OPEN_STATUSES.has(booking.status));
  const past = visible.filter((booking) => !OPEN_STATUSES.has(booking.status));

  return (
    <div className="card list-card">
      <RiskFilters value={filter} counts={counts} onChange={setFilter} />
      <div className="list-scroll">
        {visible.length === 0 && <p className="empty muted">No customers in this group.</p>}
        <BookingGroup
          title="Waiting for your decision"
          hint="Approve or decline these"
          tone="open"
          bookings={waiting}
          selectedId={selectedId}
          onSelect={onSelect}
        />
        <BookingGroup
          title="Past customers"
          hint="Already decided or completed"
          tone="closed"
          bookings={past}
          selectedId={selectedId}
          onSelect={onSelect}
        />
      </div>
    </div>
  );
}
