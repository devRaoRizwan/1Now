import { useCallback, useState } from "react";
import { api } from "./api/client.js";
import NewBookingDialog from "./components/bookings/NewBookingDialog.jsx";
import PageHeader from "./components/layout/PageHeader.jsx";
import Sidebar from "./components/layout/Sidebar.jsx";
import Icon from "./components/ui/Icon.jsx";
import Toast from "./components/ui/Toast.jsx";
import { OPEN_STATUSES } from "./constants/labels.js";
import { PAGES } from "./constants/navigation.js";
import { useDocumentTitle } from "./hooks/useDocumentTitle.js";
import { useFetch } from "./hooks/useFetch.js";
import { useToast } from "./hooks/useToast.js";
import BookingsPage from "./pages/BookingsPage.jsx";
import ReportsPage from "./pages/ReportsPage.jsx";

export default function App() {
  const [hostId, setHostId] = useState(1);
  const [page, setPage] = useState("bookings");
  const [selectedId, setSelectedId] = useState(null);
  const [dialogOpen, setDialogOpen] = useState(false);
  // Bumped after every change so all views refetch fresh risk scores.
  const [version, setVersion] = useState(0);
  const { message, notify } = useToast();

  const refresh = useCallback(() => setVersion((value) => value + 1), []);
  const closeDialog = useCallback(() => setDialogOpen(false), []);

  const { data: hosts } = useFetch(api.hosts, []);
  const { data: bookings } = useFetch(() => api.bookings(hostId), [hostId, version]);
  const { data: reports } = useFetch(() => api.reports(hostId), [hostId, version]);

  const host = hosts?.find((item) => item.id === hostId);
  const current = PAGES[page];
  useDocumentTitle(current.title);

  if (!host || !bookings || !reports) return null;

  const counts = {
    bookings: bookings.filter((booking) => OPEN_STATUSES.has(booking.status)).length,
    reports: reports.length,
  };

  function switchHost(id) {
    setHostId(Number(id));
    setSelectedId(null);
  }

  function navigate(key) {
    setPage(key);
    window.scrollTo({ top: 0, behavior: "smooth" });
  }

  function handleCreated(booking) {
    closeDialog();
    setPage("bookings");
    setSelectedId(booking.id);
    refresh();
    notify(`New booking from ${booking.renter_name}: ${booking.risk.level} risk`);
  }

  return (
    <div className="shell">
      <Sidebar hosts={hosts} hostId={hostId} page={page} counts={counts} onNavigate={navigate} onSwitchHost={switchHost} />

      <div className="workspace">
        <PageHeader
          title={current.title}
          subtitle={current.subtitle(host)}
          action={
            <button className="btn primary" onClick={() => setDialogOpen(true)}>
              <Icon name="plus" size={16} />
              New booking (demo)
            </button>
          }
        />

        <main className="page-body">
          {page === "bookings" ? (
            <BookingsPage
              bookings={bookings}
              hostId={hostId}
              selectedId={selectedId}
              onSelect={setSelectedId}
              version={version}
              onChanged={refresh}
              notify={notify}
            />
          ) : (
            <ReportsPage reports={reports} hostId={hostId} onChanged={refresh} notify={notify} />
          )}
        </main>
      </div>

      {dialogOpen && <NewBookingDialog hostId={hostId} hostName={host.name} onClose={closeDialog} onCreated={handleCreated} />}
      <Toast message={message} />
    </div>
  );
}
