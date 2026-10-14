export const APP_NAME = "Renter Trust Network";

export const PAGES = {
  bookings: {
    title: "Customer bookings",
    subtitle: (host) => `Customers who want to rent from ${host.name}. Check the risk before you approve.`,
  },
  reports: {
    title: "My reports",
    subtitle: () => "Customers you have warned other companies about.",
  },
};
