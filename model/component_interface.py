from model.abstract_api_element import AbstractApiElement


class ComponentInterface(AbstractApiElement):
    """
    Represents a Component Interface from the Decidim API.

    Even thought in GraphQL a ComponentInterface is considered an interface, it contains fields, for this reason,
    ComponentInterface is defined as a class.
    """

    @property
    def id(self) -> str:
        return self.__id

    @property
    def name(self) -> str:
        return self.__name

    @property
    def weight(self) -> int:
        return self.__weight

    def __init__(self, component_id: str, name: str, weight: int) -> None:
        self.__id: str = component_id
        self.__name: str = name
        self.__weight: int = weight
