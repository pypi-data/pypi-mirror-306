"""Common functions for PazGas Power API."""

import http
import logging
from datetime import datetime
from json import JSONDecodeError
from typing import Any, Optional

from aiohttp import ClientError, ClientResponse, ClientSession

from pazgas_power.models.error import PazGasErrorResponse

from .exceptions import PazGasPowerError

_LOGGER = logging.getLogger(__name__)


async def parse_error_response(resp, response_content):
    _LOGGER.warning(f"Failed call: (Code {resp.status}): {resp.reason} -> {response_content}")
    try:
        json_resp = await resp.json(content_type=None)
        try:
            err = PazGasErrorResponse.parse_obj(json_resp)
            raise PazGasPowerError(f"Error PazGas Power API: {err.error} - {err.message}")
        except Exception:
            raise PazGasPowerError(f"Error PazGas Power API: {json_resp}")
    except Exception as e:
        raise PazGasPowerError(f"Error PazGas Power API: {resp.status}): {resp.reason} - {e}")


HEADERS = {
    "Accept": "*/*",
    "Accept-Language": "en-US,en;q=0.9,fr;q=0.8,he;q=0.7",
    "Content-Type": "application/json",
    "Origin": "https://personalarea.pazgas.co.il",
    "Priority": "u=1, i",
    "Referer": "https://personalarea.pazgas.co.il/login",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko Safari/537.36",
    "X-Web-Client": "pazgas_webapp",
}

AUTH_HEADERS = HEADERS.copy()

version: Optional[str] = None
version_fetch_datetime: Optional[datetime] = None


def get_auth_headers(token: str) -> dict:
    AUTH_HEADERS["Authorization"] = f"{token}"
    return AUTH_HEADERS


async def send_get_request(session: ClientSession, url: str) -> ClientResponse:
    try:
        resp: ClientResponse = await session.get(url)
    except TimeoutError as ex:
        raise PazGasPowerError(f"Failed to communicate with PazGas Power API due to timeout: ({str(ex)})")
    except ClientError as ex:
        raise PazGasPowerError(f"Failed to communicate with PazGas Power API due to ClientError: ({str(ex)})")
    except JSONDecodeError as ex:
        raise PazGasPowerError(f"Received invalid response from PazGas Power API: {str(ex)}")

    return resp


async def send_post_json_request(
    session: ClientSession,
    token: str | None,
    url: str,
    timeout: Optional[int] = 300,
    headers: Optional[dict] = None,
    data: Optional[dict] = None,
    json_data: Optional[dict] = None,
    use_auth: Optional[bool] = True,
) -> dict[str, Any]:
    resp = await send_post_request(data, headers, json_data, session, timeout, token, url, use_auth)

    json = await resp.json(content_type=None)

    _LOGGER.debug(f"{url} responded with data: {json}")
    return json


async def send_post_request(data, headers, json_data, session, timeout, token, url, use_auth):
    try:
        if not headers:
            headers = HEADERS if not use_auth else get_auth_headers(token)

        if not timeout:
            timeout = session.timeout

        _LOGGER.debug(f"Sending POST request to {url} with data: {json_data}")
        resp = await session.post(url=url, data=data, json=json_data, headers=headers, timeout=timeout)
    except TimeoutError as ex:
        raise PazGasPowerError(f"Failed to communicate with PazGas Power API due to timeout: ({str(ex)})")
    except ClientError as ex:
        raise PazGasPowerError(f"Failed to communicate with PazGas Power API due to ClientError: ({str(ex)})")
    except JSONDecodeError as ex:
        raise PazGasPowerError(f"Received invalid response from PazGas Power API: {str(ex)}")
    if resp.status == http.HTTPStatus.UNAUTHORIZED:
        raise PazGasPowerError("Unauthorized request, please check your JWT token")
    if resp.status != http.HTTPStatus.OK:
        await parse_error_response(resp, await resp.text())
    return resp


def is_valid_israeli_id(id):
    id = str(id).strip()
    if len(id) > 9 or len(id) < 5 or not id.isdigit():
        return False

    # Pad string with zeros up to 9 digits
    id = id.zfill(9)

    total = sum(
        (int(digit) * (2 if i % 2 else 1) - 9)
        if int(digit) * (2 if i % 2 else 1) > 9
        else int(digit) * (2 if i % 2 else 1)
        for i, digit in enumerate(id)
    )

    return total % 10 == 0


def validate_phone(phone):
    phone = phone.replace("-", "")
    phone = str(phone).strip()
    if len(phone) != 10 or not phone.isdigit():
        return 0
    return phone[:3] + "-" + phone[3:]
