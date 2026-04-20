"""Helpers for external API calls.

Each call is split into a dedicated function so routes can orchestrate
multiple calls in a predictable order.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

import requests


@dataclass
class ApiResponse:
    name: str
    ok: bool
    status_code: int
    data: Any


def fetch_json(name: str, url: str, timeout: int = 10) -> ApiResponse:
    """Fetch JSON from a URL and normalize the response payload."""
    try:
        response = requests.get(url, timeout=timeout)
        response.raise_for_status()
        return ApiResponse(
            name=name,
            ok=True,
            status_code=response.status_code,
            data=response.json(),
        )
    except requests.RequestException as exc:
        status_code = getattr(exc.response, "status_code", 0) if hasattr(exc, "response") else 0
        return ApiResponse(name=name, ok=False, status_code=status_code, data={"error": str(exc)})


def call_all_services() -> dict[str, Any]:
    """Call each configured API in separate requests and return combined output."""
    calls = [
        ("posts", "https://jsonplaceholder.typicode.com/posts/1"),
        ("users", "https://jsonplaceholder.typicode.com/users/1"),
    ]

    results: dict[str, Any] = {}
    failures: list[dict[str, Any]] = []

    for name, url in calls:
        result = fetch_json(name=name, url=url)
        results[name] = result.data
        if not result.ok:
            failures.append(
                {
                    "service": name,
                    "status_code": result.status_code,
                    "error": result.data,
                }
            )

    return {
        "ok": len(failures) == 0,
        "results": results,
        "failures": failures,
    }
