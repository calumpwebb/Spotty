import argparse
import base64
import secrets
import urllib.parse

import requests
from flask import Flask, request, redirect, make_response


def create_app(client_id, client_secret, redirect_uri="http://localhost:8888/callback"):
    """
    Create a Flask app with the given Spotify credentials.

    :param client_id: Spotify Client ID (required)
    :param client_secret: Spotify Client Secret (required)
    :param redirect_uri: Redirect URI (default: http://localhost:8888/callback)
    :return: Configured Flask application
    """
    app = Flask(__name__)

    # Spotify config
    SCOPE = (
        "playlist-modify-public "
        "playlist-modify-private "
        "user-read-private "
        "user-read-email "
        "playlist-modify-public "
        "playlist-modify-private"
    )
    STATE_KEY = "spotify_auth_state"

    # Token storage for demo (not secure for production)
    tokens = {}

    def generate_random_string(length=16):
        """Generate a random string for the state parameter."""
        return secrets.token_hex(length // 2)

    @app.route("/login")
    def login():
        state = generate_random_string(16)
        # Set a cookie with the 'state' value
        response = make_response()
        response.set_cookie(STATE_KEY, state)

        query_params = {
            "response_type": "code",
            "client_id": client_id,
            "scope": SCOPE,
            "redirect_uri": redirect_uri,
            "state": state,
        }
        auth_url = "https://accounts.spotify.com/authorize?" + urllib.parse.urlencode(
            query_params
        )
        return redirect(auth_url)

    @app.route("/callback")
    def callback():
        # Invalidate the state cookie
        response = make_response()
        response.set_cookie(STATE_KEY, "", expires=0)

        code = request.args.get("code")
        if not code:
            return redirect("/#?" + urllib.parse.urlencode({"error": "missing_code"}))

        # Exchange authorization code for tokens
        token_url = "https://accounts.spotify.com/api/token"
        headers = {
            "Content-Type": "application/x-www-form-urlencoded",
            "Authorization": "Basic "
            + base64.b64encode(f"{client_id}:{client_secret}".encode()).decode(),
        }
        data = {
            "code": code,
            "redirect_uri": redirect_uri,
            "grant_type": "authorization_code",
        }

        r = requests.post(token_url, data=data, headers=headers)
        if r.status_code == 200:
            tokens.update(r.json())  # store tokens in-memory
            return redirect("/")
        else:
            return redirect("/#?" + urllib.parse.urlencode({"error": "invalid_token"}))

    @app.route("/")
    def home():
        if not tokens:
            return "No tokens available. Please <a href='/login'>login</a> first."
        access_token = tokens.get("access_token")
        refresh_token = tokens.get("refresh_token")
        return f"""
        <html>
        <body>
            <h1>Spotify Authorization Successful!</h1>
            <h2>Here are your tokens and credentials:</h2>
            <p><strong>Access Token:</strong></p>
            <textarea rows="4" cols="100">{access_token}</textarea>
            <p><strong>Refresh Token:</strong></p>
            <textarea rows="4" cols="100">{refresh_token}</textarea>
            <p><strong>Client ID:</strong></p>
            <textarea rows="1" cols="100">{client_id}</textarea>
            <p><strong>Client Secret:</strong></p>
            <textarea rows="1" cols="100">{client_secret}</textarea>
            <p>Copy these values for use in your API calls!</p>
            <a href="/login">Login again</a>
        </body>
        </html>
        """

    @app.route("/favicon.ico")
    def favicon():
        return "", 204

    return app


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Spotify OAuth2 callback server.")
    parser.add_argument(
        "--client-id", required=True, help="Spotify Client ID (required)"
    )
    parser.add_argument(
        "--client-secret", required=True, help="Spotify Client Secret (required)"
    )
    parser.add_argument(
        "--redirect-uri",
        default="http://localhost:8888/callback",
        help="Spotify Redirect URI (default: http://localhost:8888/callback)",
    )
    args = parser.parse_args()

    app = create_app(
        client_id=args.client_id,
        client_secret=args.client_secret,
        redirect_uri=args.redirect_uri,
    )
    app.run(port=8888, debug=True)
