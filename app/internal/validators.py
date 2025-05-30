"""
Shared validation utilities for the FastAPI Todo application.

This module contains reusable validation functions to avoid code duplication
across different models.
"""

import re
from typing import Optional


def validate_username(username: Optional[str]) -> Optional[str]:
    """
    Validate and normalize username.

    Args:
        username: Username to validate (can be None for optional fields)

    Returns:
        Normalized username (lowercase) or None if input was None

    Raises:
        ValueError: If username doesn't meet requirements
    """
    if username is None:
        return None

    # Allow only alphanumeric characters, hyphens, and underscores
    if not re.match(r"^[a-zA-Z0-9_-]+$", username):
        raise ValueError(
            "Username can only contain letters, numbers, hyphens, and underscores"
        )

    # Ensure it doesn't start or end with special characters
    if username.startswith(("-", "_")) or username.endswith(("-", "_")):
        raise ValueError("Username cannot start or end with hyphens or underscores")

    return username.lower()  # Normalize to lowercase


def validate_password(password: Optional[str]) -> Optional[str]:
    """
    Validate password strength.

    Args:
        password: Password to validate (can be None for optional fields)

    Returns:
        The original password if valid, or None if input was None

    Raises:
        ValueError: If password doesn't meet security requirements
    """
    if password is None:
        return None

    # Check for at least one uppercase letter
    if not re.search(r"[A-Z]", password):
        raise ValueError("Password must contain at least one uppercase letter")

    # Check for at least one lowercase letter
    if not re.search(r"[a-z]", password):
        raise ValueError("Password must contain at least one lowercase letter")

    # Check for at least one digit
    if not re.search(r"\d", password):
        raise ValueError("Password must contain at least one number")

    # Check for at least one special character
    if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
        raise ValueError(
            'Password must contain at least one special character (!@#$%^&*(),.?":{}|<>)'
        )

    # Check for common weak passwords
    weak_passwords = ["password", "12345678", "password123", "admin123"]
    if password.lower() in weak_passwords:
        raise ValueError("Password is too common, please choose a stronger password")

    return password


def validate_task_title(title: Optional[str]) -> Optional[str]:
    """
    Validate and normalize task title.

    Args:
        title: Task title to validate (can be None for optional fields)

    Returns:
        Trimmed title or None if input was None

    Raises:
        ValueError: If title doesn't meet requirements
    """
    if title is None:
        return None

    # Remove leading/trailing whitespace
    title = title.strip()

    # Ensure title is not empty after stripping
    if not title:
        raise ValueError("Task title cannot be empty or only whitespace")

    # Check for extremely short or meaningless titles
    if len(title) < 2:
        raise ValueError("Task title must be at least 2 characters long")

    return title


def validate_task_description(description: Optional[str]) -> Optional[str]:
    """
    Validate and normalize task description.

    Args:
        description: Task description to validate (can be None)

    Returns:
        Trimmed description or None if empty/None
    """
    if description is None:
        return None

    # Remove leading/trailing whitespace
    description = description.strip()

    # Return None if empty after stripping
    if not description:
        return None

    return description


# Field configuration constants for reusability
USERNAME_FIELD_CONFIG = {
    "min_length": 3,
    "max_length": 50,
    "description": "Username must be 3-50 characters long",
}

PASSWORD_FIELD_CONFIG = {
    "min_length": 8,
    "max_length": 128,
    "description": "Password must be 8-128 characters long",
}

TASK_TITLE_FIELD_CONFIG = {
    "min_length": 1,
    "max_length": 200,
    "description": "Task title must be 1-200 characters long",
}

TASK_DESCRIPTION_FIELD_CONFIG = {
    "max_length": 1000,
    "description": "Task description must not exceed 1000 characters",
}
