const DECISIONS = [
  { value: "declined", label: "Decline", className: "btn decline" },
  { value: "info_requested", label: "Request info", className: "btn" },
  { value: "approved", label: "Approve", className: "btn approve" },
];

export default function DecisionBar({ risk, canDecide, onDecide }) {
  return (
    <div className={`decision ${risk.level}`}>
      <div>
        <div className="decision-label">Suggested action</div>
        <div className="decision-text">{risk.recommendation}</div>
      </div>
      {canDecide && (
        <div className="decision-buttons">
          {DECISIONS.map((decision) => (
            <button key={decision.value} className={decision.className} onClick={() => onDecide(decision.value)}>
              {decision.label}
            </button>
          ))}
        </div>
      )}
    </div>
  );
}
