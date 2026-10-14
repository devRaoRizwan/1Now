import { useState } from "react";
import { api } from "../../api/client.js";
import { DEMO_CUSTOMERS } from "../../constants/demoCustomers.js";
import { useFetch } from "../../hooks/useFetch.js";
import { formatRupees, isoDaysFromNow } from "../../utils/format.js";
import { SelectField, TextField } from "../ui/Field.jsx";
import Modal from "../ui/Modal.jsx";

const EMPTY_RENTER = {
  renter_name: "",
  renter_email: "",
  renter_phone: "",
  license_state: "",
  license_number: "",
  license_expiry: "",
  date_of_birth: "",
};

const CUSTOMER_OPTIONS = DEMO_CUSTOMERS.map(({ id, label, description }) => ({ value: id, label, description }));

const TEXT_FIELDS = [
  { name: "renter_name", label: "Full name" },
  { name: "renter_email", label: "Email", type: "email" },
  { name: "renter_phone", label: "Phone" },
  { name: "date_of_birth", label: "Date of birth", type: "date" },
];

const LICENSE_FIELDS = [
  { name: "license_state", label: "Province", maxLength: 2, placeholder: "PB" },
  { name: "license_number", label: "Licence number" },
  { name: "license_expiry", label: "Licence expiry", type: "date" },
];

const TRIP_FIELDS = [
  { name: "start_date", label: "Pick-up", type: "date" },
  { name: "end_date", label: "Return", type: "date" },
];

export default function NewBookingDialog({ hostId, hostName, onClose, onCreated }) {
  const [form, setForm] = useState({ ...EMPTY_RENTER, vehicle_id: "", start_date: isoDaysFromNow(3), end_date: isoDaysFromNow(6) });
  const [customerId, setCustomerId] = useState("");
  const [error, setError] = useState(null);
  const [saving, setSaving] = useState(false);

  const { data: vehicles } = useFetch(
    () =>
      api.vehicles(hostId).then((list) => {
        setForm((current) => ({ ...current, vehicle_id: list[0]?.id ?? "" }));
        return list;
      }),
    [hostId],
  );

  const setField = (name, value) => setForm((current) => ({ ...current, [name]: value }));

  function fillDemoCustomer(id) {
    const customer = DEMO_CUSTOMERS.find((item) => item.id === id);
    const [startIn, endIn] = customer.tripDays;
    setCustomerId(id);
    setForm((current) => ({
      ...current,
      ...customer.renter,
      start_date: isoDaysFromNow(startIn),
      end_date: isoDaysFromNow(endIn),
    }));
  }

  async function submit(event) {
    event.preventDefault();
    setError(null);
    setSaving(true);
    try {
      onCreated(await api.createBooking({ ...form, host_id: hostId, vehicle_id: Number(form.vehicle_id) }));
    } catch (err) {
      setError(err.message);
    } finally {
      setSaving(false);
    }
  }

  const renderField = ({ name, ...props }) => (
    <TextField key={name} required value={form[name]} onChange={(event) => setField(name, event.target.value)} {...props} />
  );

  return (
    <Modal title="A customer books a car" subtitle={`Pretend you are a customer booking a car on ${hostName}'s website.`} onClose={onClose}>
      <form onSubmit={submit}>
        <div className="demo-fill">
          <SelectField
            label="Quick fill with a demo customer"
            placeholder="Choose a demo customer…"
            value={customerId}
            options={CUSTOMER_OPTIONS}
            onChange={fillDemoCustomer}
          />
        </div>

        <div className="form-grid">
          <SelectField
            label="Car"
            wide
            value={form.vehicle_id}
            options={(vehicles ?? []).map((vehicle) => ({
              value: vehicle.id,
              label: vehicle.name,
              description: `${formatRupees(vehicle.daily_rate)} per day`,
            }))}
            onChange={(id) => setField("vehicle_id", id)}
          />
          {TEXT_FIELDS.map(renderField)}
          <div className="form-row-3">{LICENSE_FIELDS.map(renderField)}</div>
          {TRIP_FIELDS.map(renderField)}
        </div>

        {error && <p className="error">{error}</p>}
        <div className="actions modal-actions">
          <button type="button" className="btn" onClick={onClose}>
            Cancel
          </button>
          <button type="submit" className="btn primary" disabled={saving}>
            {saving ? "Checking…" : "Submit booking"}
          </button>
        </div>
      </form>
    </Modal>
  );
}
