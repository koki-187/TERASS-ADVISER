"""
A simple proxy server that forwards chat completion requests to the OpenAI API.

This script uses Flask to expose a single POST endpoint at ``/openai/chat``.  Clients
must include an ``X-MyAgent-Token`` header whose value matches the
``INTERNAL_APP_TOKEN`` environment variable.  The proxy will forward the
request body to the OpenAI Chat Completions API using the ``OPENAI_API_KEY``
environment variable for authorization, and return the response unchanged.

Running this server allows mobile or desktop applications to avoid bundling
API secrets directly in client-side code.  Instead, the secrets remain on
the server and can be rotated centrally without requiring a new app release.
"""

from flask import Flask, request, Response
import os
import requests


app = Flask(__name__)

# Fetch sensitive values from the environment.  These should be populated via
# your secret management solution (e.g. Bitwarden) prior to starting the
# application.  See setup scripts for examples of how to populate them.
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
INTERNAL_APP_TOKEN = os.getenv("INTERNAL_APP_TOKEN")


@app.post("/openai/chat")
def proxy_chat() -> Response:
    """Proxy an OpenAI chat completion request.

    The client must provide the ``X-MyAgent-Token`` header.  The body is
    forwarded to OpenAI as JSON.  Any error during the forward will be
    returned as a 500 response.
    """
    token = request.headers.get("X-MyAgent-Token")
    if not token or token != INTERNAL_APP_TOKEN:
        # Respond with 403 if the provided token is missing or incorrect.
        return Response("Forbidden", status=403)

    if not OPENAI_API_KEY:
        # If the API key isn't set, we can't contact OpenAI.
        return Response("API key not configured", status=500)

    # Build the request to OpenAI.  Accept whatever JSON the client provided.
    payload = request.get_json(silent=True)
    url = "https://api.openai.com/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {OPENAI_API_KEY}",
        "Content-Type": "application/json",
    }

    try:
        response = requests.post(url, headers=headers, json=payload, timeout=60)
        return Response(
            response.content,
            status=response.status_code,
            content_type=response.headers.get("Content-Type", "application/json"),
        )
    except requests.RequestException as exc:
        # Surface network or request errors to the caller.
        return Response(str(exc), status=500)


if __name__ == "__main__":
    # Default to port 8080, but allow overriding via the PORT environment variable.
    port = int(os.getenv("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
