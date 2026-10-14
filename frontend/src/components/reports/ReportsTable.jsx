import { formatDate } from "../../utils/format.js";
import { Capsule, SeverityCapsule } from "../ui/Capsule.jsx";

export default function ReportsTable({ reports, onWithdraw }) {
  return (
    <table className="table">
      <thead>
        <tr>
          <th>Customer</th>
          <th>Incident</th>
          <th>Severity</th>
          <th>Date</th>
          <th>Private note</th>
          <th />
        </tr>
      </thead>
      <tbody>
        {reports.map((report) => (
          <tr key={report.id} className={report.expired ? "expired" : ""}>
            <td className="strong">{report.renter_name}</td>
            <td>{report.incident}</td>
            <td><SeverityCapsule severity={report.severity} /></td>
            <td className="nowrap">
              {formatDate(report.incident_date)} {report.expired && <Capsule>Expired</Capsule>}
            </td>
            <td className="muted">{report.private_note || "–"}</td>
            <td className="col-action">
              <button className="btn small" onClick={() => onWithdraw(report)}>
                Withdraw
              </button>
            </td>
          </tr>
        ))}
      </tbody>
    </table>
  );
}
