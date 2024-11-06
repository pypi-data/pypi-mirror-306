"""API for authentication with PazGas Power."""

import logging

from pazgas_power.models.common import PazGasRequest
from pazgas_power.models.customer_data import CustomerData

from .commons import is_valid_israeli_id, send_post_json_request, validate_phone
from .const import APIM_URL, SEND_OTP_PATH, VERIFY_OTP_PATH
from .models.auth import SendOtpRequest, SendOtpResponse, VerifyOtpRequest

_LOGGER = logging.getLogger(__name__)


class AuthApi:
    def __init__(self, session):
        self._session = session

    async def send_otp(
        self,
        identity_number: str,
        phone: str,
    ) -> SendOtpResponse:
        if not is_valid_israeli_id(identity_number):
            raise ValueError(f"Invalid Israeli ID: {identity_number}")
        phone = validate_phone(phone)
        if not phone:
            raise ValueError(f"Invalid phone number: {phone}")

        req = PazGasRequest(path=SEND_OTP_PATH, data=SendOtpRequest(customer_id=identity_number, customer_phone=phone))

        res = await send_post_json_request(self._session, None, APIM_URL, json_data=req.to_dict(), use_auth=False)
        return SendOtpResponse.from_dict(res)

    async def verify_otp(self, session_id, otp) -> CustomerData:
        req = PazGasRequest(path=VERIFY_OTP_PATH, data=VerifyOtpRequest(session_id=session_id, otp=otp))

        res = await send_post_json_request(self._session, None, APIM_URL, json_data=req.to_dict(), use_auth=False)
        return CustomerData.from_dict(res)
