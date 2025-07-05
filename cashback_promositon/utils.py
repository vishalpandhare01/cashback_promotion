# parse values if invalid
def parse_float(value, field_name):
    try:
        return float(value)
    except (ValueError, TypeError):
        raise ValueError(f"{field_name} must be a number.")
    