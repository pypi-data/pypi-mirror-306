"""
This type stub file was generated by pyright.
"""

from saml2 import SamlBase, saml

NAMESPACE = ...
STATUS_SUCCESS = ...
STATUS_REQUESTER = ...
STATUS_RESPONDER = ...
STATUS_VERSION_MISMATCH = ...
STATUS_AUTHN_FAILED = ...
STATUS_INVALID_ATTR_NAME_OR_VALUE = ...
STATUS_INVALID_NAMEID_POLICY = ...
STATUS_NO_AUTHN_CONTEXT = ...
STATUS_NO_AVAILABLE_IDP = ...
STATUS_NO_PASSIVE = ...
STATUS_NO_SUPPORTED_IDP = ...
STATUS_PARTIAL_LOGOUT = ...
STATUS_PROXY_COUNT_EXCEEDED = ...
STATUS_REQUEST_DENIED = ...
STATUS_REQUEST_UNSUPPORTED = ...
STATUS_REQUEST_VERSION_DEPRECATED = ...
STATUS_REQUEST_VERSION_TOO_HIGH = ...
STATUS_REQUEST_VERSION_TOO_LOW = ...
STATUS_RESOURCE_NOT_RECOGNIZED = ...
STATUS_TOO_MANY_RESPONSES = ...
STATUS_UNKNOWN_ATTR_PROFILE = ...
STATUS_UNKNOWN_PRINCIPAL = ...
STATUS_UNSUPPORTED_BINDING = ...
class ExtensionsType_(SamlBase):
    """The urn:oasis:names:tc:SAML:2.0:protocol:ExtensionsType element"""
    c_tag = ...
    c_namespace = ...
    c_children = ...
    c_attributes = ...
    c_child_order = ...
    c_cardinality = ...


def extensions_type__from_string(xml_string): # -> None:
    ...

class StatusMessage(SamlBase):
    """The urn:oasis:names:tc:SAML:2.0:protocol:StatusMessage element"""
    c_tag = ...
    c_namespace = ...
    c_value_type = ...
    c_children = ...
    c_attributes = ...
    c_child_order = ...
    c_cardinality = ...


def status_message_from_string(xml_string): # -> None:
    ...

class StatusDetailType_(SamlBase):
    """The urn:oasis:names:tc:SAML:2.0:protocol:StatusDetailType element"""
    c_tag = ...
    c_namespace = ...
    c_children = ...
    c_attributes = ...
    c_child_order = ...
    c_cardinality = ...
    c_any = ...


def status_detail_type__from_string(xml_string): # -> None:
    ...

class AuthnContextComparisonType_(SamlBase):
    """The urn:oasis:names:tc:SAML:2.0:protocol:AuthnContextComparisonType
    element"""
    c_tag = ...
    c_namespace = ...
    c_value_type = ...
    c_children = ...
    c_attributes = ...
    c_child_order = ...
    c_cardinality = ...


def authn_context_comparison_type__from_string(xml_string): # -> None:
    ...

class NameIDPolicyType_(SamlBase):
    """The urn:oasis:names:tc:SAML:2.0:protocol:NameIDPolicyType element"""
    c_tag = ...
    c_namespace = ...
    c_children = ...
    c_attributes = ...
    c_child_order = ...
    c_cardinality = ...
    def __init__(self, format=..., sp_name_qualifier=..., allow_create=..., text=..., extension_elements=..., extension_attributes=...) -> None:
        ...
    


def name_id_policy_type__from_string(xml_string): # -> None:
    ...

class RequesterID(SamlBase):
    """The urn:oasis:names:tc:SAML:2.0:protocol:RequesterID element"""
    c_tag = ...
    c_namespace = ...
    c_value_type = ...
    c_children = ...
    c_attributes = ...
    c_child_order = ...
    c_cardinality = ...


def requester_id_from_string(xml_string): # -> None:
    ...

