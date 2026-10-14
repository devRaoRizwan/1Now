from app.risk import assess
from conftest import days_from_today, years_ago

CHEAP_CAR = {"value_pkr": 3_500_000}
EXPENSIVE_CAR = {"value_pkr": 45_000_000}


def make_booking(**overrides) -> dict:
    return {
        "renter_email": "clean@gmail.com",
        "start_date": days_from_today(10),
        "end_date": days_from_today(13),
        "booked_on": days_from_today(0),
        "license_expiry": days_from_today(1000),
        "date_of_birth": years_ago(35),
        **overrides,
    }


def reason_codes(result: dict) -> set:
    return {reason["code"] for reason in result["reasons"]}


def report(host_id: int, incident_type: str, *matched_on: str) -> dict:
    return {"reporter_host_id": host_id, "incident_type": incident_type, "matched_on": list(matched_on)}


def test_clean_booking_is_low_risk():
    result = assess(make_booking(), CHEAP_CAR, [], viewer_host_id=1)
    assert result["score"] == 0
    assert result["level"] == "low"


def test_licence_expiring_during_trip_is_medium_risk():
    result = assess(make_booking(license_expiry=days_from_today(11)), CHEAP_CAR, [], 1)
    assert "license_expires_during_trip" in reason_codes(result)
    assert result["level"] == "medium"


def test_young_driver_booking_expensive_car_last_minute():
    booking = make_booking(date_of_birth=years_ago(19), start_date=days_from_today(1), end_date=days_from_today(3))
    result = assess(booking, EXPENSIVE_CAR, [], 1)
    assert {"very_young_driver", "last_minute_high_value"} <= reason_codes(result)
    assert result["score"] == 40


def test_licence_reported_by_two_companies_is_high_risk():
    matches = [report(2, "damage", "license", "email"), report(3, "chargeback", "license")]
    result = assess(make_booking(), CHEAP_CAR, matches, viewer_host_id=1)
    assert result["level"] == "high"
    assert result["score"] == 60 + 10 + 10


def test_contact_only_match_asks_for_verification():
    result = assess(make_booking(), CHEAP_CAR, [report(2, "no_show", "phone")], viewer_host_id=1)
    assert reason_codes(result) == {"network_contact_match"}
    assert result["level"] == "medium"


def test_score_is_capped_at_100():
    matches = [report(host_id, "theft", "license") for host_id in (2, 3, 4, 5)]
    risky = make_booking(license_expiry=days_from_today(-1), date_of_birth=years_ago(19), renter_email="x@mailinator.com")
    assert assess(risky, EXPENSIVE_CAR, matches, 1)["score"] == 100
