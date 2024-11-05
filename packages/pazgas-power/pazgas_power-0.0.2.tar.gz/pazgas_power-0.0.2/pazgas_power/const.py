"""Constants for the PazGas Power API."""

import json

from pazgas_power.models.package import Package

APIM_URL = "https://personalarea.pazgas.co.il/api/hashmal/apim"
SEND_OTP_PATH = "LoginPersonalArea/a2prod/SendOtp"
VERIFY_OTP_PATH = "PersonalArea/a2prod/VerifyOtp"

# Taken from https://personalarea.pazgas.co.il/tracker
PACKAGES_JSON = """
[
    {
        "url":"/packages/package-חבילות-דיפולט/",
        "name":"Package חבילות דיפולט",
        "title":"דיפולט",
        "__typename":"PackageType",
        "description":"",
        "image":null,
        "altTextForImage":"",
        "activeFromDate":"2023-10-09T12:00:00Z",
        "activeToDate":"2023-10-31T12:00:00Z",
        "identify":"",
        "packageTheme":"light-blue",
        "packageStatus":false,
        "recommendedPackage":false,
        "recommendedText":"",
        "currency":"",
        "discountValue":"",
        "discountText":"",
        "noteText":"",
        "packageButtonText":"",
        "addCheckmarkToList":false,
        "hideDataString":false,
        "dataText":"החבילה פעילה החל מ - ",
        "personalAreaBenefits":[
            {
            "content":{
                "benefitValue":"עקב עבודות תשתית לשדרוג האתר לא ניתן לטעון את המידע כעת"
            }
            },
            {
            "content":{
                "benefitValue":"אנו מצפים לפתור את התקלה בהקדם"
            }
            },
            {
            "content":{
                "benefitValue":"עמך הסליחה"
            }
            }
        ]
    },
    {
        "url":"/packages/package-לילה-חינם/",
        "name":"Package לילה חינם",
        "title":"לילה חינם",
        "__typename":"PackageType",
        "description":"מסלול לילה בו תינתן הנחה של 100% על תעריף הצריכה בימים א'-ה' בין חצות ועד 7 בבוקר למחרת למשך 3 חודשים ולאחר מכן 15% הנחה בלילה",
        "image":null,
        "altTextForImage":"",
        "activeFromDate":"2023-12-17T12:00:00Z",
        "activeToDate":"2024-01-31T12:00:00Z",
        "identify":"880248",
        "packageTheme":"dark-blue",
        "packageStatus":true,
        "recommendedPackage":true,
        "recommendedText":"מומלץ!",
        "currency":"",
        "discountValue":"0",
        "discountText":"₪ בלילה!",
        "noteText":"",
        "packageButtonText":"להצטרפות",
        "addCheckmarkToList":true,
        "hideDataString":false,
        "dataText":"החבילה פעילה החל מ - ",
        "personalAreaBenefits":[
            {
            "content":{
                "benefitValue":"מסלול לילה בו תינתן הנחה של 100% על תעריף הצריכה."
            }
            },
            {
            "content":{
                "benefitValue":"בימים א'-ה' בין חצות ועד 7 בבוקר למחרת "
            }
            },
            {
            "content":{
                "benefitValue":"למשך 3 חודשים מיום ההצטרפות"
            }
            },
            {
            "content":{
                "benefitValue":"לאחר מכן ממשיכים לחסוך עם 15% הנחה על הצריכה בשעות המסלול"
            }
            }
        ]
    },
    {
        "url":"/packages/package-סופ-ש-מוזל/",
        "name":"Package סוף שבוע מוזל",
        "title":"סוף שבוע מוזל",
        "__typename":"PackageType",
        "description":"מסלול סוף שבוע בו תינתן הנחה של 10% הנחה על הצריכה בימים ו'-ש׳ מיום חמישי ב00:00 ועד למוצאי שבת ב – 00:00.",
        "image":null,
        "altTextForImage":"",
        "activeFromDate":"2023-11-07T12:00:00Z",
        "activeToDate":"2023-11-22T12:00:00Z",
        "identify":"880237",
        "packageTheme":"green",
        "packageStatus":true,
        "recommendedPackage":false,
        "recommendedText":"",
        "currency":"%",
        "discountValue":"10",
        "discountText":"הנחה בסוף שבוע",
        "noteText":"",
        "packageButtonText":"להצטרפות",
        "addCheckmarkToList":true,
        "hideDataString":false,
        "dataText":"החבילה פעילה החל מ - ",
        "personalAreaBenefits":[
            {
            "content":{
                "benefitValue":"מסלול סוף שבוע בו תינתן הנחה של 10% הנחה על הצריכה"
            }
            },
            {
            "content":{
                "benefitValue":"בימים ו'-ש׳ מיום חמישי ב00:00 ועד למוצאי שבת ב – 00:00"
            }
            }
        ]
    },
    {
        "url":"/packages/package-24-7-קבוע/",
        "name":"Package 24/7 קבוע",
        "title":"24/7 קבוע",
        "__typename":"PackageType",
        "description":"מסלול 24/7 בו תינתן הנחה של 6% הנחה על כל הצריכה בחשבונית 24/7.",
        "image":null,
        "altTextForImage":"",
        "activeFromDate":"2023-10-01T12:00:00Z",
        "activeToDate":"2023-11-02T12:00:00Z",
        "identify":"880245",
        "packageTheme":"teal",
        "packageStatus":true,
        "recommendedPackage":false,
        "recommendedText":"",
        "currency":"%",
        "discountValue":"6",
        "discountText":" הנחה 24/7",
        "noteText":"",
        "packageButtonText":"להצטרפות",
        "addCheckmarkToList":true,
        "hideDataString":false,
        "dataText":"החבילה פעילה החל מ - ",
        "personalAreaBenefits":[
            {
            "content":{
                "benefitValue":"מסלול 24/7 קבוע בו תינתן הנחה של 6% על כל הצריכה בחשבונית 24/7."
            }
            }
        ]
    },
    {
        "url":"/packages/package-יום-מוזל/",
        "name":"package יום מוזל",
        "title":"יום מוזל",
        "__typename":"PackageType",
        "description":"מסלול יום בו תינתן הנחה של 15% על הצריכה בימים א-ה' בין השעות  8:00 בבוקר ועד 16:00 אחר הצהריים.",
        "image":null,
        "altTextForImage":"",
        "activeFromDate":"2023-10-10T12:00:00Z",
        "activeToDate":"0001-01-01T00:00:00Z",
        "identify":"880238",
        "packageTheme":"light-blue",
        "packageStatus":true,
        "recommendedPackage":false,
        "recommendedText":"",
        "currency":"%",
        "discountValue":"15",
        "discountText":"הנחה ביום",
        "noteText":"",
        "packageButtonText":"להצטרפות",
        "addCheckmarkToList":true,
        "hideDataString":false,
        "dataText":"החבילה פעילה החל מ - ",
        "personalAreaBenefits":[
            {
            "content":{
                "benefitValue":"15% הנחה על תעריף הצריכה בימים א'-ה'"
            }
            },
            {
            "content":{
                "benefitValue":"בין השעות 8:00 בבוקר ועד 16:00 אחר הצהריים"
            }
            }
        ]
    },
    {
        "url":"/packages/package-לילה-מוזל/",
        "name":"Package לילה מוזל",
        "title":"15% הנחה בלילה (אמצע שבוע)",
        "__typename":"PackageType",
        "description":" חשמל מסלול לילה –מעניק 15%  א'-ה' 00:00-07:00 (מתחיל בלילה שבין ראשון לשני– הלילה שבין חמישי לשישי)",
        "image":null,
        "altTextForImage":"",
        "activeFromDate":"2023-10-05T12:00:00Z",
        "activeToDate":"0001-01-01T00:00:00Z",
        "identify":"880239",
        "packageTheme":"light-blue",
        "packageStatus":true,
        "recommendedPackage":false,
        "recommendedText":"",
        "currency":"%",
        "discountValue":"15",
        "discountText":"הנחה בלילה",
        "noteText":"",
        "packageButtonText":"להצטרפות",
        "addCheckmarkToList":true,
        "hideDataString":false,
        "dataText":"החבילה פעילה החל מ - ",
        "personalAreaBenefits":[
            {
            "content":{
                "benefitValue":"15% הנחה על תעריף הצריכה בימים א'-ה'"
            }
            },
            {
            "content":{
                "benefitValue":"בין חצות ועד 07:00 בבוקר למחרת"
            }
            }
        ]
    },
    {
        "url":"/packages/package-7-הנחה-קבועה/",
        "name":"Package 7% הנחה קבועה",
        "title":"24/7 קבוע",
        "__typename":"PackageType",
        "description":"מסלול 24/7 בו תינתן הנחה של 7% הנחה על כל הצריכה בחשבונית 24/7.",
        "image":null,
        "altTextForImage":"",
        "activeFromDate":"2024-03-01T12:00:00Z",
        "activeToDate":"2024-05-31T12:00:00Z",
        "identify":"880251",
        "packageTheme":"dark-blue",
        "packageStatus":true,
        "recommendedPackage":true,
        "recommendedText":"מומלץ!",
        "currency":"%",
        "discountValue":"7",
        "discountText":" הנחה 24/7",
        "noteText":"",
        "packageButtonText":"להצטרפות",
        "addCheckmarkToList":true,
        "hideDataString":false,
        "dataText":"החבילה פעילה החל מ - ",
        "personalAreaBenefits":[
            {
            "content":{
                "benefitValue":"מסלול 24/7 קבוע בו תינתן הנחה של 7% על כל הצריכה בחשבונית 24/7."
            }
            }
        ]
    },
    {
        "url":"/packages/package-7-הנחה-קבועה-1/",
        "name":"Package 7% הנחה קבועה (1)",
        "title":"24/7 קבוע",
        "__typename":"PackageType",
        "description":"מסלול 24/7 בו תינתן הנחה של 7% הנחה על כל הצריכה בחשבונית 24/7.",
        "image":null,
        "altTextForImage":"",
        "activeFromDate":"2024-03-01T12:00:00Z",
        "activeToDate":"2024-05-31T12:00:00Z",
        "identify":"770081",
        "packageTheme":"dark-blue",
        "packageStatus":true,
        "recommendedPackage":true,
        "recommendedText":"מומלץ!",
        "currency":"%",
        "discountValue":"7",
        "discountText":" הנחה 24/7",
        "noteText":"",
        "packageButtonText":"להצטרפות",
        "addCheckmarkToList":false,
        "hideDataString":false,
        "dataText":"החבילה פעילה החל מ - ",
        "personalAreaBenefits":[
            {
            "content":{
                "benefitValue":"מסלול 24/7 קבוע בו תינתן הנחה של 7% על כל הצריכה בחשבונית 24/7."
            }
            }
        ]
    },
    {
        "url":"/packages/yellow/",
        "name":"yellow",
        "title":"",
        "__typename":"PackageType",
        "description":"",
        "image":null,
        "altTextForImage":"",
        "activeFromDate":"0001-01-01T00:00:00Z",
        "activeToDate":"0001-01-01T00:00:00Z",
        "identify":"880253",
        "packageTheme":"yellow",
        "packageStatus":false,
        "recommendedPackage":false,
        "recommendedText":"",
        "currency":"",
        "discountValue":"",
        "discountText":"",
        "noteText":"",
        "packageButtonText":"",
        "addCheckmarkToList":true,
        "hideDataString":false,
        "dataText":"החבילה פעילה החל מ - ",
        "personalAreaBenefits":[
            {
            "content":{
                "benefitValue":"מסלול צבירה ב- yellow מקנה הטבה של עד 10% מתעריף הצריכה של החשמל בלבד (ללא צבירה בדמי השימוש הקבועים) בחשבונית בכל שעות היממה 24/7."
            }
            }
        ]
    },
    {
        "url":"/packages/5-הנחה-קבועה/",
        "name":"5% הנחה קבועה",
        "title":"5% הנחה קבועה",
        "__typename":"PackageType",
        "description":"",
        "image":null,
        "altTextForImage":"",
        "activeFromDate":"0001-01-01T00:00:00Z",
        "activeToDate":"0001-01-01T00:00:00Z",
        "identify":"880236",
        "packageTheme":"dark-blue",
        "packageStatus":false,
        "recommendedPackage":false,
        "recommendedText":"",
        "currency":"",
        "discountValue":"",
        "discountText":"",
        "noteText":"",
        "packageButtonText":"",
        "addCheckmarkToList":false,
        "hideDataString":false,
        "dataText":"החבילה פעילה החל מ - ",
        "personalAreaBenefits":[
            {
            "content":{
                "benefitValue":"מסלול הנחה קבועה בו תינתן הנחה של 5% על כל צריכת החשמל בחשבונית 24/7. (ללא הנחה בדמי השימוש הקבועים)"
            }
            }
        ]
    },
    {
        "url":"/packages/חודשיים-חשמל-חינם-בלילה/",
        "name":"חודשיים חשמל חינם בלילה",
        "title":"חודשיים חשמל חינם בלילה",
        "__typename":"PackageType",
        "description":"",
        "image":null,
        "altTextForImage":"",
        "activeFromDate":"0001-01-01T00:00:00Z",
        "activeToDate":"0001-01-01T00:00:00Z",
        "identify":"770079",
        "packageTheme":"dark-blue",
        "packageStatus":false,
        "recommendedPackage":false,
        "recommendedText":"",
        "currency":"",
        "discountValue":"",
        "discountText":"",
        "noteText":"",
        "packageButtonText":"",
        "addCheckmarkToList":false,
        "hideDataString":false,
        "dataText":"החבילה פעילה החל מ - ",
        "personalAreaBenefits":[
            {
            "content":{
                "benefitValue":"מסלול לילה בו תינתן הנחה של 100% על תעריף הצריכה בימים א'-ש' בין 23:00 ועד 7 בבוקר למחרת למשך חודשיים מיום ההצטרפות. לאחר מכן ממשיכים לחסוך עם 15% הנחה על הצריכה בשעות המסלול."
            }
            }
        ]
    },
    {
        "url":"/packages/15-הנחה-בלילה-כל-השבוע/",
        "name":"15% הנחה בלילה (כל השבוע)",
        "title":"15% הנחה בלילה",
        "__typename":"PackageType",
        "description":"",
        "image":null,
        "altTextForImage":"",
        "activeFromDate":"0001-01-01T00:00:00Z",
        "activeToDate":"0001-01-01T00:00:00Z",
        "identify":"880246",
        "packageTheme":"dark-blue",
        "packageStatus":false,
        "recommendedPackage":false,
        "recommendedText":"",
        "currency":"",
        "discountValue":"",
        "discountText":"",
        "noteText":"",
        "packageButtonText":"",
        "addCheckmarkToList":true,
        "hideDataString":false,
        "dataText":"החבילה פעילה החל מ - ",
        "personalAreaBenefits":[
            {
            "content":{
                "benefitValue":"15% הנחה על תעריף הצריכה בימים א'-ש'"
            }
            },
            {
            "content":{
                "benefitValue":"בין 23:00 ועד 07:00 בבוקר למחרת"
            }
            }
        ]
    },
    {
        "url":"/packages/15-הנחה-ביום-כל-השבוע/",
        "name":"15% הנחה ביום (כל השבוע)",
        "title":"15% הנחה ביום",
        "__typename":"PackageType",
        "description":"",
        "image":null,
        "altTextForImage":"",
        "activeFromDate":"0001-01-01T00:00:00Z",
        "activeToDate":"0001-01-01T00:00:00Z",
        "identify":"880247",
        "packageTheme":"dark-blue",
        "packageStatus":false,
        "recommendedPackage":false,
        "recommendedText":"",
        "currency":"",
        "discountValue":"",
        "discountText":"",
        "noteText":"",
        "packageButtonText":"",
        "addCheckmarkToList":true,
        "hideDataString":false,
        "dataText":"החבילה פעילה החל מ - ",
        "personalAreaBenefits":[
            {
            "content":{
                "benefitValue":"15% הנחה על תעריף הצריכה בימים א'-ש'"
            }
            },
            {
            "content":{
                "benefitValue":"בין השעות 8:00 בבוקר ועד 16:00 אחר הצהריים"
            }
            }
        ]
    }
]
"""  # noqa: E501

# Parse JSON


# Create a constant list of packages
PACKAGES = [Package.from_dict(package_json) for package_json in json.loads(PACKAGES_JSON)]
PACKAGES_MAP = {package.identify: package for package in PACKAGES}