class IDPEntryType_(SamlBase):
    """The urn:oasis:names:tc:SAML:2.0:protocol:IDPEntryType element"""
    c_tag = ...
    c_namespace = ...
    c_children = ...
    c_attributes = ...
    c_child_order = ...
    c_cardinality = ...
    def __init__(self, provider_id=..., name=..., loc=..., text=..., extension_elements=..., extension_attributes=...) -> None:
        ...
    


def idp_entry_type__from_string(xml_string): # -> None:
    ...

class GetComplete(SamlBase):
    """The urn:oasis:names:tc:SAML:2.0:protocol:GetComplete element"""
    c_tag = ...
    c_namespace = ...
    c_value_type = ...
    c_children = ...
    c_attributes = ...
    c_child_order = ...
    c_cardinality = ...


def get_complete_from_string(xml_string): # -> None:
    ...

class Artifact(SamlBase):
    """The urn:oasis:names:tc:SAML:2.0:protocol:Artifact element"""
    c_tag = ...
    c_namespace = ...
    c_value_type = ...
    c_children = ...
    c_attributes = ...
    c_child_order = ...
    c_cardinality = ...


def artifact_from_string(xml_string): # -> None:
    ...

class NewID(SamlBase):
    """The urn:oasis:names:tc:SAML:2.0:protocol:NewID element"""
    c_tag = ...
    c_namespace = ...
    c_value_type = ...
    c_children = ...
    c_attributes = ...
    c_child_order = ...
    c_cardinality = ...


def new_id_from_string(xml_string): # -> None:
    ...

class NewEncryptedID(saml.EncryptedElementType_):
    """The urn:oasis:names:tc:SAML:2.0:protocol:NewEncryptedID element"""
    c_tag = ...
    c_namespace = ...
    c_children = ...
    c_attributes = ...
    c_child_order = ...
    c_cardinality = ...


def new_encrypted_id_from_string(xml_string): # -> None:
    ...

class TerminateType_(SamlBase):
    """The urn:oasis:names:tc:SAML:2.0:protocol:TerminateType element"""
    c_tag = ...
    c_namespace = ...
    c_children = ...
    c_attributes = ...
    c_child_order = ...
    c_cardinality = ...


def terminate_type__from_string(xml_string): # -> None:
    ...

class SessionIndex(SamlBase):
    """The urn:oasis:names:tc:SAML:2.0:protocol:SessionIndex element"""
    c_tag = ...
    c_namespace = ...
    c_value_type = ...
    c_children = ...
    c_attributes = ...
    c_child_order = ...
    c_cardinality = ...


def session_index_from_string(xml_string): # -> None:
    ...

class Extensions(ExtensionsType_):
    """The urn:oasis:names:tc:SAML:2.0:protocol:Extensions element"""
    c_tag = ...
    c_namespace = ...
    c_children = ...
    c_attributes = ...
    c_child_order = ...
    c_cardinality = ...


def extensions_from_string(xml_string): # -> None:
    ...

class StatusDetail(StatusDetailType_):
    """The urn:oasis:names:tc:SAML:2.0:protocol:StatusDetail element"""
    c_tag = ...
    c_namespace = ...
    c_children = ...
    c_attributes = ...
    c_child_order = ...
    c_cardinality = ...


def status_detail_from_string(xml_string): # -> None:
    ...

class RequestAbstractType_(SamlBase):
    """The urn:oasis:names:tc:SAML:2.0:protocol:RequestAbstractType element"""
    c_tag = ...
    c_namespace = ...
    c_children = ...
    c_attributes = ...
    c_child_order = ...
    c_cardinality = ...
    def __init__(self, issuer=..., signature=..., extensions=..., id=..., version=..., issue_instant=..., destination=..., consent=..., text=..., extension_elements=..., extension_attributes=...) -> None:
        ...
    


