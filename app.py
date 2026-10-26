import os

from flask import Flask, jsonify

app = Flask(__name__)

APP_VERSION = os.getenv("APP_VERSION", "0.1.0")
APP_READY = True


@app.get("/")
def home():
    return """
    <!doctype html>
    <html lang="en">
      <head><title>OpsPulse</title></head>
      <body>
        <h1>OpsPulse</h1>
        <p>Service is running.</p>
        <p>Check <a href="/health">health</a> or <a href="/api/status">API status</a>.</p>
      </body>
    </html>
    """


@app.get("/health")
def health():
    return jsonify(status="healthy"), 200


@app.get("/ready")
def ready():
    if not APP_READY:
        return jsonify(status="not ready"), 503

    return jsonify(status="ready"), 200


@app.get("/api/status")
def api_status():
    return jsonify(status="ok", version=APP_VERSION), 200