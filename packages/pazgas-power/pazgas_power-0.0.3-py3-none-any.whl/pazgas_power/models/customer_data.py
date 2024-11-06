"""Defines the CustomerData and Invoice data classes."""
import base64
from dataclasses import dataclass, field
from datetime import date
from typing import List, Optional
from uuid import UUID

import aiofiles
from mashumaro import DataClassDictMixin, field_options

from pazgas_power.const import PACKAGES_MAP
from pazgas_power.exceptions import PazGasPowerError
from pazgas_power.models.package import Package


@dataclass
class Invoice(DataClassDictMixin):
    """
    Represents an individual invoice.

    Attributes:
        invoice_number (str): The invoice number.
        invoice_total_price (str): The total price of the invoice.
        invoice_month (int): The month of the invoice.
        invoice_day (int): The day of the invoice.
        invoice_year (int): The year of the invoice.
        invoice_year_sliced (str): The last two digits of the invoice year.
        invoice_file (Optional[str]): The file associated with the invoice, if any.
    """

    invoice_number: str = field(metadata=field_options(alias="invoiceNumber"))
    invoice_total_price: str = field(metadata=field_options(alias="invoiceTotalPrice"))
    invoice_month: int = field(metadata=field_options(alias="invoiceMonth"))
    invoice_day: int = field(metadata=field_options(alias="invoiceDay"))
    invoice_year: int = field(metadata=field_options(alias="invoiceYear"))
    invoice_year_sliced: str = field(metadata=field_options(alias="invoiceYearSliced"))
    invoice_file: Optional[str] = field(metadata=field_options(alias="invoiceFile"))

    async def write_pdf_invoice_file(self, path):
        """Write the Invoice to PDF file"""

        if not self.invoice_file:
            return
        try:
            decoded_data = base64.b64decode(self.invoice_file)

            # Verify the content is a valid PDF
            if decoded_data[:5] != b'%PDF-':
                raise PazGasPowerError("Invoice Files is not a valid PDF")

            async with aiofiles.open('path', mode='w') as f:
                await f.write(decoded_data)
        except (base64.binascii.Error, UnicodeDecodeError) as e:
            raise PazGasPowerError("field invoice_file isn't a valid base64 encoding") from e
        except Exception as e:
            raise PazGasPowerError("Error saving PDF to file") from e


@dataclass
class CustomerData(DataClassDictMixin):
    """
    Represents customer data including contact information, account details, and invoices.

    Attributes:
        cellphone (str): The customer's cellphone number.
        package_id (str): The package ID associated with the customer.
        activation_date (date): The activation date of the customer's package.
        building_number (str): The building number in the customer's address.
        city_description (str): The city in the customer's address.
        customer_id (str): The customer's unique ID.
        email (str): The customer's email address.
        environment (str): The environment associated with the customer account.
        full_name (str): The full name of the customer.
        invoices (List[Invoice]): A list of invoices associated with the customer.
        is_onboarded (bool): Indicates if the customer has completed onboarding.
        need_to_order_smart_meter (bool): Indicates if the customer needs to order a smart meter.
        phone (str): The customer's primary phone number.
        status_code (str): The status code of the customer account.
        street_description (str): The street description in the customer's address.
        uuid (UUID): The unique identifier for the customer record.
    """

    cellphone: str = field(metadata=field_options(alias="Cellphone"))
    package_id: str = field(metadata=field_options(alias="PackageId"))
    activation_date: date = field(metadata=field_options(alias="activationDate"))
    building_number: str = field(metadata=field_options(alias="buildingNumber"))
    city_description: str = field(metadata=field_options(alias="cityDescription"))
    customer_id: str = field(metadata=field_options(alias="customerId"))
    email: str = field(metadata=field_options(alias="email"))
    environment: str = field(metadata=field_options(alias="environment"))
    full_name: str = field(metadata=field_options(alias="fullName"))
    invoices: List[Invoice] = field(metadata=field_options(alias="invoices"))
    is_onboarded: bool = field(metadata=field_options(alias="isOnboarded"))
    need_to_order_smart_meter: bool = field(metadata=field_options(alias="needToOrderSmartMeter"))
    phone: str = field(metadata=field_options(alias="phone"))
    status_code: str = field(metadata=field_options(alias="statusCode"))
    street_description: str = field(metadata=field_options(alias="streetDescription"))
    uuid: UUID = field(metadata=field_options(alias="uuid"))
    package: Optional[Package] = None

    def __post_init__(self):
        if isinstance(self.package_id, str) and self.package_id.isdigit():
            self.package = PACKAGES_MAP.get(int(self.package_id))
