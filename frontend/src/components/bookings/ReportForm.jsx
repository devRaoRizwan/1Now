import { useState } from "react";
import { api } from "../../api/client.js";
import { INCIDENT_OPTIONS, SEVERITY_LEVELS } from "../../constants/labels.js";
import { capitalize, formatDate, isoDaysFromNow } from "../../utils/format.js";
import { SelectField, TextField } from "../ui/Field.jsx";

const SEVERITY_OPTIONS = SEVERITY_LEVELS.map((level) => ({
  value: level,
  label: capitalize(level),
  icon: <span className={`option-dot ${level}`} />,
}));

const emptyReport = () => ({
  incident_type: "damage",
  severity: "medium",
  incident_date: isoDaysFromNow(0),
  private_note: "",
});

export default function ReportForm({ booking, hostId, onReported }) {
  const [open, setOpen] = useState(false);
  const [form, setForm] = useState(emptyReport);
  const [error, setError] = useState(null);

  const update = (field) => (value) => setForm((current) => ({ ...current, [field]: value }));

  async function submit(event) {
    event.preventDefault();
    setError(null);
    try {
      onReported(await api.report(booking.id, { ...form, host_id: hostId }));
      setOpen(false);
      setForm(emptyReport());
    } catch (err) {
      setError(err.message);
    }
  }

  return (
    <div className="report-box">
      <div className="report-head">
        <div>
          <strong>Had a problem with this customer?</strong>
          <p className="muted small">
            Warn other rental companies. They see what happened and when, but never your company name, your notes or the
            customer's details.
          </p>
        </div>
        {!open && (
          <button className="btn outline-accent" onClick={() => setOpen(true)}>
            Report customer
          </button>
        )}
      </div>

      {booking.my_reports.length > 0 && (
        <ul className="own-reports">
          {booking.my_reports.map((report) => (
            <li key={report.id}>
              You reported <strong>{report.incident}</strong> ({report.severity}) on {formatDate(report.incident_date)}
            </li>
          ))}
        </ul>
      )}

      {open && (
        <form className="report-form" onSubmit={submit}>
          <SelectField label="Incident" value={form.incident_type} options={INCIDENT_OPTIONS} onChange={update("incident_type")} />
          <SelectField label="Severity" value={form.severity} options={SEVERITY_OPTIONS} onChange={update("severity")} />
          <TextField
            label="Date"
            type="date"
            required
            max={isoDaysFromNow(0)}
            value={form.incident_date}
            onChange={(event) => update("incident_date")(event.target.value)}
          />
          <TextField
            label="Private note (only you see this)"
            wide
            rows={2}
            placeholder="What happened?"
            value={form.private_note}
            onChange={(event) => update("private_note")(event.target.value)}
          />
          {error && <p className="error wide">{error}</p>}
          <div className="actions wide">
            <button type="button" className="btn" onClick={() => setOpen(false)}>
              Cancel
            </button>
            <button type="submit" className="btn primary">
              Warn other companies
            </button>
          </div>
        </form>
      )}
    </div>
  );
}
