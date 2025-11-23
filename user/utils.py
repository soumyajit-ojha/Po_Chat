"""
This module contains utility functions that are useed across this user app.
"""

import re
import os
from django.core.exceptions import ValidationError


def validate_phone_number(phone_number: str) -> str:
    """
    Validate phone:
    - Must start with '+91' followed by india country code and number groups.
    - Only digits allowed after the '+'.
    Example: +919876543210
    Returns:
        phone (str): value
    Raises:
        ValidationError: If the phone number is invalid.
    """
    if not phone_number or not phone_number.strip():
        raise ValidationError("Phone number is required.")

    phone_number = phone_number.strip()

    if not re.match(r"^\+91\d{10}$", phone_number):
        raise ValidationError(
            "Invalid phone number format. Use format like +919876543210."
        )

    return phone_number


def validate_name(
    name: str,
    ignored_chars: str = "",
    min_len: int = 1,
    max_len: int = 50,
    allow_blank: bool = True,
) -> str:
    """
    Validate a name:
    - Only allows uppercase/lowercase letters and ignored_chars.
    - Length must be in min_len to max_len.
    - Disallows digits and other special characters.
    - allow empty string or none

    Args:
        name (str): The input name to validate.
        ignored_chars (str): Characters to ignore during validation.
        min_length (int): Minimum allowed length of the name.
        max_length (int): Maximum allowed length of the name.
        allow_blank (bool): If True, allows empty strings or None.
    Returns:
        name (str): validated_name
    Raises:
        ValidationError: If the name is invalid.
    """
    if not name or not name.strip():
        if allow_blank:
            return ""
        raise ValidationError("Name is required to validate.")

    name = name.strip()
    # Remove ignored characters before validation
    if ignored_chars:
        pattern = f"[{re.escape(ignored_chars)}]"
        cleaned_name = re.sub(pattern, "", name)
    else:
        cleaned_name = name
    # validate pattern
    if not re.match(r"^[A-Za-z ]+$", cleaned_name):
        raise ValidationError(
            f"Invalid format. Use only letters, space {ignored_chars}"
        )
    # validate length
    if not min_len <= len(cleaned_name) <= max_len:
        raise ValidationError(
            f"Name length must be between {min_len} and {max_len} characters."
        )

    return name


def validate_password(password):
    """
    Validates the given password against security rules.
    """
    if not 7 <= len(password) <= 20 :
        raise ValidationError("Password length must be within 7 to 20 characters.")
    if not re.search(r"[A-Z]", password):
        raise ValidationError("Password must contain at least one uppercase letter.")
    if not re.search(r"[a-z]", password):
        raise ValidationError("Password must contain at least one lowercase letter.")
    if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
        raise ValidationError("Password must contain at least one special character.")
    if not re.search(r"[0-9]", password):
        raise ValidationError("Password must contain at least one digit.")
    return password


def validate_email(email: str, allow_blanck: bool = True) -> str:
    """validatea a email"""

    if not email or not email.strip():
        if allow_blanck:
            return ""
        raise ValidationError("Email is required.")
    email = email.strip()
    if not re.match(r"^[a-z0-9._%-]+@[a-z0-9.-]+\.[a--z]{2,}$", email):
        raise ValidationError(
            "email must be lowercase and valid format (e.g., dummy12@email.com)"
        )
    return email


def validate_uploaded_file(
    file_obj,
    allowed_image_formats: tuple = (".png", ".jpeg", ".jpg"),
    max_size_mb: float = 2,
):
    """
    Validate uploaded file based on size and extension.

    Args:
        file_obj: Uploaded file object
        allowed_types (tuple): tuple of allowed file extensions
        max_size_mb (int): Max file size in MB

    Raises:
        ValidationError: If file is invalid
    """
    # 1. Validate file size
    max_size_bytes = max_size_mb * 1024 * 1024
    if file_obj.size > max_size_bytes:
        raise ValidationError(f"File size should not exceed {max_size_mb} MB.")

    # 2. Validate file type
    ext = os.path.splitext(file_obj.name)[1].lower()
    if ext not in allowed_image_formats:
        raise ValidationError(
            f"Unsupported file type: {ext}. Allowed types: {allowed_image_formats}"
        )

    return file_obj
