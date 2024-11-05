import requests
import os
from typing import Dict
import time

CURRENT_TOKEN = ""
CURRENT_EXPIRY = -1


class Request:
    def __init__(self, method, url, headers, body=""):
        self.method = method
        self.url = url
        self.headers = headers
        self.body = body

    def __str__(self):
        return f"Request(method={self.method}, url={self.url}, headers={self.headers}, body={self.body})"


class Response:
    def __init__(self, status, headers, body):
        self.status = status
        self.headers = headers
        self.body = body

    def __str__(self):
        return (
            f"Response(status={self.status}, headers={self.headers}, body={self.body})"
        )


class CustomHook:

    def getToken(self, client_id, client_secret):
        full_url = "https://auth.celitech.net/oauth2/token"
        headers = {"Content-type": "application/x-www-form-urlencoded"}
        data = {
            "client_id": client_id,
            "client_secret": client_secret,
            "grant_type": "client_credentials",
        }

        resp = requests.post(full_url, headers=headers, data=data)
        return resp.json()

    def before_request(self, request: Request, **kwargs):
        print("request", request)
        print("kwargs", kwargs)

        client_id = kwargs.get("client_id")
        client_secret = kwargs.get("client_secret")

        print("client_id", client_id)
        print("client_secret", client_secret)

        if not client_id or not client_secret:
            raise Exception(
                "Missing client_id and/or client_secret constructor parameters"
            )

        global CURRENT_TOKEN, CURRENT_EXPIRY

        if not CURRENT_TOKEN or CURRENT_EXPIRY < round(time.time() * 1000):

            token_response = self.getToken(client_id, client_secret)

            print("token_response", token_response)

            if token_response.get("error"):
                raise Exception(token_response.get("error"))

            expires_in = token_response.get("expires_in")
            access_token = token_response.get("access_token")

            if not expires_in or not access_token:
                raise Exception("There is an issue with getting the oauth token")

            CURRENT_EXPIRY = round(time.time() * 1000) + expires_in * 1000
            CURRENT_TOKEN = access_token

        authorization = f"Bearer {CURRENT_TOKEN}"

        print("authorization", authorization)

        request.headers.update({"Authorization": authorization})

    def after_response(self, request: Request, response: Response, **kwargs):
        pass

    def on_error(
        self, error: Exception, request: Request, response: Response, **kwargs
    ):
        pass
