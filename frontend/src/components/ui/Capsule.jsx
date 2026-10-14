import { LEVEL_LABELS, STATUS_LABELS, STATUS_TONES } from "../../constants/labels.js";
import { capitalize } from "../../utils/format.js";

export function Capsule({ tone = "neutral", dot = false, children }) {
  return (
    <span className={`capsule ${tone}`}>
      {dot && <span className="capsule-dot" />}
      {children}
    </span>
  );
}

export function RiskCapsule({ level, score }) {
  return (
    <Capsule tone={level} dot>
      {LEVEL_LABELS[level]}
      <span className="capsule-score">{score}</span>
    </Capsule>
  );
}

export function StatusCapsule({ status }) {
  return <Capsule tone={STATUS_TONES[status]}>{STATUS_LABELS[status]}</Capsule>;
}

export function SeverityCapsule({ severity }) {
  return (
    <Capsule tone={severity} dot>
      {capitalize(severity)}
    </Capsule>
  );
}