class AssertionIDRequestType_(RequestAbstractType_):
    """
    The urn:oasis:names:tc:SAML:2.0:protocol:AssertionIDRequestType element
    """
    c_tag = ...
    c_namespace = ...
    c_children = ...
    c_attributes = ...
    c_child_order = ...
    c_cardinality = ...
    def __init__(self, assertion_id_ref=..., issuer=..., signature=..., extensions=..., id=..., version=..., issue_instant=..., destination=..., consent=..., text=..., extension_elements=..., extension_attributes=...) -> None:
        ...
    


def assertion_id_request_type__from_string(xml_string): # -> None:
    ...

class SubjectQueryAbstractType_(RequestAbstractType_):
    """
    The urn:oasis:names:tc:SAML:2.0:protocol:SubjectQueryAbstractType element
    """
    c_tag = ...
    c_namespace = ...
    c_children = ...
    c_attributes = ...
    c_child_order = ...
    c_cardinality = ...
    def __init__(self, subject=..., issuer=..., signature=..., extensions=..., id=..., version=..., issue_instant=..., destination=..., consent=..., text=..., extension_elements=..., extension_attributes=...) -> None:
        ...
    


class RequestedAuthnContextType_(SamlBase):
    """The urn:oasis:names:tc:SAML:2.0:protocol:RequestedAuthnContextType
    element"""
    c_tag = ...
    c_namespace = ...
    c_children = ...
    c_attributes = ...
    c_child_order = ...
    c_cardinality = ...
    def __init__(self, authn_context_class_ref=..., authn_context_decl_ref=..., comparison=..., text=..., extension_elements=..., extension_attributes=...) -> None:
        ...
    


def requested_authn_context_type__from_string(xml_string): # -> None:
    ...

class AttributeQueryType_(SubjectQueryAbstractType_):
    """The urn:oasis:names:tc:SAML:2.0:protocol:AttributeQueryType element"""
    c_tag = ...
    c_namespace = ...
    c_children = ...
    c_attributes = ...
    c_child_order = ...
    c_cardinality = ...
    def __init__(self, attribute=..., subject=..., issuer=..., signature=..., extensions=..., id=..., version=..., issue_instant=..., destination=..., consent=..., text=..., extension_elements=..., extension_attributes=...) -> None:
        ...
    


def attribute_query_type__from_string(xml_string): # -> None:
    ...

class AuthzDecisionQueryType_(SubjectQueryAbstractType_):
    """The urn:oasis:names:tc:SAML:2.0:protocol:AuthzDecisionQueryType
    element"""
    c_tag = ...
    c_namespace = ...
    c_children = ...
    c_attributes = ...
    c_child_order = ...
    c_cardinality = ...
    def __init__(self, action=..., evidence=..., resource=..., subject=..., issuer=..., signature=..., extensions=..., id=..., version=..., issue_instant=..., destination=..., consent=..., text=..., extension_elements=..., extension_attributes=...) -> None:
        ...
    


def authz_decision_query_type__from_string(xml_string): # -> None:
    ...

class NameIDPolicy(NameIDPolicyType_):
    """The urn:oasis:names:tc:SAML:2.0:protocol:NameIDPolicy element"""
    c_tag = ...
    c_namespace = ...
    c_children = ...
    c_attributes = ...
    c_child_order = ...
    c_cardinality = ...


def name_id_policy_from_string(xml_string): # -> None:
    ...

class IDPEntry(IDPEntryType_):
    """The urn:oasis:names:tc:SAML:2.0:protocol:IDPEntry element"""
    c_tag = ...
    c_namespace = ...
    c_children = ...
    c_attributes = ...
    c_child_order = ...
    c_cardinality = ...


def idp_entry_from_string(xml_string): # -> None:
    ...

class ArtifactResolveType_(RequestAbstractType_):
    """The urn:oasis:names:tc:SAML:2.0:protocol:ArtifactResolveType element"""
    c_tag = ...
    c_namespace = ...
    c_children = ...
    c_attributes = ...
    c_child_order = ...
    c_cardinality = ...
    def __init__(self, artifact=..., issuer=..., signature=..., extensions=..., id=..., version=..., issue_instant=..., destination=..., consent=..., text=..., extension_elements=..., extension_attributes=...) -> None:
        ...
    


