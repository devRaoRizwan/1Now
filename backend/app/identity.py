import hashlib
import hmac
import re

from app.config import NETWORK_SECRET

GMAIL_DOMAINS = {"gmail.com", "googlemail.com"}


def normalize_email(email: str) -> str:
    # Gmail ignores dots, and every provider ignores "+tags":
    # "Bilal.Ahmed+lahore@Gmail.com" and "bilalahmed@gmail.com" are the same inbox.
    local, _, domain = email.strip().lower().partition("@")
    local = local.split("+", 1)[0]
    if domain in GMAIL_DOMAINS:
        local = local.replace(".", "")
        domain = "gmail.com"
    return f"{local}@{domain}"


def normalize_phone(phone: str) -> str:
    # International digits with a Pakistan (+92) default:
    # "0300-1234567", "+92 300 1234567" and "0092 300 1234567" are the same number.
    digits = re.sub(r"\D", "", phone)
    if digits.startswith("00"):
        return digits[2:]
    if digits.startswith("0"):
        return "92" + digits[1:]
    if len(digits) == 10 and digits.startswith("3"):
        return "92" + digits
    return digits


def normalize_license(province: str, number: str) -> str:
    # Licence numbers are only unique per issuing province.
    clean_number = re.sub(r"[^A-Z0-9]", "", number.upper())
    return f"{province.strip().upper()}:{clean_number}"


def fingerprint(kind: str, value: str) -> str:
    # Keyed, so the shared table can't be reversed with a list of known phone numbers.
    return hmac.new(NETWORK_SECRET, f"{kind}:{value}".encode(), hashlib.sha256).hexdigest()


def identity_hashes(email: str, phone: str, province: str, license_number: str) -> dict:
    return {
        "email_hash": fingerprint("email", normalize_email(email)),
        "phone_hash": fingerprint("phone", normalize_phone(phone)),
        "license_hash": fingerprint("license", normalize_license(province, license_number)),
    }
