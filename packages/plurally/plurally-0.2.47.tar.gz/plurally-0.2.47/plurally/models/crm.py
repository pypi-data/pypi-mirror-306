from plurally.models.hubspot import (
    HubspotCompanyCreate,
    HubspotContactCreate,
    HubspotContactsRead,
    HubspotContactToCompany,
)
from plurally.models.source.constant import Text


class SalesForce(Text):
    ICON = "salesforce"


__all__ = [
    "HubspotContactsRead",
    "HubspotContactCreate",
    "HubspotCompanyCreate",
    "HubspotContactToCompany",
    "SalesForce",
]
