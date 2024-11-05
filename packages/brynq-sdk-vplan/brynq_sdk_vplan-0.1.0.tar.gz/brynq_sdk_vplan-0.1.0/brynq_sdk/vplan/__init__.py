import requests
import json
from typing import List, Union
from brynq_sdk.brynq import BrynQ
from brynq_sdk.vplan.activity import Activity
from brynq_sdk.vplan.item import Item
from brynq_sdk.vplan.project import Project
from brynq_sdk.vplan.resource import Resource
from brynq_sdk.vplan.time_tracking import TimeTracking
from brynq_sdk.vplan.user import User


class VPlan(BrynQ):
    def __init__(self, label: Union[str, List], debug: bool = False):
        """
        A class to fetch data from the vPlan API. See https://developer.vplan.com/documentation/#tag/General/ for more information
        """
        super().__init__()
        self.headers = self._get_credentials(label)
        self.base_url = 'https://api.vplan.com/v1/'
        self.activity = Activity(self)
        self.item = Item(self)
        self.project = Project(self)
        self.resource = Resource(self)
        self.time_tracking = TimeTracking(self)
        self.user = User(self)

    def _get_credentials(self, label) -> str:
        """
        Retrieve API key and env from the system credentials.
        Args: label (Union[str, List]): The label or list of labels to get the credentials.
        Returns: str: The authorization headers
        """
        credentials = self.get_system_credential(system='vplan', label=label)
        headers = {
            'X-Api-Key': credentials['X-Api-Key'],
            'X-Api-Env': credentials['X-Api-Env']
        }
        return headers