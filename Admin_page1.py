"""Cleaned admin utility script for the Flask backend.

This replaces older, error-prone logic with a small set of usable commands.
"""

from __future__ import annotations

import json
from typing import Any

import requests

BACKEND_URL = 'http://127.0.0.1:5000'


def _request(method: str, path: str) -> dict[str, Any]:
    response = requests.request(method=method, url=f'{BACKEND_URL}{path}', timeout=20)
    response.raise_for_status()
    return response.json()


def check_health() -> dict[str, Any]:
    return _request('GET', '/health')


def run_sync_job() -> dict[str, Any]:
    return _request('POST', '/run-sync')


def main() -> None:
    print('Admin backend check...')

    health = check_health()
    print('Health:', json.dumps(health, indent=2))

    sync_result = run_sync_job()
    print('Synchronous run result:')
    print(json.dumps(sync_result, indent=2))


if __name__ == '__main__':
    main()
