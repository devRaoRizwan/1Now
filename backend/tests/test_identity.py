from app.identity import identity_hashes, normalize_email, normalize_license, normalize_phone


def test_gmail_variants_are_the_same_address():
    assert normalize_email("Bilal.Ahmed+lahore@Gmail.com") == "bilalahmed@gmail.com"
    assert normalize_email("b.i.l.a.l.ahmed@googlemail.com") == "bilalahmed@gmail.com"


def test_other_providers_keep_dots_but_drop_tags():
    assert normalize_email("Ayesha.S+rentals@Yahoo.com") == "ayesha.s@yahoo.com"


def test_pakistani_phone_formats_match():
    variants = ["0300-1234567", "+92 300 1234567", "0092 300 1234567", "300 1234567", "92-300-123-4567"]
    assert {normalize_phone(variant) for variant in variants} == {"923001234567"}


def test_licence_includes_province_and_ignores_formatting():
    assert normalize_license("sd", "khi-19-88123") == "SD:KHI1988123"
    assert normalize_license("SD", "KHI1988123") != normalize_license("PB", "KHI1988123")


def test_fingerprints_do_not_contain_raw_values():
    hashes = identity_hashes("a@b.com", "03001234567", "SD", "KHI1988123")
    assert all(len(value) == 64 and "KHI1988123" not in value for value in hashes.values())
