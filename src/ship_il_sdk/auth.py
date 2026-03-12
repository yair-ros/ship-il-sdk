from .exceptions import AuthenticationError


def authenticate(session, base_url, username, password, customer_id):
    r = session.post(
        f"{base_url}/Token",
        data={
            "username": username,
            "password": password,
            "scope": str(customer_id),
            "grant_type": "password",
        },
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )

    if r.status_code != 200:
        raise AuthenticationError(r.text)

    data = r.json()
    token = data.get("access_token")

    if not token:
        raise AuthenticationError("Token missing")

    session.headers["Authorization"] = f"Bearer {token}"
    return token, int(data.get("expires_in", 3600))
