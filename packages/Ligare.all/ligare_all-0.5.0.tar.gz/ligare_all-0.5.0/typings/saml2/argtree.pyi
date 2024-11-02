"""
This type stub file was generated by pyright.
"""

__author__ = ...
def find_paths(cls, arg, path=..., seen=..., res=..., lev=...): # -> list[Any] | None:
    ...

def set_arg(cls, arg, value): # -> list[Any]:
    ...

def add_path(tdict, path):
    """
    Create or extend an argument tree `tdict` from `path`.

    :param tdict: a dictionary representing a argument tree
    :param path: a path list
    :return: a dictionary

    Convert a list of items in a 'path' into a nested dict, where the
    second to last item becomes the key for the final item. The remaining
    items in the path become keys in the nested dict around that final pair
    of items.

    For example, for input values of:
        tdict={}
        path = ['assertion', 'subject', 'subject_confirmation',
                'method', 'urn:oasis:names:tc:SAML:2.0:cm:bearer']

        Returns an output value of:
           {'assertion': {'subject': {'subject_confirmation':
                         {'method': 'urn:oasis:names:tc:SAML:2.0:cm:bearer'}}}}

    Another example, this time with a non-empty tdict input:

        tdict={'method': 'urn:oasis:names:tc:SAML:2.0:cm:bearer'},
        path=['subject_confirmation_data', 'in_response_to', '_012345']

        Returns an output value of:
            {'subject_confirmation_data': {'in_response_to': '_012345'},
             'method': 'urn:oasis:names:tc:SAML:2.0:cm:bearer'}
    """
    ...

def is_set(tdict, path): # -> bool:
    """

    :param tdict: a dictionary representing a argument tree
    :param path: a path list
    :return: True/False if the value is set
    """
    ...

def get_attr(tdict, path):
    ...

