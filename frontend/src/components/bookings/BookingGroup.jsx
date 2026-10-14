import BookingRow from "./BookingRow.jsx";

export default function BookingGroup({ title, hint, tone, bookings, selectedId, onSelect }) {
  if (bookings.length === 0) return null;

  return (
    <section className={`booking-group ${tone}`}>
      <div className="group-heading">
        <span className="group-mark" />
        <div className="group-text">
          <span className="group-title">{title}</span>
          <span className="group-hint">{hint}</span>
        </div>
        <span className="group-count">{bookings.length}</span>
      </div>
      <ul className="booking-list">
        {bookings.map((booking) => (
          <li key={booking.id}>
            <BookingRow booking={booking} selected={booking.id === selectedId} onSelect={onSelect} />
          </li>
        ))}
      </ul>
    </section>
  );
}
