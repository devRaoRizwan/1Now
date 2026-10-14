from datetime import date, timedelta

from app import repository

# Demo data. All dates are relative to today so the demo never goes stale.

HOSTS = [
    {"id": 1, "name": "Rao Rent-a-Car", "owner_name": "Rao Rizwan", "city": "Lahore", "logo": "rao-rent-a-car.svg"},
    {"id": 2, "name": "Karachi Drive", "owner_name": "Ahmed Khan", "city": "Karachi", "logo": "karachi-drive.svg"},
    {"id": 3, "name": "Islamabad Wheels", "owner_name": "Sana Malik", "city": "Islamabad", "logo": "islamabad-wheels.svg"},
]

VEHICLES = [
    {"id": 1, "host_id": 1, "name": "Toyota Fortuner (2024)", "daily_rate": 18_000, "value_pkr": 16_000_000},
    {"id": 2, "host_id": 1, "name": "Suzuki Cultus (2022)", "daily_rate": 6_000, "value_pkr": 3_500_000},
    {"id": 3, "host_id": 1, "name": "Toyota Land Cruiser (2023)", "daily_rate": 35_000, "value_pkr": 45_000_000},
    {"id": 4, "host_id": 2, "name": "Honda City (2023)", "daily_rate": 7_000, "value_pkr": 4_500_000},
    {"id": 5, "host_id": 2, "name": "Honda Civic (2024)", "daily_rate": 12_000, "value_pkr": 9_000_000},
    {"id": 6, "host_id": 3, "name": "Toyota Hilux (2023)", "daily_rate": 15_000, "value_pkr": 14_000_000},
    {"id": 7, "host_id": 3, "name": "Kia Sportage (2022)", "daily_rate": 11_000, "value_pkr": 8_500_000},
]


def days_from_today(days: int) -> str:
    return (date.today() + timedelta(days=days)).isoformat()


def years_ago(years: int) -> str:
    today = date.today()
    return today.replace(year=today.year - years, day=min(today.day, 28)).isoformat()


def renter(name, email, phone, province, license_number, license_valid_days, age) -> dict:
    return {
        "name": name,
        "email": email,
        "phone": phone,
        "license_state": province,
        "license_number": license_number,
        "license_expiry": days_from_today(license_valid_days),
        "date_of_birth": years_ago(age),
    }


def demo_bookings() -> list[dict]:
    # Bilal uses a slightly different email/phone format with each company,
    # to show the network still recognises him.
    def bilal(email, phone, province, number):
        return renter("Bilal Ahmed", email, phone, province, number, 900, 29)

    return [
        {"key": "bilal_karachi", "host_id": 2, "vehicle_id": 5, "status": "completed", "days": (-160, -155, -170),
         "renter": bilal("bilal.ahmed@gmail.com", "0300-1234567", "SD", "KHI-19-88123")},
        {"key": "bilal_islamabad", "host_id": 3, "vehicle_id": 6, "status": "completed", "days": (-65, -60, -70),
         "renter": bilal("BilalAhmed+rides@gmail.com", "+92 300 1234567", "sd", "khi 1988123")},
        {"key": "imran_islamabad", "host_id": 3, "vehicle_id": 7, "status": "completed", "days": (-910, -905, -915),
         "renter": renter("Imran Qureshi", "imran.qureshi@outlook.com", "0333-5550110", "IS", "ISB-12-41188", 600, 41)},
        {"key": "ayesha_karachi", "host_id": 2, "vehicle_id": 4, "status": "completed", "days": (-8, -4, -12),
         "renter": renter("Ayesha Siddiqui", "ayesha.siddiqui@yahoo.com", "0321-5550182", "SD", "KHI-21-55219", 1200, 31)},
        {"key": "bilal_lahore", "host_id": 1, "vehicle_id": 3, "status": "pending", "days": (1, 4, 0),
         "renter": bilal("Bilal.Ahmed+lahore@gmail.com", "92-300-123-4567", "SD", "KHI-19-88123")},
        {"key": "fatima", "host_id": 1, "vehicle_id": 2, "status": "pending", "days": (14, 18, -3),
         "renter": renter("Fatima Noor", "fatima.noor@gmail.com", "0301-5550123", "PB", "LHR-18-12345", 1500, 34)},
        {"key": "hamza", "host_id": 1, "vehicle_id": 1, "status": "pending", "days": (1, 3, 0),
         "renter": renter("Hamza Ali", "hamza.ali2006@gmail.com", "0345-5550166", "PB", "LHR-24-62011", 1000, 20)},
        {"key": "usman", "host_id": 1, "vehicle_id": 2, "status": "pending", "days": (5, 30, -1),
         "renter": renter("Usman Tariq", "usman.tariq@hotmail.com", "0312-5550177", "KP", "PSH-10-55123", 10, 45)},
        {"key": "zain", "host_id": 1, "vehicle_id": 1, "status": "pending", "days": (6, 9, -2),
         "renter": renter("Zain Abbas", "zain.abbas@outlook.com", "0300 1234567", "IS", "ISB-20-29988", 800, 27)},
        {"key": "hira", "host_id": 1, "vehicle_id": 2, "status": "approved", "days": (-2, 2, -9),
         "renter": renter("Hira Javed", "hira.javed@icloud.com", "0322-5550199", "PB", "LHR-15-31415", 1400, 38)},
    ]


DEMO_REPORTS = [
    {"booking": "bilal_karachi", "reporter": 2, "type": "damage", "severity": "high", "day": -155,
     "note": "Front bumper and wheel damaged, customer stopped answering calls."},
    {"booking": "bilal_islamabad", "reporter": 3, "type": "chargeback", "severity": "medium", "day": -50,
     "note": "Disputed the full payment with his bank after returning the Hilux."},
    # Older than the retention window: shows that expired reports stop counting.
    {"booking": "imran_islamabad", "reporter": 3, "type": "damage", "severity": "low", "day": -905,
     "note": "Scratched door."},
]


def seed(connection) -> None:
    for host in HOSTS:
        repository.insert(connection, "hosts", host)
    for vehicle in VEHICLES:
        repository.insert(connection, "vehicles", vehicle)

    booking_ids = {}
    for booking in demo_bookings():
        start, end, booked = booking["days"]
        booking_ids[booking["key"]] = repository.create_booking(
            connection, booking["host_id"], booking["vehicle_id"], booking["renter"],
            days_from_today(start), days_from_today(end), days_from_today(booked), booking["status"],
        )

    for report in DEMO_REPORTS:
        booking = repository.get_booking(connection, booking_ids[report["booking"]])
        repository.create_report(
            connection, booking, report["reporter"], report["type"], report["severity"],
            days_from_today(report["day"]), report["note"], days_from_today(report["day"] + 1),
        )
    connection.commit()


def seed_if_empty(connection) -> None:
    if not repository.list_hosts(connection):
        seed(connection)
