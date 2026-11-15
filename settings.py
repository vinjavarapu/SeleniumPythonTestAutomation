"""Application settings used by the browser test suite."""

from dataclasses import dataclass


@dataclass(frozen=True)
class AppSettings:
    """Runtime settings shared by tests and page objects."""

    base_url: str
    username: str
    password: str
    wait_seconds: float
