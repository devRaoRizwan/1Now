async function request(path, options = {}) {
  const response = await fetch(path, {
    headers: { "Content-Type": "application/json" },
    ...options,
  });
  const body = await response.json().catch(() => ({}));

  if (!response.ok) {
    // FastAPI returns a string for our own errors and a list for validation errors.
    const detail = Array.isArray(body.detail)
      ? body.detail.map((item) => item.msg.replace(/^Value error, /, "")).join("; ")
      : body.detail;
    throw new Error(detail || `Request failed (${response.status})`);
  }
  return body;
}

const post = (path, data) => request(path, { method: "POST", body: JSON.stringify(data) });

export const api = {
  hosts: () => request("/api/hosts"),
  vehicles: (hostId) => request(`/api/hosts/${hostId}/vehicles`),
  bookings: (hostId) => request(`/api/hosts/${hostId}/bookings`),
  reports: (hostId) => request(`/api/hosts/${hostId}/reports`),
  booking: (bookingId, hostId) => request(`/api/bookings/${bookingId}?host_id=${hostId}`),
  createBooking: (data) => post("/api/bookings", data),
  decide: (bookingId, hostId, decision) => post(`/api/bookings/${bookingId}/decision`, { host_id: hostId, decision }),
  report: (bookingId, data) => post(`/api/bookings/${bookingId}/report`, data),
  withdraw: (reportId, hostId) => request(`/api/reports/${reportId}?host_id=${hostId}`, { method: "DELETE" }),
};
