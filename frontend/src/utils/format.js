const fullDate = new Intl.DateTimeFormat("en-GB", { day: "numeric", month: "short", year: "numeric" });
const shortDate = new Intl.DateTimeFormat("en-GB", { day: "numeric", month: "short" });

const toDate = (iso) => new Date(`${iso}T00:00:00`);

export const formatDate = (iso) => fullDate.format(toDate(iso));

export const formatRange = (startIso, endIso) => `${shortDate.format(toDate(startIso))} – ${shortDate.format(toDate(endIso))}`;

export const formatRupees = (amount) => `Rs ${amount.toLocaleString("en-PK")}`;

export const capitalize = (text) => text.charAt(0).toUpperCase() + text.slice(1);

// Local calendar date. toISOString() would use UTC and be a day off around midnight in Pakistan.
const toIsoDate = (date) =>
  [date.getFullYear(), String(date.getMonth() + 1).padStart(2, "0"), String(date.getDate()).padStart(2, "0")].join("-");

export function isoDaysFromNow(days) {
  const date = new Date();
  date.setDate(date.getDate() + days);
  return toIsoDate(date);
}

export function isoYearsAgo(years) {
  const date = new Date();
  date.setFullYear(date.getFullYear() - years);
  return toIsoDate(date);
}
