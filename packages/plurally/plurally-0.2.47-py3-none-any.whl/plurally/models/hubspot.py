import enum
from datetime import datetime, timezone
from typing import Any, List, Union

import tenacity
from hubspot import HubSpot
from hubspot.crm.companies.models import (
    PublicAssociationsForObject as CompanyPublicAssociationsForObject,
)
from hubspot.crm.companies.models import (
    SimplePublicObjectInputForCreate as CompanySimplePublicObjectInputForCreate,
)
from hubspot.crm.contacts import (
    PublicAssociationsForObject as ContactPublicAssociationsForObject,
)
from hubspot.crm.contacts import PublicObjectSearchRequest
from hubspot.crm.contacts import (
    SimplePublicObjectInputForCreate as ContactSimplePublicObjectInputForCreate,
)
from hubspot.crm.objects import AssociationSpec
from loguru import logger
from pydantic import BaseModel, ConfigDict, Field, create_model, field_validator

from plurally.models import utils
from plurally.models.auto import Auto
from plurally.models.misc import Table
from plurally.models.node import Node

HUBSPOT_FILTERS_TYPE_FRIENDLY = "Hubspot Filters"


class HubspotCompanyCreate(Auto): ...


class HubspotCompanyRead(Auto):
    id: str


class HubspotContactCreate(Auto): ...


class HubspotContactRead(Auto):
    id: str


BASE_CLASSES = {
    "HubspotCompanyCreate": HubspotCompanyCreate,
    "HubspotCompanyRead": HubspotCompanyRead,
    "HubspotContactCreate": HubspotContactCreate,
    "HubspotContactRead": HubspotContactRead,
}


class HubspotOperator(enum.Enum):
    LT = "LT"
    LTE = "LTE"
    GT = "GT"
    GTE = "GTE"
    EQ = "EQ"
    NEQ = "NEQ"
    BETWEEN = "BETWEEN"
    IN = "IN"
    NOT_IN = "NOT_IN"
    HAS_PROPERTY = "HAS_PROPERTY"
    NOT_HAS_PROPERTY = "NOT_HAS_PROPERTY"
    CONTAINS_TOKEN = "CONTAINS_TOKEN"
    NOT_CONTAINS_TOKEN = "NOT_CONTAINS_TOKEN"


class HubspotFilter(BaseModel):
    model_config = ConfigDict(use_enum_values=True)
    propertyName: str
    operator: HubspotOperator
    value: Any


class HubspotFilterDict(BaseModel):
    filters: List[HubspotFilter]


class HubspotBase(Node):
    SCOPES = [
        "crm.objects.contacts.read",
        "crm.objects.contacts.write",
        "crm.objects.companies.read",
        "crm.objects.companies.write",
    ]
    ICON = "hubspot"

    def __init__(self, init_inputs: Node.InitSchema):
        super().__init__(init_inputs)
        assert self.SCOPES is not None, "SCOPES must be defined in the subclass"
        self._service = None
        self._token = None
        self._token_expiry = None

    def token(self):
        now = datetime.now(tz=timezone.utc).replace(tzinfo=None)
        if self._token is None or self._token_expiry < now:
            self.reset()
            self._token, self._token_expiry = utils.get_access_token(self.SCOPES)
        return self._token

    @property
    def service(self) -> HubSpot:
        if self._service is None:
            self._service = HubSpot(access_token=self.token())
        return self._service

    def reset(self):
        self._token = None
        self._token_expiry = None
        self._service = None


class HubspotCompaniesRead(HubspotBase):

    class InitSchema(Node.InitSchema):
        properties: str = Field(
            "name, domain, industry, description",
            title="Properties",
            description="The properties to fetch (comma separated).",
            json_schema_extra={
                "uiSchema": {
                    "ui:widget": "textarea",
                    "ui:placeholder": "Comma separated properties, for example: name, domain, industry, description",
                }
            },
        )
        limit: int = Field(
            100,
            title="Limit",
            description="The number of companies to fetch.",
            json_schema_extra={"advanced": True},
        )

    class OutputSchema(Node.OutputSchema):
        companies: Table = Field(...)

    class InputSchema(Node.InputSchema):
        filter_groups: List[HubspotFilterDict] = Field(
            [],
            title="Filters",
            description="The filters to apply in the search.",
            json_schema_extra={"type-friendly": HUBSPOT_FILTERS_TYPE_FRIENDLY},
        )

    def __init__(self, init_inputs: Node.InitSchema):
        self.limit = init_inputs.limit
        self.properties = init_inputs.properties
        super().__init__(init_inputs)

    def serialize(self):
        return super().serialize() | {
            "limit": self.limit,
            "properties": self.properties,
        }

    def forward(self, node_inputs: InputSchema):
        q = PublicObjectSearchRequest(
            properties=[s.strip() for s in self.properties.split(",")],
            filter_groups=node_inputs.model_dump()["filter_groups"],
            limit=self.limit,
        )
        companies = self.service.crm.companies.search_api.do_search(q)
        return [company.properties for company in companies.results]


