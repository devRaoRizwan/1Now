import { APP_NAME, PAGES } from "../../constants/navigation.js";
import CompanyLogo from "../ui/CompanyLogo.jsx";
import Dropdown from "../ui/Dropdown.jsx";
import Icon from "../ui/Icon.jsx";

export default function Sidebar({ hosts, hostId, page, counts, onNavigate, onSwitchHost }) {
  const companyOptions = hosts.map((host) => ({
    value: host.id,
    label: host.name,
    description: `${host.owner_name} · ${host.city}`,
    icon: <CompanyLogo host={host} size={32} />,
  }));

  return (
    <aside className="sidebar">
      <a className="sidebar-brand" href="https://1now.ai" target="_blank" rel="noreferrer">
        <img src="/logos/1now.svg" alt="1Now" className="brand-logo" />
        <span className="brand-product">{APP_NAME}</span>
      </a>

      <nav className="sidebar-nav" aria-label="Main">
        {Object.entries(PAGES).map(([key, item]) => (
          <button
            key={key}
            className={`nav-item ${page === key ? "active" : ""}`}
            aria-current={page === key ? "page" : undefined}
            onClick={() => onNavigate(key)}
          >
            <Icon name={key} />
            <span className="nav-label">{item.title}</span>
            {counts[key] > 0 && <span className="nav-count">{counts[key]}</span>}
          </button>
        ))}
      </nav>

      <div className="sidebar-account">
        <span className="sidebar-label">Signed in as</span>
        <Dropdown
          variant="account"
          placement="top"
          ariaLabel="Switch company (demo)"
          value={hostId}
          options={companyOptions}
          onChange={onSwitchHost}
        />
      </div>
    </aside>
  );
}
