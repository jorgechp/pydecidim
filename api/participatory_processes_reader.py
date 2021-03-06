"""
This Reader retrives a list of Participatory processes from Decidim.
"""
from typing import List

from api.abstract_decidim_reader import AbstractDecidimReader
from api.decidim_connector import DecidimConnector
from model.participatory_process import ParticipatoryProcess

from model.participatory_process_filter import ParticipatoryProcessFilter
from model.participatory_process_sort import ParticipatoryProcessSort

# Path to the query schema
from model.translated_field import TranslatedField

API_URL = 'queries\\participatory_processes.graphql'


class ParticipatoryProcessesReader(AbstractDecidimReader):
    """
    This reader retrieves list of Participatory processes from Decidim.
    """

    def __init__(self, decidim_connector: DecidimConnector, base_path="."):
        """

        :param decidim_connector: An instance of a DecidimConnector class.
        :param base_path: The base path to the schema directory.
        """
        super().__init__(decidim_connector, base_path + "\\" + API_URL)

    def process_query(self) -> List[ParticipatoryProcess]:
        """
        Send the query to the API and extract a list of participatory processes.
        :return: A list of participatory processes.
        """

        component_filter: ParticipatoryProcessFilter = ParticipatoryProcessFilter()
        component_sort: ParticipatoryProcessSort = ParticipatoryProcessSort()
        response: dict = super().process_query_from_file({'filter': component_filter, 'order': component_sort})

        participatory_processes: List[ParticipatoryProcess] = []
        for participatory_process_dict in response['participatoryProcesses']:
            id: str = participatory_process_dict['id']
            translations: [] = participatory_process_dict['title']['translations']
            title: TranslatedField = TranslatedField.parse_from_gql(translations)
            participatory_process: ParticipatoryProcess = ParticipatoryProcess(id=id, title=title)
            participatory_processes.append(participatory_process)
        return participatory_processes
