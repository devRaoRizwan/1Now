from conftest import days_from_today

RAO, KARACHI, ISLAMABAD = 1, 2, 3


def bookings_by_name(client, host_id: int) -> dict:
    return {booking["renter_name"]: booking for booking in client.get(f"/api/hosts/{host_id}/bookings").json()}


def create_booking(client, host_id: int, vehicle_id: int, **renter):
    body = {
        "host_id": host_id,
        "vehicle_id": vehicle_id,
        "renter_name": "Test Customer",
        "renter_email": "test@example.com",
        "renter_phone": "0300-0000000",
        "license_state": "PB",
        "license_number": "LHR-00-00001",
        "license_expiry": days_from_today(900),
        "date_of_birth": "1990-05-05",
        "start_date": days_from_today(5),
        "end_date": days_from_today(8),
        **renter,
    }
    return client.post("/api/bookings", json=body)


def test_bilal_is_matched_across_companies_despite_different_formats(client):
    bilal = bookings_by_name(client, RAO)["Bilal Ahmed"]
    assert bilal["risk_level"] == "high"

    detail = client.get(f"/api/bookings/{bilal['id']}?host_id={RAO}").json()
    assert len(detail["network_matches"]) == 2
    assert not any(match["reported_by_you"] for match in detail["network_matches"])
    assert "private_note" not in str(detail["network_matches"])


def test_clean_customer_is_low_risk(client):
    assert bookings_by_name(client, RAO)["Fatima Noor"]["risk_level"] == "low"


def test_expired_reports_do_not_count(client):
    assert bookings_by_name(client, ISLAMABAD)["Imran Qureshi"]["risk_score"] == 0


def test_company_cannot_read_another_companys_booking(client):
    bilal = bookings_by_name(client, RAO)["Bilal Ahmed"]
    assert client.get(f"/api/bookings/{bilal['id']}?host_id={KARACHI}").status_code == 403


def test_report_then_flag_then_withdraw(client):
    ayesha = bookings_by_name(client, KARACHI)["Ayesha Siddiqui"]
    response = client.post(f"/api/bookings/{ayesha['id']}/report", json={
        "host_id": KARACHI, "incident_type": "chargeback", "severity": "high",
        "incident_date": days_from_today(-2), "private_note": "Secret note",
    })
    assert response.status_code == 201

    response = create_booking(
        client, RAO, 2, renter_name="Ayesha Siddiqui", renter_email="AYESHA.SIDDIQUI@yahoo.com",
        renter_phone="+92 321 5550182", license_state="SD", license_number="KHI 21 55219",
    )
    assert response.status_code == 201
    new_booking = response.json()
    assert new_booking["risk"]["level"] == "high"
    assert "Secret note" not in str(new_booking)

    report_id = next(
        report["id"] for report in client.get(f"/api/hosts/{KARACHI}/reports").json()
        if report["renter_name"] == "Ayesha Siddiqui"
    )
    assert client.delete(f"/api/reports/{report_id}?host_id={RAO}").status_code == 403
    assert client.delete(f"/api/reports/{report_id}?host_id={KARACHI}").status_code == 200

    after = client.get(f"/api/bookings/{new_booking['id']}?host_id={RAO}").json()
    assert after["risk"]["level"] == "low"
    assert after["network_matches"] == []


def test_a_decision_can_only_be_made_once(client):
    fatima = bookings_by_name(client, RAO)["Fatima Noor"]
    approved = client.post(f"/api/bookings/{fatima['id']}/decision", json={"host_id": RAO, "decision": "approved"})
    assert approved.json()["status"] == "approved"
    again = client.post(f"/api/bookings/{fatima['id']}/decision", json={"host_id": RAO, "decision": "declined"})
    assert again.status_code == 409


def test_cannot_book_another_companys_car(client):
    assert create_booking(client, RAO, 5).status_code == 400


def test_return_date_must_be_after_pick_up(client):
    response = create_booking(client, RAO, 2, start_date=days_from_today(5), end_date=days_from_today(3))
    assert response.status_code == 422
