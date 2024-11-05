"""Data models for authentication"""

from dataclasses import dataclass, field
from uuid import UUID

from mashumaro import DataClassDictMixin, field_options
from mashumaro.config import BaseConfig


@dataclass
class SendOtpRequest(DataClassDictMixin):
    customer_phone: str = field(metadata=field_options(alias="custPhone"))
    customer_id: str = field(metadata=field_options(alias="custId"))

    class Config(BaseConfig):
        serialize_by_alias = True


@dataclass
class SendOtpResponse(DataClassDictMixin):
    session_id: UUID = field(metadata=field_options(alias="sessionId"))
    otp: str = field(metadata=field_options(alias="otp"))

    class Config(BaseConfig):
        serialize_by_alias = True


@dataclass
class VerifyOtpRequest(DataClassDictMixin):
    session_id: UUID = field(metadata=field_options(alias="SessionId"))
    otp: str = field(metadata=field_options(alias="OTP"))

    class Config(BaseConfig):
        serialize_by_alias = True
