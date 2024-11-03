"""PazGasPower API client."""

import logging
from typing import Optional

import aiohttp
from aiohttp import ClientSession

from pazgas_power.exceptions import PazGasPowerError
from pazgas_power.models.auth import SendOtpResponse
from pazgas_power.models.customer_data import CustomerData

from .auth_api import AuthApi

_LOGGER = logging.getLogger(__name__)


class PazGasPowerApi:
    def __init__(self, user_id: str | int, phone: str, session: Optional[ClientSession] = None):
        self.user_id = str(user_id)
        self.phone = str(phone)

        if not session:
            session = aiohttp.ClientSession()

        self._session = session
        self.auth = AuthApi(self._session)

    async def login_and_get_customer_data(self) -> CustomerData:
        try:
            send_otp_response: SendOtpResponse = await self.auth.send_otp(
                identity_number=self.user_id, phone=self.phone
            )
            return await self.auth.verify_otp(session_id=send_otp_response.session_id, otp=send_otp_response.otp)
        except Exception as ex:
            _LOGGER.error(f"Failed to login and get customer data: {str(ex)}")
            raise PazGasPowerError(f"Failed to login and get customer data - {ex}")
