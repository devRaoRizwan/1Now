export default function CompanyLogo({ host, size = 36 }) {
  return <img className="company-logo" src={`/logos/${host.logo}`} alt={`${host.name} logo`} width={size} height={size} />;
}
