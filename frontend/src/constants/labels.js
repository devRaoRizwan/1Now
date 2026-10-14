export const STATUS_LABELS = {
  pending: "Pending",
  info_requested: "Info requested",
  approved: "Approved",
  declined: "Declined",
  completed: "Completed",
};

export const STATUS_TONES = {
  pending: "accent",
  info_requested: "medium",
  approved: "low",
  declined: "high",
  completed: "neutral",
};

export const OPEN_STATUSES = new Set(["pending", "info_requested"]);

export const LEVEL_LABELS = { low: "Low risk", medium: "Medium risk", high: "High risk" };

export const MATCH_LABELS = { license: "Licence", email: "Email", phone: "Phone" };

export const SOURCE_LABELS = { network: "Other companies", booking: "This booking" };

export const SEVERITY_LEVELS = ["low", "medium", "high"];

export const INCIDENT_OPTIONS = [
  { value: "damage", label: "Vehicle damage" },
  { value: "no_show", label: "No-show" },
  { value: "chargeback", label: "Payment chargeback" },
  { value: "theft", label: "Theft / unreturned vehicle" },
  { value: "fake_id", label: "Fake or stolen ID" },
  { value: "smoking", label: "Smoking / excessive cleaning" },
  { value: "late_return", label: "Late return" },
];

export const RISK_FILTERS = [
  { value: "all", label: "All" },
  { value: "high", label: "High" },
  { value: "medium", label: "Medium" },
  { value: "low", label: "Low" },
];
