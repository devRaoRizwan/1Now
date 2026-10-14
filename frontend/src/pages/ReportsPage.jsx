import { api } from "../api/client.js";
import ReportsTable from "../components/reports/ReportsTable.jsx";

export default function ReportsPage({ reports, hostId, onChanged, notify }) {
  async function withdraw(report) {
    if (!window.confirm(`Withdraw your ${report.incident.toLowerCase()} report on ${report.renter_name}?`)) return;
    try {
      await api.withdraw(report.id, hostId);
      onChanged();
      notify("Report withdrawn. Other companies no longer see it");
    } catch (err) {
      notify(err.message);
    }
  }

  return (
    <div className="card reports-card">
      <p className="muted note">
        Other companies only see what happened and when, never your company name or notes. Reports stop counting after
        2 years, and you can withdraw one at any time.
      </p>
      {reports.length === 0 ? (
        <p className="empty muted">You haven't reported anyone.</p>
      ) : (
        <ReportsTable reports={reports} onWithdraw={withdraw} />
      )}
    </div>
  );
}