def artifact_resolve_type__from_string(xml_string): # -> None:
    ...

class Terminate(TerminateType_):
    """The urn:oasis:names:tc:SAML:2.0:protocol:Terminate element"""
    c_tag = ...
    c_namespace = ...
    c_children = ...
    c_attributes = ...
    c_child_order = ...
    c_cardinality = ...


def terminate_from_string(xml_string): # -> None:
    ...

class LogoutRequestType_(RequestAbstractType_):
    """The urn:oasis:names:tc:SAML:2.0:protocol:LogoutRequestType element"""
    c_tag = ...
    c_namespace = ...
    c_children = ...
    c_attributes = ...
    c_child_order = ...
    c_cardinality = ...
    def __init__(self, base_id=..., name_id=..., encrypted_id=..., session_index=..., reason=..., not_on_or_after=..., issuer=..., signature=..., extensions=..., id=..., version=..., issue_instant=..., destination=..., consent=..., text=..., extension_elements=..., extension_attributes=...) -> None:
        ...
    


def logout_request_type__from_string(xml_string): # -> None:
    ...

class NameIDMappingRequestType_(RequestAbstractType_):
    """The urn:oasis:names:tc:SAML:2.0:protocol:NameIDMappingRequestType
    element"""
    c_tag = ...
    c_namespace = ...
    c_children = ...
    c_attributes = ...
    c_child_order = ...
    c_cardinality = ...
    def __init__(self, base_id=..., name_id=..., encrypted_id=..., name_id_policy=..., issuer=..., signature=..., extensions=..., id=..., version=..., issue_instant=..., destination=..., consent=..., text=..., extension_elements=..., extension_attributes=...) -> None:
        ...
    


def name_id_mapping_request_type__from_string(xml_string): # -> None:
    ...

class AssertionIDRequest(AssertionIDRequestType_):
    """The urn:oasis:names:tc:SAML:2.0:protocol:AssertionIDRequest element"""
    c_tag = ...
    c_namespace = ...
    c_children = ...
    c_attributes = ...
    c_child_order = ...
    c_cardinality = ...


def assertion_id_request_from_string(xml_string): # -> None:
    ...

class SubjectQuery(SubjectQueryAbstractType_):
    """The urn:oasis:names:tc:SAML:2.0:protocol:SubjectQuery element"""
    c_tag = ...
    c_namespace = ...
    c_children = ...
    c_attributes = ...
    c_child_order = ...
    c_cardinality = ...


def subject_query_from_string(xml_string): # -> None:
    ...

class RequestedAuthnContext(RequestedAuthnContextType_):
    """
    The urn:oasis:names:tc:SAML:2.0:protocol:RequestedAuthnContext element
    """
    c_tag = ...
    c_namespace = ...
    c_children = ...
    c_attributes = ...
    c_child_order = ...
    c_cardinality = ...


def requested_authn_context_from_string(xml_string): # -> None:
    ...

class AttributeQuery(AttributeQueryType_):
    """The urn:oasis:names:tc:SAML:2.0:protocol:AttributeQuery element"""
    c_tag = ...
    c_namespace = ...
    c_children = ...
    c_attributes = ...
    c_child_order = ...
    c_cardinality = ...


def attribute_query_from_string(xml_string): # -> None:
    ...

class AuthzDecisionQuery(AuthzDecisionQueryType_):
    """The urn:oasis:names:tc:SAML:2.0:protocol:AuthzDecisionQuery element"""
    c_tag = ...
    c_namespace = ...
    c_children = ...
    c_attributes = ...
    c_child_order = ...
    c_cardinality = ...


def authz_decision_query_from_string(xml_string): # -> None:
    ...