class HubspotContactsRead(HubspotBase):

    class InitSchema(Node.InitSchema):
        properties: str = Field(
            "firstname, lastname, email, phone, company, jobtitle",
            title="Properties",
            description="The properties to fetch (comma separated).",
            json_schema_extra={
                "uiSchema": {
                    "ui:widget": "textarea",
                    "ui:placeholder": "Comma separated properties, for example: firstname, lastname, email, phone, company, jobtitle",
                }
            },
        )
        limit: int = Field(
            100,
            title="Limit",
            description="The number of contacts to fetch.",
            json_schema_extra={"advanced": True},
        )

    class OutputSchema(Node.OutputSchema):
        contacts: Table = Field(...)

    class InputSchema(Node.InputSchema):
        filter_groups: List[HubspotFilterDict] = Field(
            [],
            title="Filters",
            description="The filters to apply in the search.",
            json_schema_extra={"type-friendly": HUBSPOT_FILTERS_TYPE_FRIENDLY},
        )

    def __init__(self, init_inputs: Node.InitSchema):
        self.limit = init_inputs.limit
        self.properties = init_inputs.properties
        super().__init__(init_inputs)

    def serialize(self):
        return super().serialize() | {
            "limit": self.limit,
            "properties": self.properties,
        }

    def forward(self, node_inputs: InputSchema):
        q = PublicObjectSearchRequest(
            properties=[s.strip() for s in self.properties.split(",")],
            filter_groups=node_inputs.model_dump()["filter_groups"],
            limit=self.limit,
        )
        contacts = self.service.crm.contacts.search_api.do_search(q)
        return [contact.properties for contact in contacts.results]


