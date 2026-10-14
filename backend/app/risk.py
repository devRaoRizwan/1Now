from datetime import date

# Every point in a score comes with a plain-English reason, so a host can always
# explain a decision. Pure functions only: easy to read and test.

MEDIUM_RISK_THRESHOLD = 30
HIGH_RISK_THRESHOLD = 60
MAX_SCORE = 100

LICENSE_MATCH_POINTS = 60
CONTACT_MATCH_POINTS = 35
EXTRA_REPORTER_POINTS = 10
MAX_EXTRA_REPORTER_POINTS = 20
SEVERE_INCIDENT_POINTS = 10

LICENSE_EXPIRED_POINTS = 50
LICENSE_EXPIRES_DURING_TRIP_POINTS = 30
UNDER_21_POINTS = 25
UNDER_25_POINTS = 10
LAST_MINUTE_HIGH_VALUE_POINTS = 15
LONG_TRIP_POINTS = 10
DISPOSABLE_EMAIL_POINTS = 15

HIGH_VALUE_VEHICLE_PKR = 10_000_000
LAST_MINUTE_DAYS = 1
LONG_TRIP_DAYS = 21

INCIDENT_LABELS = {
    "damage": "Vehicle damage",
    "no_show": "No-show",
    "chargeback": "Payment chargeback",
    "theft": "Theft / unreturned vehicle",
    "fake_id": "Fake or stolen ID",
    "smoking": "Smoking / excessive cleaning",
    "late_return": "Late return",
}

SEVERE_INCIDENTS = {"theft", "fake_id", "chargeback"}

DISPOSABLE_EMAIL_DOMAINS = {
    "mailinator.com",
    "guerrillamail.com",
    "10minutemail.com",
    "tempmail.com",
    "yopmail.com",
    "trashmail.com",
}

RECOMMENDATIONS = {
    "low": "Looks fine to approve",
    "medium": "Request more info (ID selfie, proof of insurance) before approving",
    "high": "Decline, or verify ID in person before handing over keys",
}


def count_label(count: int, singular: str, plural: str) -> str:
    return f"{count} {singular if count == 1 else plural}"


def age_on(birth: date, day: date) -> int:
    return day.year - birth.year - ((day.month, day.day) < (birth.month, birth.day))


def build_reason(code: str, label: str, detail: str, points: int, source: str) -> dict:
    return {"code": code, "label": label, "detail": detail, "points": points, "source": source}


def describe_reporters(reporter_ids: set, viewer_host_id: int) -> str:
    others = reporter_ids - {viewer_host_id}
    others_text = count_label(len(others), "other company", "other companies")
    if not others:
        return "you"
    if viewer_host_id in reporter_ids:
        return f"you and {others_text}"
    return others_text


def network_reasons(matches: list[dict], viewer_host_id: int) -> list[dict]:
    if not matches:
        return []

    reporter_ids = {match["reporter_host_id"] for match in matches}
    incident_types = sorted({match["incident_type"] for match in matches})
    summary = (
        f"{count_label(len(matches), 'report', 'reports')} from {describe_reporters(reporter_ids, viewer_host_id)}: "
        + ", ".join(INCIDENT_LABELS[incident] for incident in incident_types)
        + "."
    )

    # A licence match is strong evidence of the same person. Phones and emails get
    # shared or recycled, so a contact-only match asks for verification instead.
    if any("license" in match["matched_on"] for match in matches):
        reasons = [build_reason(
            "network_license_match", "Driver's licence was reported in the network",
            summary, LICENSE_MATCH_POINTS, "network",
        )]
    else:
        reasons = [build_reason(
            "network_contact_match", "Email or phone matches a reported customer",
            f"Licence is different, so this may be a shared contact. {summary} Verify ID before approving.",
            CONTACT_MATCH_POINTS, "network",
        )]

    if len(reporter_ids) > 1:
        reasons.append(build_reason(
            "network_multiple_hosts", "Reported by more than one company",
            f"{len(reporter_ids)} different companies reported this customer.",
            min(EXTRA_REPORTER_POINTS * (len(reporter_ids) - 1), MAX_EXTRA_REPORTER_POINTS), "network",
        ))

    severe = sorted(set(incident_types) & SEVERE_INCIDENTS)
    if severe:
        reasons.append(build_reason(
            "network_severe_incident", "Includes a severe incident",
            ", ".join(INCIDENT_LABELS[incident] for incident in severe) + ".",
            SEVERE_INCIDENT_POINTS, "network",
        ))
    return reasons


