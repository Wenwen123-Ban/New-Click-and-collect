from __future__ import annotations

from flask import Flask, jsonify

from api_clients import call_all_services

app = Flask(__name__)


@app.get('/health')
def health() -> tuple:
    return jsonify({'status': 'ok'}), 200


@app.post('/run-sync')
def run_sync() -> tuple:
    """Run backend jobs synchronously in a single request thread."""
    payload = call_all_services()
    status_code = 200 if payload['ok'] else 502
    return jsonify(payload), status_code


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
