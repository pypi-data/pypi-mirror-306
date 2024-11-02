"""
This type stub file was generated by pyright.
"""

from saml2 import SAMLError

__author__ = ...
logger = ...
class AuthnFailure(SAMLError):
    ...


class EncodeError(SAMLError):
    ...


class UserAuthnMethod:
    def __init__(self, srv) -> None:
        ...
    
    def __call__(self, *args, **kwargs):
        ...
    
    def authenticated_as(self, **kwargs):
        ...
    
    def verify(self, **kwargs):
        ...
    


def is_equal(a, b): # -> bool:
    ...

def url_encode_params(params=...): # -> str:
    ...

def create_return_url(base, query, **kwargs): # -> str:
    """
    Add a query string plus extra parameters to a base URL which may contain
    a query part already.

    :param base: redirect_uri may contain a query part, no fragment allowed.
    :param query: Old query part as a string
    :param kwargs: extra query parameters
    :return:
    """
    ...

class UsernamePasswordMako(UserAuthnMethod):
    """Do user authentication using the normal username password form
    using Mako as template system"""
    cookie_name = ...
    def __init__(self, srv, mako_template, template_lookup, pwd, return_to) -> None:
        """
        :param srv: The server instance
        :param mako_template: Which Mako template to use
        :param pwd: Username/password dictionary like database
        :param return_to: Where to send the user after authentication
        :return:
        """
        ...
    
    def __call__(self, cookie=..., policy_url=..., logo_url=..., query=..., **kwargs): # -> Response:
        """
        Put up the login form
        """
        ...
    
    def verify(self, request, **kwargs): # -> Redirect | Unauthorized:
        """
        Verifies that the given username and password was correct
        :param request: Either the query part of a URL a urlencoded
            body of a HTTP message or a parse such.
        :param kwargs: Catch whatever else is sent.
        :return: redirect back to where ever the base applications
            wants the user after authentication.
        """
        ...
    
    def authenticated_as(self, cookie=..., **kwargs): # -> dict[str, str] | None:
        ...
    
    def done(self, areq): # -> bool:
        ...
    


class SocialService(UserAuthnMethod):
    def __init__(self, social) -> None:
        ...
    
    def __call__(self, server_env, cookie=..., sid=..., query=..., **kwargs):
        ...
    
    def callback(self, server_env, cookie=..., sid=..., query=..., **kwargs):
        ...
    


class AuthnMethodChooser:
    def __init__(self, methods=...) -> None:
        ...
    
    def __call__(self, **kwargs): # -> None:
        ...
    


class LDAPAuthn(UsernamePasswordMako):
    def __init__(self, srv, ldapsrv, return_to, dn_pattern, mako_template, template_lookup) -> None:
        """
            :param srv: The server instance
            :param ldapsrv: Which LDAP server to us
            :param return_to: Where to send the user after authentication
            :return:
            """
        ...
    


