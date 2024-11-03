from typing import List
from uuid import UUID

import requests


class SquareAuthenticationHelper:
    def __init__(
        self,
        param_int_square_authentication_port: int = 10011,
        param_str_square_authentication_ip: str = "localhost",
        param_str_square_authentication_protocol: str = "http",
    ):
        try:
            self.global_str_square_authentication_url_base = (
                f"{param_str_square_authentication_protocol}://"
                f"{param_str_square_authentication_ip}:{param_int_square_authentication_port}"
            )
        except Exception:
            raise

    def _make_request(self, method, endpoint, data=None, params=None, headers=None):
        try:
            url = f"{self.global_str_square_authentication_url_base}/{endpoint}"
            if headers:
                headers = {
                    key.replace("_", "-"): value for key, value in headers.items()
                }
            response = requests.request(
                method,
                url,
                json=data,
                params=params,
                headers=headers,
            )
            response.raise_for_status()
            return response.json()
        except Exception:
            raise

    def register_username_v0(
        self,
        username: str,
        password: str,
    ):
        try:
            endpoint = "register_username/v0"
            params = {
                "username": username,
                "password": password,
            }
            return self._make_request(method="POST", endpoint=endpoint, params=params)
        except Exception:
            raise

    def login_username_v0(
        self,
        username: str,
        password: str,
        app_id: int,
    ):
        try:
            endpoint = "login_username/v0"
            params = {
                "username": username,
                "password": password,
                "app_id": app_id,
            }
            return self._make_request(method="GET", endpoint=endpoint, params=params)
        except Exception:
            raise

    def generate_access_token_v0(
        self,
        user_id: str,
        app_id: int,
        refresh_token: str,
    ):
        try:
            endpoint = "generate_access_token/v0"
            params = {
                "user_id": user_id,
                "app_id": app_id,
            }
            headers = {
                "refresh_token": refresh_token,
            }
            return self._make_request(
                method="GET", endpoint=endpoint, params=params, headers=headers
            )
        except Exception:
            raise

    def logout_v0(
        self,
        user_id: str,
        app_id: int,
        access_token: str,
        refresh_token: str,
    ):
        try:
            endpoint = "logout/v0"
            params = {
                "user_id": user_id,
                "app_id": app_id,
            }
            headers = {
                "refresh_token": refresh_token,
                "access_token": access_token,
            }
            return self._make_request(
                method="DELETE", endpoint=endpoint, params=params, headers=headers
            )
        except Exception:
            raise

    def get_user_app_ids_v0(
        self,
        user_id: UUID,
    ):
        try:
            endpoint = "get_user_app_ids/v0"
            params = {
                "user_id": user_id,
            }
            return self._make_request(
                method="GET",
                endpoint=endpoint,
                params=params,
            )
        except Exception:
            raise

    def update_user_app_ids_v0(
        self,
        user_id: UUID,
        app_ids_to_add: List[int],
        app_ids_to_remove: List[int],
    ):
        try:
            endpoint = "update_user_app_ids/v0"
            params = {
                "user_id": user_id,
            }
            payload = {
                "app_ids_to_add": app_ids_to_add,
                "app_ids_to_remove": app_ids_to_remove,
            }
            return self._make_request(
                method="PATCH", endpoint=endpoint, params=params, data=payload
            )
        except Exception:
            raise
