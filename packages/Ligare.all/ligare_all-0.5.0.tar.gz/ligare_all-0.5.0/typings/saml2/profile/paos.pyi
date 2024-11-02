"""
This type stub file was generated by pyright.
"""

from saml2 import SamlBase

NAMESPACE = ...
class RequestType_(SamlBase):
    """The urn:liberty:paos:2003-08:RequestType element"""
    c_tag = ...
    c_namespace = ...
    c_children = ...
    c_attributes = ...
    c_child_order = ...
    c_cardinality = ...
    def __init__(self, response_consumer_url=..., service=..., message_id=..., must_understand=..., actor=..., text=..., extension_elements=..., extension_attributes=...) -> None:
        ...
    


def request_type__from_string(xml_string): # -> None:
    ...

class ResponseType_(SamlBase):
    """The urn:liberty:paos:2003-08:ResponseType element"""
    c_tag = ...
    c_namespace = ...
    c_children = ...
    c_attributes = ...
    c_child_order = ...
    c_cardinality = ...
    def __init__(self, ref_to_message_id=..., must_understand=..., actor=..., text=..., extension_elements=..., extension_attributes=...) -> None:
        ...
    


def response_type__from_string(xml_string): # -> None:
    ...

class Request(RequestType_):
    """The urn:liberty:paos:2003-08:Request element"""
    c_tag = ...
    c_namespace = ...
    c_children = ...
    c_attributes = ...
    c_child_order = ...
    c_cardinality = ...


def request_from_string(xml_string): # -> None:
    ...

class Response(ResponseType_):
    """The urn:liberty:paos:2003-08:Response element"""
    c_tag = ...
    c_namespace = ...
    c_children = ...
    c_attributes = ...
    c_child_order = ...
    c_cardinality = ...


def response_from_string(xml_string): # -> None:
    ...

ELEMENT_FROM_STRING = ...
ELEMENT_BY_TAG = ...
def factory(tag, **kwargs):
    ...

