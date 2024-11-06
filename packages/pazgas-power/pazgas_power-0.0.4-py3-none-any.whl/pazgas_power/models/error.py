"""Error response model"""

from dataclasses import dataclass, field

from mashumaro import DataClassDictMixin, field_options


@dataclass
class PazGasErrorResponse(DataClassDictMixin):
    """Represents an error response."""

    error: str = field(metadata=field_options(alias="error"))
    status: int = field(metadata=field_options(alias="status"))
    message: str = field(metadata=field_options(alias="message"))