def booking_reasons(booking: dict, vehicle: dict) -> list[dict]:
    start = date.fromisoformat(booking["start_date"])
    end = date.fromisoformat(booking["end_date"])
    booked_on = date.fromisoformat(booking["booked_on"])
    license_expiry = date.fromisoformat(booking["license_expiry"])
    age = age_on(date.fromisoformat(booking["date_of_birth"]), start)
    lead_days = (start - booked_on).days
    trip_days = (end - start).days
    email_domain = booking["renter_email"].rsplit("@", 1)[-1].lower()

    reasons = []

    if license_expiry < start:
        reasons.append(build_reason(
            "license_expired", "Driver's licence is expired",
            f"Expired on {license_expiry.isoformat()}.", LICENSE_EXPIRED_POINTS, "booking",
        ))
    elif license_expiry < end:
        reasons.append(build_reason(
            "license_expires_during_trip", "Licence expires during the trip",
            f"Expires {license_expiry.isoformat()}, trip ends {end.isoformat()}.",
            LICENSE_EXPIRES_DURING_TRIP_POINTS, "booking",
        ))

    if age < 21:
        reasons.append(build_reason(
            "very_young_driver", "Driver is under 21",
            f"Age {age} at pick-up. Most insurers exclude under-21s.", UNDER_21_POINTS, "booking",
        ))
    elif age < 25:
        reasons.append(build_reason(
            "young_driver", "Driver is under 25",
            f"Age {age} at pick-up. Higher accident risk; check your insurance covers it.", UNDER_25_POINTS, "booking",
        ))

    if lead_days <= LAST_MINUTE_DAYS and vehicle["value_pkr"] >= HIGH_VALUE_VEHICLE_PKR:
        reasons.append(build_reason(
            "last_minute_high_value", "Last-minute booking of a high-value car",
            f"Booked {count_label(lead_days, 'day', 'days')} before pick-up for a Rs {vehicle['value_pkr']:,} vehicle, "
            "a common pattern in rental fraud.",
            LAST_MINUTE_HIGH_VALUE_POINTS, "booking",
        ))

    if trip_days > LONG_TRIP_DAYS:
        reasons.append(build_reason(
            "long_trip", "Unusually long trip",
            f"{trip_days} days. Long trips are harder to recover if something goes wrong.", LONG_TRIP_POINTS, "booking",
        ))

    if email_domain in DISPOSABLE_EMAIL_DOMAINS:
        reasons.append(build_reason(
            "disposable_email", "Disposable email address",
            f"{email_domain} is a throwaway inbox service.", DISPOSABLE_EMAIL_POINTS, "booking",
        ))

    return reasons


def risk_level(score: int) -> str:
    if score >= HIGH_RISK_THRESHOLD:
        return "high"
    if score >= MEDIUM_RISK_THRESHOLD:
        return "medium"
    return "low"


def assess(booking: dict, vehicle: dict, matches: list[dict], viewer_host_id: int) -> dict:
    reasons = network_reasons(matches, viewer_host_id) + booking_reasons(booking, vehicle)
    score = min(sum(reason["points"] for reason in reasons), MAX_SCORE)
    level = risk_level(score)
    return {"score": score, "level": level, "recommendation": RECOMMENDATIONS[level], "reasons": reasons}
