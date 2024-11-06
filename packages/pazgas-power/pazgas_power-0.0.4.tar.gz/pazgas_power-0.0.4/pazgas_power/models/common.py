# This file contains common classes
from dataclasses import dataclass, field
from typing import Union

from mashumaro import DataClassDictMixin, field_options
from mashumaro.config import BaseConfig

from pazgas_power.models.auth import SendOtpRequest, VerifyOtpRequest

APIMRequest = Union[VerifyOtpRequest, SendOtpRequest]


@dataclass
class PazGasRequest(DataClassDictMixin):
    """Base class for all PazGas requests"""

    path: str = field(metadata=field_options(alias="path"))
    data: APIMRequest = field(metadata=field_options(alias="data"))

    class Config(BaseConfig):
        serialize_by_alias = True
