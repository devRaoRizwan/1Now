import { MATCH_LABELS } from "../../constants/labels.js";
import { formatDate } from "../../utils/format.js";
import { Capsule, SeverityCapsule } from "../ui/Capsule.jsx";
import Section from "../ui/Section.jsx";

export default function NetworkReports({ matches }) {
  return (
    <Section title="Reports from other companies">
      {matches.length === 0 ? (
        <p className="muted">No rental company has reported this customer in the last 2 years.</p>
      ) : (
        <table className="table matches-table">
          <thead>
            <tr>
              <th>Incident</th>
              <th>Severity</th>
              <th>Date</th>
              <th className="col-matched">Matched on</th>
              <th>Reported by</th>
            </tr>
          </thead>
          <tbody>
            {matches.map((match, index) => (
              <tr key={index}>
                <td>{match.incident}</td>
                <td><SeverityCapsule severity={match.severity} /></td>
                <td className="nowrap">{formatDate(match.incident_date)}</td>
                <td className="col-matched">
                  <div className="capsule-row tight">
                    {match.matched_on.map((kind) => <Capsule key={kind}>{MATCH_LABELS[kind]}</Capsule>)}
                  </div>
                </td>
                <td className="muted">{match.reported_by_you ? "You" : "Hidden"}</td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
    </Section>
  );
}