class HubspotEntityCreateBuilder:

    @classmethod
    def build(
        cls,
        entity_name: str,
        unique_property_name: str,
        properties_default: str,
        api_name: str,
        entity_create_kls,
        entity_associations_kls,
        extra_props: dict = None,
    ):
        class HubspotEntityCreate(HubspotBase):
            ENTITY_NAME_TITLE = entity_name.title()
            CREATE_BASE_KLS = BASE_CLASSES[f"Hubspot{ENTITY_NAME_TITLE}Create"]
            READ_BASE_KLS = BASE_CLASSES[f"Hubspot{ENTITY_NAME_TITLE}Read"]

            class InitSchema(Node.InitSchema):
                __doc__ = f"""
Creates a HubSpot {entity_name.title()}.

This block requires you to connect your HubSpot account to Plurally.
                """
                properties: str = Field(
                    properties_default,
                    title="Properties",
                    description="The properties to assign (comma separated).",
                    json_schema_extra={
                        "uiSchema": {
                            "ui:widget": "textarea",
                            "ui:placeholder": f"Comma separated properties, for example: {properties_default}",
                        }
                    },
                )

                update_if_exists: bool = Field(
                    True,
                    title="Update if Exists",
                    description=f"If a {entity_name} with the same {unique_property_name} exists, update it.",
                    json_schema_extra={"advanced": True},
                )

                @field_validator("properties")
                def validate_properties(cls, v):
                    v = [s.strip().lower() for s in v.split(",")]
                    if unique_property_name not in v:
                        raise ValueError(
                            f"{unique_property_name} is required in properties for {entity_name}."
                        )
                    return ",".join(v)

            DESC = InitSchema.__doc__

            InputSchema = create_model(
                f"{ENTITY_NAME_TITLE}Input",
                **{
                    entity_name: (
                        CREATE_BASE_KLS,
                        Field(
                            ...,
                            title=f"Hubspot {ENTITY_NAME_TITLE}",
                            description=f"The {entity_name} to create or update.",
                            json_schema_extra={
                                "type-friendly": f"Hubspot {ENTITY_NAME_TITLE}",
                                "jit": True,
                            },
                        ),
                    ),
                    **(extra_props or {}),
                },
                __base__=Node.InputSchema,
            )

            OutputSchema = create_model(
                f"{ENTITY_NAME_TITLE}Input",
                **{
                    entity_name: (
                        READ_BASE_KLS,
                        Field(
                            ...,
                            title=f"Hubspot {ENTITY_NAME_TITLE}",
                            description=f"The {entity_name} that was created or updated.",
                            json_schema_extra={
                                "type-friendly": f"Hubspot {ENTITY_NAME_TITLE}",
                                "jit": True,
                            },
                        ),
                    )
                },
                __base__=Node.OutputSchema,
            )

            def __init__(self, init_inputs: Node.InitSchema):
                self._properties = init_inputs.properties
                self.update_if_exists = init_inputs.update_if_exists
                self.entity_name = entity_name
                super().__init__(init_inputs)

            @property
            def adapters(self):
                return super().adapters | {
                    entity_name: {
                        Association: get_entity_to_assoc(self.ENTITY_NAME_TITLE)
                    }
                }

            @property
            def properties(self):
                return self._properties

            @properties.setter
            def properties(self, value):
                self._properties = value
                self._set_schemas()

            def _get_input_props(self):
                EntityModel = create_model(
                    f"Hubspot{self.ENTITY_NAME_TITLE}",
                    **{
                        prop: (Union[str, None], Field(None, title=prop))
                        for prop in [s.strip() for s in self.properties.split(",")]
                    },
                    __base__=self.CREATE_BASE_KLS,
                )
                return {
                    self.entity_name: (
                        EntityModel,
                        Field(..., title=f"Hubspot {self.ENTITY_NAME_TITLE}"),
                    ),
                    **(extra_props or {}),
                }

            def _set_schemas(self):
                self.InputSchema = create_model(
                    f"{self.ENTITY_NAME_TITLE}Input",
                    **self._get_input_props(),
                    __base__=Node.InputSchema,
                )

                EntityModel = create_model(
                    f"Hubspot{self.ENTITY_NAME_TITLE}",
                    id=(str, Field(..., title="ID")),
                    **{
                        prop: (Union[str, None], Field(None, title=prop))
                        for prop in [s.strip() for s in self.properties.split(",")]
                    },
                    __base__=self.READ_BASE_KLS,
                )

                self.OutputSchema = create_model(
                    f"{self.ENTITY_NAME_TITLE}Output",
                    **{
                        self.entity_name: (
                            EntityModel,
                            Field(..., title=f"Hubspot {self.ENTITY_NAME_TITLE}"),
                        )
                    },
                    __base__=Node.OutputSchema,
                )

            def serialize(self):
                return super().serialize() | {
                    "properties": self._properties,
                    "update_if_exists": self.update_if_exists,
                }

            @property
            def basic_api(self):
                return getattr(self.service.crm, api_name).basic_api

            @property
            def search_api(self):
                return getattr(self.service.crm, api_name).search_api

            def get_existing(self, unique_property_value):
                search_results = self.search_api.do_search(
                    PublicObjectSearchRequest(
                        properties=[unique_property_name],
                        filter_groups=[
                            {
                                "filters": [
                                    {
                                        "propertyName": unique_property_name,
                                        "operator": "EQ",
                                        "value": unique_property_value,
                                    }
                                ]
                            }
                        ],
                        limit=1,
                    )
                )
                if search_results.total > 0:
                    logger.debug(f"{self.entity_name} already exists.")
                    return search_results.results[0]

            @tenacity.retry(
                wait=tenacity.wait_fixed(5),
                stop=tenacity.stop_after_attempt(3),
            )
            def forward(self, node_inputs):
                entity = getattr(node_inputs, self.entity_name)
                unique_property_value = getattr(entity, unique_property_name)
                properties = node_inputs.model_dump()[self.entity_name]
                associations = node_inputs.associations
                entity = self.get_existing(unique_property_value)
                if entity:
                    if self.update_if_exists:
                        logger.debug(f"Updating {self.entity_name} with id={entity.id}")
                        create_data = entity_create_kls(properties=properties)
                        entity = self.basic_api.update(entity.id, create_data)
                        if associations:
                            self.associate(int(entity.id), associations)
                            entity = self.get_existing(unique_property_value)
                    else:
                        # entity already exists not updating but not raising an error
                        pass
                else:
                    if associations:
                        associations = [
                            entity_associations_kls(**associations.model_dump())
                        ]
                        logger.debug(f"Associating with {associations}")
                    create_data = entity_create_kls(
                        properties=properties, associations=associations
                    )
                    entity = self.basic_api.create(create_data)

                self.outputs = self.OutputSchema(
                    **{self.entity_name: {**{"id": entity.id}, **entity.properties}}
                ).model_dump()

            def associate(self, entity_id, associations):
                # associations is a unique assoc for not
                # later might be a list, need to see
                # then the next line should be changed
                for association in [associations]:
                    # check if assoc exists
                    existing_assocs = (
                        self.service.crm.associations.v4.basic_api.get_page(
                            association.from_oject_type,
                            entity_id,
                            association.to_object_type,
                        )
                    )

                    if any(
                        existing_assoc.to_object_id == association.to.id
                        for existing_assoc in existing_assocs.results
                    ):
                        # assoc already exists, do nothing
                        ...
                    else:
                        for existing_assoc in existing_assocs.results:
                            self.service.crm.associations.v4.basic_api.archive(
                                association.from_oject_type,
                                entity_id,
                                association.to_object_type,
                                existing_assoc.to_object_id,
                            )

                        args = [
                            association.from_oject_type,
                            entity_id,
                            association.to_object_type,
                            association.to.id,
                            [
                                AssociationSpec(
                                    association.types[0].associationCategory,
                                    association.types[0].associationTypeId,
                                )
                            ],
                        ]
                        logger.debug(f"Associating with {associations}")
                        self.service.crm.associations.v4.basic_api.create(*args)

            def _get_cls_props(self):
                return {}

        return HubspotEntityCreate


