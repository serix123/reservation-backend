import re
from django.core.exceptions import ValidationError

def validate_philippine_mobile_number(value):
    """Validates Philippine mobile number format: +63-9xx-xxx-xxxx."""
    pattern = r"^\+63-9\d{2}-\d{3}-\d{4}$"
    if not re.match(pattern, value):
        raise ValidationError(
            "Invalid Philippine mobile number format. Use +63-9xx-xxx-xxxx."
        )
