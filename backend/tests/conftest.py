from datetime import date, timedelta

import pytest
from fastapi.testclient import TestClient


def days_from_today(days: int) -> str:
    return (date.today() + timedelta(days=days)).isoformat()


def years_ago(years: int) -> str:
    today = date.today()
    return today.replace(year=today.year - years, day=min(today.day, 28)).isoformat()


@pytest.fixture()
def client(tmp_path, monkeypatch):
    monkeypatch.setenv("TRUST_DB_PATH", str(tmp_path / "test.db"))
    from app.main import app

    with TestClient(app) as test_client:
        yield test_client
