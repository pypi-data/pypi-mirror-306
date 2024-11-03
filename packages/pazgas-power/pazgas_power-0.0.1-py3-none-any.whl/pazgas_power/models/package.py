"""Package model module."""

from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Optional

from mashumaro import DataClassDictMixin, field_options


@dataclass
class BenefitContent(DataClassDictMixin):
    """
    Represents a benefit content item within a package.

    Attributes:
        benefit_value (str): The value or description of the benefit.
    """

    benefit_value: str = field(metadata=field_options(alias="benefitValue"))


@dataclass
class PersonalAreaBenefit(DataClassDictMixin):
    """
    Represents a personal area benefit containing benefit content.

    Attributes:
        content (BenefitContent): The content of the benefit.
    """

    content: BenefitContent = field(metadata=field_options(alias="content"))


@dataclass
class Package(DataClassDictMixin):
    """
    Represents a package with various attributes and benefits.

    Attributes:
        url (str): The URL of the package.
        name (str): The name of the package.
        title (str): The title of the package.
        typename (str): The GraphQL typename of the package.
        description (str): The description of the package.
        image (Optional[str]): The URL to an image for the package, if any.
        alt_text_for_image (str): Alternative text for the image.
        active_from_date (datetime): The start date of package activity.
        active_to_date (datetime): The end date of package activity.
        identify (str): The identifier of the package.
        package_theme (str): The theme of the package.
        package_status (bool): Whether the package is active.
        recommended_package (bool): Whether the package is recommended.
        recommended_text (str): Text displayed if the package is recommended.
        currency (str): The currency used in discounts, if applicable.
        discount_value (str): The discount value of the package.
        discount_text (str): The discount text for the package.
        note_text (str): Additional notes about the package.
        package_button_text (str): The button text for package action.
        add_checkmark_to_list (bool): Whether to add a checkmark to the list.
        hide_data_string (bool): Whether to hide the data string.
        data_text (str): Text about the package data.
        personal_area_benefits (List[PersonalAreaBenefit]): List of personal area benefits.
    """

    url: str = field(metadata=field_options(alias="url"))
    name: str = field(metadata=field_options(alias="name"))
    title: str = field(metadata=field_options(alias="title"))
    typename: str = field(metadata=field_options(alias="__typename"))
    description: str = field(metadata=field_options(alias="description"))
    image: Optional[str] = field(metadata=field_options(alias="image"))
    alt_text_for_image: str = field(metadata=field_options(alias="altTextForImage"))
    active_from_date: datetime = field(metadata=field_options(alias="activeFromDate"))
    active_to_date: datetime = field(metadata=field_options(alias="activeToDate"))
    identify: str = field(metadata=field_options(alias="identify"))
    package_theme: str = field(metadata=field_options(alias="packageTheme"))
    package_status: bool = field(metadata=field_options(alias="packageStatus"))
    recommended_package: bool = field(metadata=field_options(alias="recommendedPackage"))
    recommended_text: str = field(metadata=field_options(alias="recommendedText"))
    currency: str = field(metadata=field_options(alias="currency"))
    discount_value: str = field(metadata=field_options(alias="discountValue"))
    discount_text: str = field(metadata=field_options(alias="discountText"))
    note_text: str = field(metadata=field_options(alias="noteText"))
    package_button_text: str = field(metadata=field_options(alias="packageButtonText"))
    add_checkmark_to_list: bool = field(metadata=field_options(alias="addCheckmarkToList"))
    hide_data_string: bool = field(metadata=field_options(alias="hideDataString"))
    data_text: str = field(metadata=field_options(alias="dataText"))
    personal_area_benefits: List[PersonalAreaBenefit] = field(metadata=field_options(alias="personalAreaBenefits"))
