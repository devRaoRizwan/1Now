from datetime import date
from typing import Literal

from pydantic import BaseModel, Field, model_validator

IncidentType = Literal["damage", "no_show", "chargeback", "theft", "fake_id", "smoking", "late_return"]
Severity = Literal["low", "medium", "high"]
Decision = Literal["approved", "declined", "info_requested"]


class BookingCreate(BaseModel):
    host_id: int
    vehicle_id: int
    renter_name: str = Field(min_length=1, max_length=100)
    renter_email: str = Field(pattern=r"^[^@\s]+@[^@\s]+\.[^@\s]+$", max_length=200)
    renter_phone: str = Field(min_length=7, max_length=30)
    license_state: str = Field(pattern=r"^[A-Za-z]{2}$")
    license_number: str = Field(min_length=3, max_length=30)
    license_expiry: date
    date_of_birth: date
    start_date: date
    end_date: date

    @model_validator(mode="after")
    def check_dates(self):
        if self.end_date <= self.start_date:
            raise ValueError("end_date must be after start_date")
        if self.date_of_birth >= self.start_date:
            raise ValueError("date_of_birth must be before the trip")
        return self

    def renter(self) -> dict:
        return {
            "name": self.renter_name.strip(),
            "email": self.renter_email.strip(),
            "phone": self.renter_phone.strip(),
            "license_state": self.license_state,
            "license_number": self.license_number.strip(),
            "license_expiry": self.license_expiry.isoformat(),
            "date_of_birth": self.date_of_birth.isoformat(),
        }


class DecisionUpdate(BaseModel):
    host_id: int
    decision: Decision


class ReportCreate(BaseModel):
    host_id: int
    incident_type: IncidentType
    severity: Severity
    incident_date: date
    private_note: str = Field(default="", max_length=1000)
