import jwt
import secrets


class JWTTokenProvider():

    def __init__(self):
        self.secret = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJsb2dpbiI6Ik1pZ3VlbCJ9.NMjlW5JlMXcC6AQS2G7C3jm8GyOJK0e17FzLsLgcnIA"

    def signin(self, payload: dict) -> str:
        token = jwt.encode(payload, self.secret, algorithm="HS256")
        return token
    
    def decode(self, token) -> dict:
        payload = jwt.decode(token, self.secret, algorithms=["HS256"])
        return payload