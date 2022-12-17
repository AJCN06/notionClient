from .variables import TYPES_TEMPLATE


class Database:

    def __init__(self, notion_data):
        self.id = notion_data['id']
        self.title = notion_data['title'][0]['plain_text']
        self.description = notion_data['description']
        self.columns = list()
        self.__build_columns(notion_data['properties'])

    def __build_columns(self, notion_properties):
        for k, v in notion_properties.items():
            self.columns.append(Column(v))

    def new_page(self):
        return {
            'type': 'database_id',
            'database_id': self.id,
        }

    def get_col(self, name):
        for col in self.columns:
            if col.title == name:
                return col
        return None

    def json(self):
        return {
            "title:": self.title,
            "description": self.description,
            "id:": self.id,
            "columns": self.__json_columns()
        }

    def __json_columns(self):
        data = list()
        for col in self.columns:
            data.append(col.json())
        return data

    def print(self):
        print(self.__str__())
        for col in self.columns:
            print(col)

    def __str__(self) -> str:
        return f'''
id: {self.id}
title: {self.title}
description: {self.description}
columns:'''

class Column:
    def __init__(self, notino_data):
        self.id = notino_data['id']
        self.type = notino_data['type']
        self.title = notino_data['name']
        self.options = self.__build_options(notino_data)
        self.template = TYPES_TEMPLATE[self.type]

    def __build_options(self, data):
        if self.type == 'status':
            return [{"name": o['name'], "id": o['id']} for o in data['status']['options']]

        elif self.type == 'select':
            return [{"name": o['name'], "id": o['id']} for o in data['select']['options']]

        elif self.type == 'multi_select':
            return [{"name": o['name'], "id": o['id']} for o in data['multi_select']['options']]

        elif self.type == 'relation':
            return {'relation_database_id': data['relation']['database_id']}

        else:
            return "Any"

    def get_option_id(self, name):
        if self.type in ['status', 'select', 'multi_select']:
            for o in self.options:
                if o['name'] == name:
                    return o['id']
        return None

    def json(self):
        return {
            "id:": self.id,
            "title:": self.title,
            "type": self.type,
            "template_to_update": str(self.template),
            "options": self.options
        }

    def __str__(self):
        return f'\tName: {self.title}, Type: {self.type}, Id: {self.id}'
