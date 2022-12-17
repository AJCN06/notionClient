import requests
import json
from .variables import SEARCH_URL, QUERY_DB, QUERY_PAGE, NEW_PAGE


class Connection:
    def __init__(self, token):
        self.token = token
        self.h = {
            "accept": "application/json",
            "Authorization": f"Bearer {self.token}",
            "Notion-Version": "2022-06-28",
            "content-type": "application/json"
        }

    def search(self, filter_type: str) -> list:
        payload = {"filter": {"property": "object", "value": filter_type}}

        response = requests.post(SEARCH_URL, json=payload, headers=self.h)

        if response.status_code == 200:
            return True, response.json()['results']
        return False, []

    def get_records(self, database_id: str) -> list:
        response = requests.post(QUERY_DB.format(database_id), headers=self.h)

        if response.status_code == 200:
            return True, response.json()['results']
        return False, []

    def get_page(self, page_id):
        response = requests.get(QUERY_PAGE.format(page_id), headers=self.h)

        if response.status_code == 200:
            return True, response.json()
        return False, {}

    def update_page(self, page_id, page_data):
        response = requests.patch(QUERY_PAGE.format(
            page_id), json=page_data, headers=self.h)

        if response.status_code == 200:
            return True, response
        return False, {}

    def create_page(self, page):
        response = requests.post(NEW_PAGE, json=page, headers=self.h)
        if response.status_code == 200:
            return True, response
        return False, {}
