import re

from django.core.exceptions import ValidationError

validate_picture = ["jpg", "jpeg", "png", "gif", "bmp", "tiff", "webp", "svg", "ico"]

UZB_PHONE_REGEX = r"^\+998( ?94| ?[3-9]\d) ?\d{3} ?\d{2} ?\d{2}$"

def validate_phone(value):
    if not re.match(UZB_PHONE_REGEX, value):
        raise ValidationError("Noto‘g‘ri telefon raqam formati! (+998 XX XXX XX XX)")