class IDPListType_(SamlBase):
    """The urn:oasis:names:tc:SAML:2.0:protocol:IDPListType element"""
    c_tag = ...
    c_namespace = ...
    c_children = ...
    c_attributes = ...
    c_child_order = ...
    c_cardinality = ...
    def __init__(self, idp_entry=..., get_complete=..., text=..., extension_elements=..., extension_attributes=...) -> None:
        ...
    


def idp_list_type__from_string(xml_string): # -> None:
    ...

class ArtifactResolve(ArtifactResolveType_):
    """The urn:oasis:names:tc:SAML:2.0:protocol:ArtifactResolve element"""
    c_tag = ...
    c_namespace = ...
    c_children = ...
    c_attributes = ...
    c_child_order = ...
    c_cardinality = ...


def artifact_resolve_from_string(xml_string): # -> None:
    ...

class ManageNameIDRequestType_(RequestAbstractType_):
    """
    The urn:oasis:names:tc:SAML:2.0:protocol:ManageNameIDRequestType element
    """
    c_tag = ...
    c_namespace = ...
    c_children = ...
    c_attributes = ...
    c_child_order = ...
    c_cardinality = ...
    def __init__(self, name_id=..., encrypted_id=..., new_id=..., new_encrypted_id=..., terminate=..., issuer=..., signature=..., extensions=..., id=..., version=..., issue_instant=..., destination=..., consent=..., text=..., extension_elements=..., extension_attributes=...) -> None:
        ...
    


def manage_name_id_request_type__from_string(xml_string): # -> None:
    ...

class LogoutRequest(LogoutRequestType_):
    """The urn:oasis:names:tc:SAML:2.0:protocol:LogoutRequest element"""
    c_tag = ...
    c_namespace = ...
    c_children = ...
    c_attributes = ...
    c_child_order = ...
    c_cardinality = ...


def logout_request_from_string(xml_string): # -> None:
    ...

class NameIDMappingRequest(NameIDMappingRequestType_):
    """The urn:oasis:names:tc:SAML:2.0:protocol:NameIDMappingRequest element"""
    c_tag = ...
    c_namespace = ...
    c_children = ...
    c_attributes = ...
    c_child_order = ...
    c_cardinality = ...


def name_id_mapping_request_from_string(xml_string): # -> None:
    ...

class AuthnQueryType_(SubjectQueryAbstractType_):
    """The urn:oasis:names:tc:SAML:2.0:protocol:AuthnQueryType element"""
    c_tag = ...
    c_namespace = ...
    c_children = ...
    c_attributes = ...
    c_child_order = ...
    c_cardinality = ...
    def __init__(self, requested_authn_context=..., session_index=..., subject=..., issuer=..., signature=..., extensions=..., id=..., version=..., issue_instant=..., destination=..., consent=..., text=..., extension_elements=..., extension_attributes=...) -> None:
        ...
    


def authn_query_type__from_string(xml_string): # -> None:
    ...

class IDPList(IDPListType_):
    """The urn:oasis:names:tc:SAML:2.0:protocol:IDPList element"""
    c_tag = ...
    c_namespace = ...
    c_children = ...
    c_attributes = ...
    c_child_order = ...
    c_cardinality = ...


def idp_list_from_string(xml_string): # -> None:
    ...

class ManageNameIDRequest(ManageNameIDRequestType_):
    """The urn:oasis:names:tc:SAML:2.0:protocol:ManageNameIDRequest element"""
    c_tag = ...
    c_namespace = ...
    c_children = ...
    c_attributes = ...
    c_child_order = ...
    c_cardinality = ...


def manage_name_id_request_from_string(xml_string): # -> None:
    ...

class AuthnQuery(AuthnQueryType_):
    """The urn:oasis:names:tc:SAML:2.0:protocol:AuthnQuery element"""
    c_tag = ...
    c_namespace = ...
    c_children = ...
    c_attributes = ...
    c_child_order = ...
    c_cardinality = ...


def authn_query_from_string(xml_string): # -> None:
    ...

