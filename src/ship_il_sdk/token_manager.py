import time


class TokenManager:
    def __init__(self, refresh_margin=60):
        self.token = None
        self.expiry = 0
        self.refresh_margin = refresh_margin

    def set_token(self, token, ttl=3600):
        self.token = token
        effective_ttl = max(int(ttl) - self.refresh_margin, 0)
        self.expiry = time.time() + effective_ttl

    def is_expired(self):
        return time.time() >= self.expiry

    def get(self):
        return self.token
