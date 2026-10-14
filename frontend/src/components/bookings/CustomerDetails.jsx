import { formatDate } from "../../utils/format.js";
import { Capsule } from "../ui/Capsule.jsx";
import Section from "../ui/Section.jsx";

export default function CustomerDetails({ booking }) {
  const items = [
    ["Email", booking.renter_email],
    ["Phone", booking.renter_phone],
    ["Date of birth", formatDate(booking.date_of_birth)],
    ["Licence", `${booking.license_state} ${booking.license_number}`],
    ["Licence expiry", formatDate(booking.license_expiry)],
  ];

  return (
    <Section title="Customer details" aside={<Capsule>Only visible to you</Capsule>}>
      <dl className="details">
        {items.map(([term, value]) => (
          <div key={term}>
            <dt>{term}</dt>
            <dd>{value}</dd>
          </div>
        ))}
      </dl>
    </Section>
  );
}