class ScopingType_(SamlBase):
    """The urn:oasis:names:tc:SAML:2.0:protocol:ScopingType element"""
    c_tag = ...
    c_namespace = ...
    c_children = ...
    c_attributes = ...
    c_child_order = ...
    c_cardinality = ...
    def __init__(self, idp_list=..., requester_id=..., proxy_count=..., text=..., extension_elements=..., extension_attributes=...) -> None:
        ...
    


def scoping_type__from_string(xml_string): # -> None:
    ...

class Scoping(ScopingType_):
    """The urn:oasis:names:tc:SAML:2.0:protocol:Scoping element"""
    c_tag = ...
    c_namespace = ...
    c_children = ...
    c_attributes = ...
    c_child_order = ...
    c_cardinality = ...


def scoping_from_string(xml_string): # -> None:
    ...

class AuthnRequestType_(RequestAbstractType_):
    """The urn:oasis:names:tc:SAML:2.0:protocol:AuthnRequestType element"""
    c_tag = ...
    c_namespace = ...
    c_children = ...
    c_attributes = ...
    c_child_order = ...
    c_cardinality = ...
    def __init__(self, subject=..., name_id_policy=..., conditions=..., requested_authn_context=..., scoping=..., force_authn=..., is_passive=..., protocol_binding=..., assertion_consumer_service_index=..., assertion_consumer_service_url=..., attribute_consuming_service_index=..., provider_name=..., issuer=..., signature=..., extensions=..., id=..., version=..., issue_instant=..., destination=..., consent=..., text=..., extension_elements=..., extension_attributes=...) -> None:
        ...
    


def authn_request_type__from_string(xml_string): # -> None:
    ...

class AuthnRequest(AuthnRequestType_):
    """The urn:oasis:names:tc:SAML:2.0:protocol:AuthnRequest element"""
    c_tag = ...
    c_namespace = ...
    c_children = ...
    c_attributes = ...
    c_child_order = ...
    c_cardinality = ...


def authn_request_from_string(xml_string): # -> None:
    ...

class StatusType_(SamlBase):
    """The urn:oasis:names:tc:SAML:2.0:protocol:StatusType element"""
    c_tag = ...
    c_namespace = ...
    c_children = ...
    c_attributes = ...
    c_child_order = ...
    c_cardinality = ...
    def __init__(self, status_code=..., status_message=..., status_detail=..., text=..., extension_elements=..., extension_attributes=...) -> None:
        ...
    


def status_type__from_string(xml_string): # -> None:
    ...

class Status(StatusType_):
    """The urn:oasis:names:tc:SAML:2.0:protocol:Status element"""
    c_tag = ...
    c_namespace = ...
    c_children = ...
    c_attributes = ...
    c_child_order = ...
    c_cardinality = ...


def status_from_string(xml_string): # -> None:
    ...

class StatusResponseType_(SamlBase):
    """The urn:oasis:names:tc:SAML:2.0:protocol:StatusResponseType element"""
    c_tag = ...
    c_namespace = ...
    c_children = ...
    c_attributes = ...
    c_child_order = ...
    c_cardinality = ...
    def __init__(self, issuer=..., signature=..., extensions=..., status=..., id=..., in_response_to=..., version=..., issue_instant=..., destination=..., consent=..., text=..., extension_elements=..., extension_attributes=...) -> None:
        ...
    


def status_response_type__from_string(xml_string): # -> None:
    ...

class ResponseType_(StatusResponseType_):
    """The urn:oasis:names:tc:SAML:2.0:protocol:ResponseType element"""
    c_tag = ...
    c_namespace = ...
    c_children = ...
    c_attributes = ...
    c_child_order = ...
    c_cardinality = ...
    def __init__(self, assertion=..., encrypted_assertion=..., issuer=..., signature=..., extensions=..., status=..., id=..., in_response_to=..., version=..., issue_instant=..., destination=..., consent=..., text=..., extension_elements=..., extension_attributes=...) -> None:
        ...
    


