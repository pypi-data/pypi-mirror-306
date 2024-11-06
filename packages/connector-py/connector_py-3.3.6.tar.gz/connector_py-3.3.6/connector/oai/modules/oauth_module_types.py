import typing as t
from enum import Enum

import pydantic

from connector.generated import CapabilityName
from connector.oai.capability import AuthRequest


class OAuthFlowType(str, Enum):
    CODE_FLOW = "CODE_FLOW"


class ClientAuthenticationMethod(str, Enum):
    CLIENT_SECRET_POST = "CLIENT_SECRET_POST"
    CLIENT_SECRET_BASIC = "CLIENT_SECRET_BASIC"


class RequestMethod(str, Enum):
    GET = "GET"
    POST = "POST"


class RequestDataType(str, Enum):
    FORMDATA = "FORMDATA"
    JSON = "JSON"
    QUERY = "QUERY"


class OAuthRequest(pydantic.BaseModel):
    method: RequestMethod = RequestMethod.POST
    data: RequestDataType = RequestDataType.FORMDATA


class OAuthCapabilities(pydantic.BaseModel):
    get_authorization_url: bool | None = True
    handle_authorization_callback: bool | None = True
    refresh_access_token: bool | None = True


class OAuthSettings(pydantic.BaseModel):
    authorization_url: str | t.Callable[[AuthRequest], str]
    token_url: str | t.Callable[[AuthRequest], str]
    scopes: dict[CapabilityName, str]
    flow_type: OAuthFlowType | None = OAuthFlowType.CODE_FLOW
    client_auth: ClientAuthenticationMethod | None = ClientAuthenticationMethod.CLIENT_SECRET_POST
    request_type: OAuthRequest | None = OAuthRequest()
    capabilities: OAuthCapabilities | None = OAuthCapabilities()
