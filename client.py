from .connection import Connection
from .database import Database
from .page import Page
import json


class Client:

    def __init__(self, token):
        self.remote = Connection(token)
        self.dbs = list[Database]

    def search(self, search_type: str = 'database') -> list[Database]:
        if search_type == 'database':
            success, records = self.remote.search(search_type)

            dbs = [Database(r) for r in records]
            self.dbs = dbs
            self.export_dbs()

        return self.dbs

    def export_dbs(self) -> None:
        json_data = list()
        for db in self.dbs:
            json_data.append(db.json())
        with open(f'databases_guide.json', 'w') as f:
            json.dump(json_data, f)

# Databases

    def query_database(self, database_id: str):
        success, records = self.remote.get_records(database_id)
        if success:
            pages = [Page(r) for r in records]
            return pages
        return []

    # TODO create a database
    def create_database(self):
        pass

    # TODO Update datase
    def update_database(self):
        pass

    # TODO Retrieve a database
    def get_database(self):
        pass

# Pages

    # TODO retreave a page
    def get_page(self, page_id):
        success, record = self.remote.get_page(page_id)
        if success:
            return Page(record)

    def create_page(self, page):
        success, record = self.remote.create_page({
            'parent': page, 'properties': []
        })

        if success:
            return Page(record)

    def update_page(self, page: Page):
        success, records = self.remote.update_page(page.id, page.json())
        return success

# TODO Blocks functionality
    # retireve a block
    # update a block
    # Retreave block children
    # Append block children


# TODO Users functionality
    # Retreave a user
    # List all user
