import { LEVEL_LABELS } from "../../constants/labels.js";
import { Capsule, StatusCapsule } from "../ui/Capsule.jsx";

export default function DetailHeader({ booking }) {
  const { risk } = booking;
  return (
    <div className="detail-header">
      <div>
        <h2>{booking.renter_name}</h2>
        <div className="capsule-row">
          <StatusCapsule status={booking.status} />
          <Capsule>Booking #{booking.id}</Capsule>
        </div>
      </div>
      <div className={`score ${risk.level}`}>
        <span className="score-value">{risk.score}</span>
        <span className="score-label">{LEVEL_LABELS[risk.level]}</span>
      </div>
    </div>
  );
}
