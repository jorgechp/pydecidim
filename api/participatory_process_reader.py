"""
This Reader retrives a list of Participatory processes from Decidim.
"""
from typing import List

from api.abstract_decidim_reader import AbstractDecidimReader
from api.decidim_connector import DecidimConnector
from model.component_interface import ComponentInterface
from model.elemental_type_element import ElementalTypeElement
from model.participatory_process import ParticipatoryProcess

from model.participatory_process_filter import ParticipatoryProcessFilter
from model.participatory_process_sort import ParticipatoryProcessSort

# Path to the query schema
from model.translated_field import TranslatedField

API_URL = 'queries\\participatory_process.graphql'


class ParticipatoryProcessReader(AbstractDecidimReader):
    """
    This reader retrieves list of Participatory processes from Decidim.
    """

    def __init__(self, decidim_connector: DecidimConnector, base_path="."):
        """

        :param decidim_connector: An instance of a DecidimConnector class.
        :param base_path: The base path to the schema directory.
        """
        super().__init__(decidim_connector, base_path + "\\" + API_URL)

    def process_query(self, participatory_process_id: str) -> ParticipatoryProcess:
        """
        Send the query to the API and extract a list of participatory processes.
        :param participatory_process_id: The participatory process id.
        :return: A list of participatory processes.
        """

        response: dict = super().process_query_from_file({'id': ElementalTypeElement(participatory_process_id)})
        participatory_process_dict = response['participatoryProcess']
        translations: [] = participatory_process_dict['title']['translations']
        components_dict: [dict] = participatory_process_dict['components']
        components: List[ComponentInterface] = []

        for component in components_dict:
            component_id: str = component['id']
            component_name: TranslatedField = TranslatedField.parse_from_gql(component['name']['translations'])
            component_weight: int = component['weight']
            component_interface: ComponentInterface = ComponentInterface(component_id,
                                                                         component_name,
                                                                         component_weight)
            components.append(component_interface)
        title: TranslatedField = TranslatedField.parse_from_gql(translations)
        participatory_process: ParticipatoryProcess = ParticipatoryProcess(process_id=participatory_process_id,
                                                                           title=title,
                                                                           components=components)
        return participatory_process