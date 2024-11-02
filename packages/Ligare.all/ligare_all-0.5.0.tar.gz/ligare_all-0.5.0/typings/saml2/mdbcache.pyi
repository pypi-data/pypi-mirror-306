"""
This type stub file was generated by pyright.
"""

__author__ = ...
logger = ...
class Cache:
    def __init__(self, server=..., debug=..., db=...) -> None:
        ...
    
    def delete(self, subject_id): # -> None:
        ...
    
    def get_identity(self, subject_id, entities=..., check_not_on_or_after=...): # -> tuple[dict[Any, Any], list[Any]]:
        """Get all the identity information that has been received and
        are still valid about the subject.

        :param subject_id: The identifier of the subject
        :param entities: The identifiers of the entities whoes assertions are
            interesting. If the list is empty all entities are interesting.
        :return: A 2-tuple consisting of the identity information (a
            dictionary of attributes and values) and the list of entities
            whoes information has timed out.
        """
        ...
    
    def get(self, subject_id, entity_id, check_not_on_or_after=...): # -> dict[Any, Any] | None:
        ...
    
    def set(self, subject_id, entity_id, info, timestamp=...): # -> None:
        """Stores session information in the cache. Assumes that the subject_id
        is unique within the context of the Service Provider.

        :param subject_id: The subject identifier
        :param entity_id: The identifier of the entity_id/receiver of an
            assertion
        :param info: The session info, the assertion is part of this
        :param timestamp: A time after which the assertion is not valid.
        """
        ...
    
    def reset(self, subject_id, entity_id): # -> None:
        """Scrap the assertions received from a IdP or an AA about a special
        subject.

        :param subject_id: The subjects identifier
        :param entity_id: The identifier of the entity_id of the assertion
        :return:
        """
        ...
    
    def entities(self, subject_id): # -> list[Any]:
        """Returns all the entities of assertions for a subject, disregarding
        whether the assertion still is valid or not.

        :param subject_id: The identifier of the subject
        :return: A possibly empty list of entity identifiers
        """
        ...
    
    def receivers(self, subject_id): # -> list[Any]:
        """Another name for entities() just to make it more logic in the IdP
        scenario"""
        ...
    
    def active(self, subject_id, entity_id): # -> bool:
        """Returns the status of assertions from a specific entity_id.

        :param subject_id: The ID of the subject
        :param entity_id: The entity ID of the entity_id of the assertion
        :return: True or False depending on if the assertion is still
            valid or not.
        """
        ...
    
    def subjects(self): # -> list[Any]:
        """Return identifiers for all the subjects that are in the cache.

        :return: list of subject identifiers
        """
        ...
    
    def update(self, subject_id, entity_id, ava): # -> None:
        """ """
        ...
    
    def valid_to(self, subject_id, entity_id, newtime): # -> None:
        """ """
        ...
    
    def clear(self): # -> None:
        ...
    


