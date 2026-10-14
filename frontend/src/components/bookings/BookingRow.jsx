import { STATUS_LABELS } from "../../constants/labels.js";
import { formatRange } from "../../utils/format.js";
import { RiskCapsule } from "../ui/Capsule.jsx";

export default function BookingRow({ booking, selected, onSelect }) {
  return (
    <button className={`booking-row ${selected ? "selected" : ""}`} onClick={() => onSelect(booking.id)}>
      <span className="row-name">{booking.renter_name}</span>
      <RiskCapsule level={booking.risk_level} score={booking.risk_score} />
      <span className="row-meta">
        {formatRange(booking.start_date, booking.end_date)} · {booking.vehicle_name}
      </span>
      <span className="row-status">{STATUS_LABELS[booking.status]}</span>
    </button>
  );
}
