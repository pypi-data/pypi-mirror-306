import re
import socket
import threading
import time
import urllib.parse
import webbrowser
from datetime import datetime, timezone, timedelta
from typing import Optional, Any
from urllib.parse import parse_qs

import jwt
import requests
from requests import RequestException
from terevintosoftware.pkce_client import PkceClient, PkceLoginConfig
from terevintosoftware.pkce_client.token_config_map import TokenConfigMap

from ._logger_config import _global_logger
from .config import _AZURE_SAS_TOKEN_EXPIR_GRACE_PERIOD


def _insert_proxy_auth(proxy_url: str, username: Optional[str], password: Optional[str]) -> str:
    if '//' not in proxy_url:
        raise ValueError('Proxy URL must contain http:// or https://')
    if username:
        prefix, hostname = proxy_url.split("//")
        password_str = f":{urllib.parse.quote(password)}" if password else ""
        return f"{prefix}//{urllib.parse.quote(username)}{password_str}@{hostname}"
    else:
        return proxy_url


def _is_token_expired_or_about_to_expire(token: str, token_refresh_window: int = 600) -> bool:
    try:
        decoded = jwt.decode(token, options={"verify_signature": False})
        if 'exp' in decoded:
            exp_time = decoded['exp']
            current_time = time.time()
            # time in seconds
            return current_time > exp_time - token_refresh_window
        return False
    except jwt.DecodeError:
        raise
    except jwt.ExpiredSignatureError:
        return True


def _parse_azp_from_token(token: str) -> str:
    try:
        decoded = jwt.decode(token, options={"verify_signature": False})
        return decoded.get('azp', None)
    except jwt.DecodeError:
        raise


def _sanitize_url(url: str) -> str:
    """
    handles multiple slashes in url by replacing them with a single slash, while keeping the double slashes after protocol scheme
    :param url:
    :return:
        sanitized url
    """
    parts = url.split('://')
    result = parts[0] + '://' + re.sub('//+', '/', parts[1])
    return result


def _find_free_port():
    # Create a socket
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        try:
            # Bind the socket to a random port
            s.bind(('', 0))

            # Get the port number
            _, port = s.getsockname()

            return port
        except OSError as e:
            raise EnvironmentError(f"Unable to bind a free port: {e}")
        finally:
            # Close the socket
            s.close()


class TokenHolder:
    def __init__(self, **kwargs: Any) -> None:
        self.domain = kwargs['domain']
        self.realm = kwargs['realm']
        self.client_id = kwargs['client_id']
        self.session = kwargs['session']

        # Time window (in seconds) before access_token expiry when it's still valid but eligible for refresh.
        self.token_refresh_window = kwargs.get('token_refresh_window', 60)
        self.access_token = kwargs.get('access_token', '')
        self.refresh_token = kwargs.get('refresh_token', '')

        # initializing lock - needed for concurrent uploading of files to prevent race conditions
        self._lock = threading.Lock()

    def get_tokens_with_credentials(self, username, password) -> None:
        _global_logger.debug('retrieving access-/refresh-token using credentials')
        data = {
            "grant_type": "password",
            "client_id": self.client_id,
            "username": username,
            "password": password
        }
        try:
            response = self.session.post(f'https://{self.domain}/auth/realms/{self.realm}/protocol/openid-connect/token', data=data)
            response.raise_for_status()
            response_json = response.json()

            # Ensure the expected keys are in the response
            if "access_token" in response_json and "refresh_token" in response_json:
                self.access_token = response_json["access_token"]
                self.refresh_token = response_json["refresh_token"]
            else:
                raise KeyError("Expected keys 'access_token' and 'refresh_token' not found in response")

        except (KeyError, RequestException, ValueError) as err:
            _global_logger.error(f'An error occurred: {err}')
            raise
        except Exception as err:
            _global_logger.error(f'An unexpected error occurred: {err}')
            raise

    def get_tokens_by_authflow(self) -> None:
        _global_logger.debug('retrieving access-/refresh-token using authflow')
        config = PkceLoginConfig(
                authorization_uri=f'https://{self.domain}/auth/realms/{self.realm}/protocol/openid-connect/auth',
                token_uri=f'https://{self.domain}/auth/realms/{self.realm}/protocol/openid-connect/token',
                scopes=["openid"],
                client_id=self.client_id,
                internal_port=_find_free_port(),
                add_random_state=True,
                random_state_length=32,
                verify_authorization_server_https=True,
                token_config_map=TokenConfigMap(scopes='scope'))

        login_client = PkceClient(config)
        pkce_token = login_client.login()
        self.access_token = pkce_token.access_token
        self.refresh_token = pkce_token.refresh_token

    def _refresh_tokens(self):
        payload = {
            'grant_type': 'refresh_token',
            'refresh_token': self.refresh_token,
            'client_id': self.client_id
        }
        headers = {'Content-Type': 'application/x-www-form-urlencoded'}

        try:
            response = self.session.post(f'https://{self.domain}/auth/realms/{self.realm}/protocol/openid-connect/token', headers=headers, data=payload)
            response.raise_for_status()
            response_json = response.json()
            self.access_token = response_json.get("access_token")
            self.refresh_token = response_json.get("refresh_token")
            _global_logger.debug('tokens refreshed.')
        except requests.exceptions.HTTPError as http_err:
            raise TokenRefreshError(response.status_code, f"[CRITICAL] Failed to refresh tokens: HTTP error occurred - {http_err}") from http_err
        except requests.exceptions.RequestException as req_err:
            raise TokenRefreshError(-1, f"Failed to refresh tokens: Request error occurred - {req_err}") from req_err
        except KeyError as key_err:
            raise TokenRefreshError(-1, f"Failed to refresh tokens: Key error occurred - Missing {key_err} in the response") from key_err
        except Exception as err:
            raise TokenRefreshError(-1, f"Failed to refresh tokens: An unexpected error occurred - {err}") from err

    def get_token(self) -> str:
        with self._lock:
            if _is_token_expired_or_about_to_expire(self.access_token, self.token_refresh_window):
                _global_logger.debug('access-token expired - refreshing tokens...')
                self._refresh_tokens()
            return self.access_token


