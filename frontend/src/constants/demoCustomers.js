import { isoDaysFromNow, isoYearsAgo } from "../utils/format.js";

// Ready-made customers so the demo needs no typing. Bilal and Ayesha use slightly
// different email/phone formats than in their earlier bookings, to show the network
// still recognises them.
export const DEMO_CUSTOMERS = [
  {
    id: "ayesha",
    label: "Ayesha Siddiqui",
    description: "Rented from Karachi Drive before",
    tripDays: [3, 6],
    renter: {
      renter_name: "Ayesha Siddiqui",
      renter_email: "Ayesha.Siddiqui@yahoo.com",
      renter_phone: "+92 321 5550182",
      license_state: "SD",
      license_number: "KHI 21 55219",
      license_expiry: isoDaysFromNow(1200),
      date_of_birth: isoYearsAgo(31),
    },
  },
  {
    id: "bilal",
    label: "Bilal Ahmed",
    description: "Reported by 2 companies, now using a new email",
    tripDays: [2, 5],
    renter: {
      renter_name: "Bilal Ahmed",
      renter_email: "b.i.l.a.l.ahmed+weekend@gmail.com",
      renter_phone: "0300 123 4567",
      license_state: "SD",
      license_number: "KHI-19-88123",
      license_expiry: isoDaysFromNow(900),
      date_of_birth: isoYearsAgo(29),
    },
  },
  {
    id: "maryam",
    label: "Maryam Iqbal",
    description: "Good customer, no history of problems",
    tripDays: [10, 14],
    renter: {
      renter_name: "Maryam Iqbal",
      renter_email: "maryam.iqbal@gmail.com",
      renter_phone: "0302-5550134",
      license_state: "PB",
      license_number: "LHR-16-77881",
      license_expiry: isoDaysFromNow(1400),
      date_of_birth: isoYearsAgo(36),
    },
  },
  {
    id: "ali",
    label: "Ali Raza",
    description: "Age 19, throwaway email, books last-minute",
    tripDays: [1, 3],
    renter: {
      renter_name: "Ali Raza",
      renter_email: "ali.r@mailinator.com",
      renter_phone: "0315-5550101",
      license_state: "PB",
      license_number: "LHR-25-22001",
      license_expiry: isoDaysFromNow(500),
      date_of_birth: isoYearsAgo(19),
    },
  },
];
