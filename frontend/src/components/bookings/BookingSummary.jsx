import { formatDate, formatRange, formatRupees } from "../../utils/format.js";

export default function BookingSummary({ booking }) {
  const items = [
    ["Car", booking.vehicle.name],
    ["Dates", formatRange(booking.start_date, booking.end_date)],
    ["Booked on", formatDate(booking.booked_on)],
    ["Daily rate", formatRupees(booking.vehicle.daily_rate)],
  ];

  return (
    <dl className="summary">
      {items.map(([term, value]) => (
        <div key={term}>
          <dt>{term}</dt>
          <dd>{value}</dd>
        </div>
      ))}
    </dl>
  );
}