class TokenRefreshError(Exception):
    """Custom exception for errors occurring during token refresh."""

    def __init__(self, status_code, message="Error occurred during token refresh"):
        self.status_code = status_code
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        if self.status_code > 0:
            return f"{self.message} (Status Code: {self.status_code})"
        else:
            return self.message


def _is_browser_available():
    try:
        webbrowser.get()
        return True
    except webbrowser.Error:
        _global_logger.warn('no browser available')
        return False


def _storage_access_info_should_be_renewed(sas_token: str) -> bool:
    params = parse_qs(sas_token)

    # extract expiration (`se`)
    expiry_time_str = params.get("se", [None])[0]

    if not expiry_time_str:
        _global_logger.warn("no expiration-date in SAS-Token found.")
        return False

    # convert expiration to datetime
    expiry_time = datetime.strptime(expiry_time_str, "%Y-%m-%dT%H:%M:%SZ")
    expiry_time = expiry_time.replace(tzinfo=timezone.utc)

    current_time = datetime.now(timezone.utc)
    grace_period = timedelta(minutes=_AZURE_SAS_TOKEN_EXPIR_GRACE_PERIOD)

    # compare expiration with current time
    return current_time > (expiry_time - grace_period)


def _calculate_chunk_size(file_size: int):
    """
    Determines the optimal chunk size for uploading a file based on its size.

    This heuristic function selects an appropriate chunk size to efficiently upload files
    of various sizes.

    :param file_size: The total size of the file in bytes.
    :return: The recommended chunk size in bytes.
    """
    if file_size < 104857600:  # 100 * 1024 * 1024 - Less than 100 MiB
        return 2097152  # 2 * 1024 * 1024 (4 MB)
    elif file_size < 1073741824:  # 1024 * 1024 * 1024 - Between 100 MiB and 1 GiB
        return 4194304  # 4 * 1024 * 1024  (8 MiB)
    elif file_size < 5368709120:  # 5 * 1024 * 1024 * 1024: - Between 1 GiB and 5 GiB
        return 8388608  # 8 * 1024 * 1024 (16 MiB)
    else:  # Greater than 5 GiB
        return 16777216  # 16 * 1024 * 1024 (32 MiB)


class AzureStorageAccessInfo:
    def __init__(self, token: str, url: str):
        self.token = token
        self.url = url

    def __str__(self):
        return f"AccessmanagerSASTokenResponse(token='{self.token}', url='{self.url}')"

    def __repr__(self):
        return f"AccessmanagerSASTokenResponse(token={repr(self.token)}, url={repr(self.url)})"

    def __eq__(self, other):
        if not isinstance(other, AzureStorageAccessInfo):
            return False
        return self.token == other.token and self.url == other.url

    def __hash__(self):
        return hash((self.token, self.url))

    @classmethod
    def from_json(cls, json_data: dict):
        token = json_data.get('token')
        url = json_data.get('url')
        if token is None or url is None:
            raise ValueError("Missing required fields 'token' or 'url' in JSON data")
        return cls(token=token, url=url)