class AssociationTo(BaseModel):
    id: int


class AssociationTypes(BaseModel):
    associationTypeId: int = Field()
    associationCategory: str = Field("HUBSPOT_DEFINED")


class Association(BaseModel):
    to: AssociationTo
    types: List[AssociationTypes]
    from_oject_type: str = Field(exclude=True)
    to_object_type: str = Field(exclude=True)


class HubspotContactToCompany(Node):

    ICON = "hubspot"

    class InitSchema(Node.InitSchema):
        """
        Create a HubSpot association between a contact and a company.
        """

    DESC = InitSchema.__doc__

    class InputSchema(Node.InputSchema):
        company: HubspotCompanyRead

    class OutputSchema(Node.OutputSchema):
        association: Association

    def forward(self, node_inputs: InputSchema):
        logger.debug(
            f"Creating association between contact and company with IDs: {node_inputs.company.id}"
        )
        self.outputs["association"] = Association(
            to=AssociationTo(id=node_inputs.company.id),
            types=[AssociationTypes(associationTypeId=279)],
            from_oject_type="contact",
            to_object_type="company",
        )


associations = {
    "associations": (Association, Field(None, title="Associations")),
}

_HubspotContactCreate = HubspotEntityCreateBuilder.build(
    "contact",
    "email",
    "email, firstname, lastname, phone, company, jobtitle",
    "contacts",
    ContactSimplePublicObjectInputForCreate,
    ContactPublicAssociationsForObject,
    associations,
)


class HubspotContactCreate(_HubspotContactCreate): ...


_HubspotCompanyCreate = HubspotEntityCreateBuilder.build(
    "company",
    "domain",
    "domain, name, industry, description",
    "companies",
    CompanySimplePublicObjectInputForCreate,
    CompanyPublicAssociationsForObject,
    associations,
)


class HubspotCompanyCreate(_HubspotCompanyCreate): ...


ASSOCS = {
    "HubspotContactToCompany": HubspotContactToCompany,
}


def get_entity_to_assoc(entity_name_title: str):
    def entity_to_assoc(src_node, tgt_node, src_handle):
        kls_name = f"Hubspot{tgt_node.ENTITY_NAME_TITLE}To{entity_name_title}"
        kls = ASSOCS.get(kls_name)
        if not kls:
            raise ValueError(f"Association {kls_name} not found.")
        nodes = [
            kls(
                kls.InitSchema(
                    name=f"Assoc. {tgt_node.ENTITY_NAME_TITLE} To {entity_name_title}",
                    pos_x=(src_node.pos_x + tgt_node.pos_x) / 2,
                    pos_y=(src_node.pos_y + tgt_node.pos_y) / 2,
                )
            )
        ]
        connections = [
            (0, src_handle, 1, src_node.entity_name),
            (1, "association", 2, None),
        ]
        return nodes, connections

    return entity_to_assoc
