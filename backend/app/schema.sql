CREATE TABLE IF NOT EXISTS hosts (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    owner_name TEXT NOT NULL,
    city TEXT NOT NULL,
    logo TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS vehicles (
    id INTEGER PRIMARY KEY,
    host_id INTEGER NOT NULL REFERENCES hosts(id),
    name TEXT NOT NULL,
    daily_rate INTEGER NOT NULL,
    value_pkr INTEGER NOT NULL
);

-- Private to each host: raw customer details are only returned to the owning host.
CREATE TABLE IF NOT EXISTS bookings (
    id INTEGER PRIMARY KEY,
    host_id INTEGER NOT NULL REFERENCES hosts(id),
    vehicle_id INTEGER NOT NULL REFERENCES vehicles(id),
    renter_name TEXT NOT NULL,
    renter_email TEXT NOT NULL,
    renter_phone TEXT NOT NULL,
    license_state TEXT NOT NULL,
    license_number TEXT NOT NULL,
    license_expiry TEXT NOT NULL,
    date_of_birth TEXT NOT NULL,
    start_date TEXT NOT NULL,
    end_date TEXT NOT NULL,
    booked_on TEXT NOT NULL,
    status TEXT NOT NULL DEFAULT 'pending',
    email_hash TEXT NOT NULL,
    phone_hash TEXT NOT NULL,
    license_hash TEXT NOT NULL
);

-- Shared across hosts: fingerprints and incident facts only, never names or contact details.
CREATE TABLE IF NOT EXISTS network_reports (
    id INTEGER PRIMARY KEY,
    reporter_host_id INTEGER NOT NULL REFERENCES hosts(id),
    booking_id INTEGER NOT NULL REFERENCES bookings(id),
    email_hash TEXT NOT NULL,
    phone_hash TEXT NOT NULL,
    license_hash TEXT NOT NULL,
    incident_type TEXT NOT NULL,
    severity TEXT NOT NULL,
    incident_date TEXT NOT NULL,
    private_note TEXT NOT NULL DEFAULT '',
    created_on TEXT NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_reports_license ON network_reports(license_hash);
CREATE INDEX IF NOT EXISTS idx_reports_email ON network_reports(email_hash);
CREATE INDEX IF NOT EXISTS idx_reports_phone ON network_reports(phone_hash);
