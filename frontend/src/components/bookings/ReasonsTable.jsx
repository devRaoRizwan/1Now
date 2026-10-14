import { SOURCE_LABELS } from "../../constants/labels.js";
import { Capsule } from "../ui/Capsule.jsx";
import Section from "../ui/Section.jsx";

export default function ReasonsTable({ risk }) {
  return (
    <Section title="Why this score">
      {risk.reasons.length === 0 ? (
        <p className="muted">No warning signs. Valid licence, and no company has reported this customer.</p>
      ) : (
        <table className="table reasons-table">
          <tbody>
            {risk.reasons.map((reason) => (
              <tr key={reason.code}>
                <td className="col-points">+{reason.points}</td>
                <td>
                  <div className="reason-label">{reason.label}</div>
                  <div className="reason-detail">{reason.detail}</div>
                </td>
                <td className="col-source">
                  <Capsule tone={reason.source === "network" ? "ink" : "neutral"}>{SOURCE_LABELS[reason.source]}</Capsule>
                </td>
              </tr>
            ))}
          </tbody>
          <tfoot>
            <tr>
              <td className="col-points">{risk.score}</td>
              <td colSpan={2}>Total risk score (max 100)</td>
            </tr>
          </tfoot>
        </table>
      )}
    </Section>
  );
}
