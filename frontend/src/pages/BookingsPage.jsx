import BookingDetail from "../components/bookings/BookingDetail.jsx";
import BookingList from "../components/bookings/BookingList.jsx";

export default function BookingsPage({ bookings, hostId, selectedId, onSelect, version, onChanged, notify }) {
  return (
    <div className="board">
      <BookingList bookings={bookings} selectedId={selectedId} onSelect={onSelect} />
      <BookingDetail
        key={`${hostId}-${selectedId}`}
        bookingId={selectedId}
        hostId={hostId}
        version={version}
        onChanged={onChanged}
        notify={notify}
      />
    </div>
  );
}
