def is_numeric(value):
    """Check if the input is a numeric value."""
    try:
        float(value)
        return True
    except ValueError:
        return False


def is_valid_iranian_national_code(national_code):
    """Validate Iranian national code."""
    if not national_code.isdigit() or len(national_code) != 10:
        return False

    check = int(national_code[-1])
    sum_ = sum(int(national_code[i]) * (10 - i) for i in range(9)) % 11

    return (sum_ < 2 and check == sum_) or (sum_ >= 2 and check + sum_ == 11)


def is_empty(value):
    """Check if the input is empty."""
    return value is None or str(value).strip() == ""


def is_valid_iranian_mobile(mobile_number):
    """Validate Iranian mobile number."""
    return mobile_number.isdigit() and len(mobile_number) == 11 and mobile_number.startswith("09")