def response_type__from_string(xml_string): # -> None:
    ...

class ArtifactResponseType_(StatusResponseType_):
    """The urn:oasis:names:tc:SAML:2.0:protocol:ArtifactResponseType element"""
    c_tag = ...
    c_namespace = ...
    c_children = ...
    c_attributes = ...
    c_child_order = ...
    c_cardinality = ...
    c_any = ...


def artifact_response_type__from_string(xml_string): # -> None:
    ...

class ManageNameIDResponse(StatusResponseType_):
    """The urn:oasis:names:tc:SAML:2.0:protocol:ManageNameIDResponse element"""
    c_tag = ...
    c_namespace = ...
    c_children = ...
    c_attributes = ...
    c_child_order = ...
    c_cardinality = ...


def manage_name_id_response_from_string(xml_string): # -> None:
    ...

class LogoutResponse(StatusResponseType_):
    """The urn:oasis:names:tc:SAML:2.0:protocol:LogoutResponse element"""
    c_tag = ...
    c_namespace = ...
    c_children = ...
    c_attributes = ...
    c_child_order = ...
    c_cardinality = ...


def logout_response_from_string(xml_string): # -> None:
    ...

class NameIDMappingResponseType_(StatusResponseType_):
    """
    The urn:oasis:names:tc:SAML:2.0:protocol:NameIDMappingResponseType element
    """
    c_tag = ...
    c_namespace = ...
    c_children = ...
    c_attributes = ...
    c_child_order = ...
    c_cardinality = ...
    def __init__(self, name_id=..., encrypted_id=..., issuer=..., signature=..., extensions=..., status=..., id=..., in_response_to=..., version=..., issue_instant=..., destination=..., consent=..., text=..., extension_elements=..., extension_attributes=...) -> None:
        ...
    


def name_id_mapping_response_type__from_string(xml_string): # -> None:
    ...

class Response(ResponseType_):
    """The urn:oasis:names:tc:SAML:2.0:protocol:Response element"""
    c_tag = ...
    c_namespace = ...
    c_children = ...
    c_attributes = ...
    c_child_order = ...
    c_cardinality = ...


def response_from_string(xml_string): # -> None:
    ...

class ArtifactResponse(ArtifactResponseType_):
    """The urn:oasis:names:tc:SAML:2.0:protocol:ArtifactResponse element"""
    c_tag = ...
    c_namespace = ...
    c_children = ...
    c_attributes = ...
    c_child_order = ...
    c_cardinality = ...


def artifact_response_from_string(xml_string): # -> None:
    ...

class NameIDMappingResponse(NameIDMappingResponseType_):
    """The urn:oasis:names:tc:SAML:2.0:protocol:NameIDMappingResponse element"""
    c_tag = ...
    c_namespace = ...
    c_children = ...
    c_attributes = ...
    c_child_order = ...
    c_cardinality = ...


def name_id_mapping_response_from_string(xml_string): # -> None:
    ...

class StatusCodeType_(SamlBase):
    """The urn:oasis:names:tc:SAML:2.0:protocol:StatusCodeType element"""
    c_tag = ...
    c_namespace = ...
    c_children = ...
    c_attributes = ...
    c_child_order = ...
    c_cardinality = ...
    def __init__(self, status_code=..., value=..., text=..., extension_elements=..., extension_attributes=...) -> None:
        ...
    


def status_code_type__from_string(xml_string): # -> None:
    ...

class StatusCode(StatusCodeType_):
    """The urn:oasis:names:tc:SAML:2.0:protocol:StatusCode element"""
    c_tag = ...
    c_namespace = ...
    c_children = ...
    c_attributes = ...
    c_child_order = ...
    c_cardinality = ...


def status_code_from_string(xml_string): # -> None:
    ...

ELEMENT_FROM_STRING = ...
ELEMENT_BY_TAG = ...
def factory(tag, **kwargs):
    ...

def any_response_from_string(xmlstr):
    ...

