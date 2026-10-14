import { api } from "../../api/client.js";
import { OPEN_STATUSES, STATUS_LABELS } from "../../constants/labels.js";
import { useFetch } from "../../hooks/useFetch.js";
import BookingSummary from "./BookingSummary.jsx";
import CustomerDetails from "./CustomerDetails.jsx";
import DecisionBar from "./DecisionBar.jsx";
import DetailHeader from "./DetailHeader.jsx";
import NetworkReports from "./NetworkReports.jsx";
import ReasonsTable from "./ReasonsTable.jsx";
import ReportForm from "./ReportForm.jsx";

export default function BookingDetail({ bookingId, hostId, version, onChanged, notify }) {
  const { data: booking, error, setData } = useFetch(
    () => (bookingId ? api.booking(bookingId, hostId) : Promise.resolve(null)),
    [bookingId, hostId, version],
  );

  if (!bookingId) {
    return (
      <div className="card detail-card empty-state">
        <h3>No booking selected</h3>
        <p className="muted">Choose a customer from the list to see their risk check.</p>
      </div>
    );
  }
  if (error) return <div className="card detail-card error">{error}</div>;
  if (!booking) return <div className="card detail-card muted">Loading…</div>;

  function applyUpdate(updated, message) {
    setData(updated);
    onChanged();
    notify(message);
  }

  async function decide(decision) {
    try {
      applyUpdate(await api.decide(booking.id, hostId, decision), `Booking ${STATUS_LABELS[decision].toLowerCase()}`);
    } catch (err) {
      notify(err.message);
    }
  }

  return (
    <article className="card detail-card">
      <DetailHeader booking={booking} />
      <BookingSummary booking={booking} />
      <DecisionBar risk={booking.risk} canDecide={OPEN_STATUSES.has(booking.status)} onDecide={decide} />
      <ReasonsTable risk={booking.risk} />
      <NetworkReports matches={booking.network_matches} />
      <CustomerDetails booking={booking} />
      <ReportForm
        booking={booking}
        hostId={hostId}
        onReported={(updated) => applyUpdate(updated, "Report shared with other companies")}
      />
    </article>
  );
}
