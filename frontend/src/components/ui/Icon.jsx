const PATHS = {
  chevron: "M3 4.5 6 7.5 9 4.5",
  check: "M3 7.5 5.8 10 11 4",
  bookings: "M3 5.5h14M3 10h14M3 14.5h9",
  reports: "M5 3h7l3 3v11H5zM12 3v3h3M8 10h4M8 13h4",
  plus: "M10 4v12M4 10h12",
};

const VIEWBOX = { chevron: 12, check: 14 };

export default function Icon({ name, size = 20, className = "" }) {
  const box = VIEWBOX[name] ?? 20;
  return (
    <svg className={`icon ${className}`} width={size} height={size} viewBox={`0 0 ${box} ${box}`} aria-hidden="true">
      <path d={PATHS[name]} fill="none" stroke="currentColor" strokeWidth="1.7" strokeLinecap="round" strokeLinejoin="round" />
    </svg>
  );
}
