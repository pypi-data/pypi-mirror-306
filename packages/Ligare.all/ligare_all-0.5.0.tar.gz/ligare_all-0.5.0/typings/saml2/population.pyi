"""
This type stub file was generated by pyright.
"""

logger = ...
class Population:
    def __init__(self, cache=...) -> None:
        ...
    
    def add_information_about_person(self, session_info):
        """If there already are information from this source in the cache
        this function will overwrite that information"""
        ...
    
    def stale_sources_for_person(self, name_id, sources=...): # -> list[Any]:
        """

        :param name_id: Identifier of the subject, a NameID instance
        :param sources: Sources for information about the subject
        :return:
        """
        ...
    
    def issuers_of_info(self, name_id): # -> list[Any]:
        ...
    
    def get_identity(self, name_id, entities=..., check_not_on_or_after=...): # -> tuple[dict[Any, Any], list[Any]]:
        ...
    
    def get_info_from(self, name_id, entity_id, check_not_on_or_after=...): # -> Any | None:
        ...
    
    def subjects(self): # -> list[NameID]:
        """Returns the name id's for all the persons in the cache"""
        ...
    
    def remove_person(self, name_id): # -> None:
        ...
    
    def get_entityid(self, name_id, source_id, check_not_on_or_after=...): # -> Any | Literal['']:
        ...
    
    def sources(self, name_id): # -> list[Any]:
        ...
    


