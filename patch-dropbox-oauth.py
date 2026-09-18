from pathlib import Path

TARGET = Path("/opt/hermes/tools/mcp_oauth.py")

text = TARGET.read_text(encoding="utf-8")

old_import = "from urllib.parse import parse_qs, urlparse"
new_import = "from urllib.parse import parse_qs, parse_qsl, urlencode, urlparse"

if old_import not in text:
    raise RuntimeError(
        "Dropbox OAuth patch aborted: expected urllib.parse import was not found. "
        "Hermes source may have changed."
    )

text = text.replace(old_import, new_import, 1)

old_handler = """    async def _redirect_handler(authorization_url: str) -> None:
        dashboard_flow = get_dashboard_oauth_flow()
"""

new_handler = """    async def _redirect_handler(authorization_url: str) -> None:
        # Dropbox returns a refresh_token only when offline access is requested
        # on the authorization URL. Apply this only to Dropbox OAuth and only
        # when token_access_type was not already specified.
        parsed_auth_url = urlparse(authorization_url)
        auth_host = (parsed_auth_url.hostname or "").lower()

        if (
            auth_host in {"www.dropbox.com", "dropbox.com"}
            and parsed_auth_url.path.rstrip("/") == "/oauth2/authorize"
        ):
            auth_params = parse_qsl(parsed_auth_url.query, keep_blank_values=True)

            if not any(key == "token_access_type" for key, _ in auth_params):
                auth_params.append(("token_access_type", "offline"))
                authorization_url = parsed_auth_url._replace(
                    query=urlencode(auth_params)
                ).geturl()

        dashboard_flow = get_dashboard_oauth_flow()
"""

if old_handler not in text:
    raise RuntimeError(
        "Dropbox OAuth patch aborted: expected redirect handler was not found. "
        "Hermes source may have changed."
    )

text = text.replace(old_handler, new_handler, 1)

TARGET.write_text(text, encoding="utf-8")

print("Dropbox OAuth offline-access patch applied successfully.")
