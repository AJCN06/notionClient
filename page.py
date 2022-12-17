class Page():
    def __init__(self, notion_data):
        self.title = str()
        self.properties = list()

        self.parent = notion_data['parent']['database_id']
        self.id = notion_data['id']
        self.cover = notion_data['cover']['external']['url'] if notion_data['cover'] else None
        self.database_id = notion_data['parent']['database_id']
        self.created_time = notion_data['created_time']
        self.last_edited_time = notion_data['last_edited_time']

        self.__build_properties(notion_data['properties'])
        if notion_data['icon']:
            if notion_data['icon']['type'] == 'emoji':
                self.icon = notion_data['icon']['emoji']
            else:
                self.icon = notion_data['icon']['external']['url']
            self.icon_type = notion_data['icon']['type']
        else:
            self.icon = None
            self.icon_type = None

    def __build_properties(self, notion_properties):

        for k, p in notion_properties.items():
            # TODO complete all types properties

            if p['type'] == 'title':
                title = Title(k, p)
                self.title = title.text
                self.properties.append(title)

            elif p['type'] == 'rich_text':
                self.properties.append(Text(k, p))

            elif p['type'] == 'number':
                self.properties.append(Number(k, p))

            elif p['type'] == 'select':
                self.properties.append(Select(k, p))

            elif p['type'] == 'status':
                self.properties.append(Status(k, p))

            elif p['type'] == 'multi_select':
                self.properties.append(MultiSelect(k, p))

            elif p['type'] == 'date':
                self.properties.append(Date(k, p))

            elif p['type'] == 'relation':
                self.properties.append(Relation(k, p))

            elif p['type'] == 'checkbox':
                self.properties.append(Checkbox(k, p))

            elif p['type'] == 'url':
                self.properties.append(Url(k, p))

            elif p['type'] == 'email':
                self.properties.append(Email(k, p))

            elif p['type'] == 'phone_number':
                self.properties.append(PhoneNumber(k, p))

            elif p['type'] == 'created_time':
                self.properties.append(Created_time(k, p))

            # elif p['type'] == 'created_by':
            #     print(p['type'])

            # elif p['type'] == 'last_edited_time':
            #     print(p['type'])

            # elif p['type'] == 'last_edited_by':
            #     print(p['type'])

            # elif p['type'] == 'formula':
            #     print(p['type'])

            # elif p['type'] == 'rollup':
            #     print(p['type'])

            # elif p['type'] == 'people':
            #     print(p['type'])

            # elif p['type'] == 'files':
            #     print(p['type'])
            else:
                print(p['type'])

    def get_prop(self, key: str = None):
        # FIXME when return none in some case I use get_prop('').some and lauch error
        if not key:
            return None

        for p in self.properties:
            if p.id == key or p.title == key:
                return p
        return None

    def set_prop(self, key: str = None, data: dict = None):
        if not key or not data:
            return None
        prop = self.get_prop(key=key)

        prop.update(data)
        if prop.type == 'title':
            self.title = prop.text

    def json(self):
        prop_list = dict()
        for prop in self.properties:
            complete, key, value = prop.json()
            if complete:
                prop_list[key] = value

        data = dict()
        data["properties"] = prop_list

        if self.cover:
            data['cover'] = {"external": {"url": self.cover}}

        if self.icon:
            if self.icon_type == 'external':
                data['icon'] = {"external": {"url": self.icon}}
            else:
                data['icon'] = {"emoji": self.icon}

        return data

    def print(self):
        print(self.__str__())
        for p in self.properties:
            print(p)

    def __str__(self):
        return f'''
id: {self.id}
title:  {self.title}
cover: {self.cover}
icon: {self.icon}
database_id: {self.database_id}
created_time: {self.created_time}
last_edited_time:  {self.last_edited_time}
properties:'''


class Propertie:
    def __init__(self, name, data):
        self.id = data['id']
        self.title = name
        self.type = data['type']

    def update(self, data):
        pass

    def json(self):
        return {
            'id': self.id,
            'type': self.type,
            'name': self.title
        }

    def __str__(self):
        return f'\t{self.title}'


class Relation(Propertie):
    def __init__(self, name, data):
        super().__init__(name, data)
        if data[self.type]:
            self.relations = [{'id': r['id']} for r in data[self.type]]
        else:
            self.relations = []

    def update(self, data):
        self.relations = data

    def have_relation(self, key):
        for r in self.relations:
            if r['id'] == key:
                return True
        return False

    def json(self):
        return True, self.id, {self.type: self.relations}

    def __str__(self):
        return super().__str__() + f', realtaion with: {[r["id"] for r in self.relations]}'


class Select(Propertie):
    def __init__(self, name, data):
        super().__init__(name, data)
        if data[self.type]:
            self.value = data[self.type]['name']
            self.value_id = data[self.type]['id']
        else:
            self.value = None
            self.value_id = None

    def update(self, data):
        self.value = data['name']
        self.value_id = data['id']

    def json(self):
        if not self.value_id:
            return False, self.id, {}
        return True, self.id, {self.type: {'name': self.value, 'id': self.value_id}}

    def __str__(self):
        return super().__str__() + f': {self.value},'


class MultiSelect(Propertie):
    def __init__(self, name, data):
        super().__init__(name, data)
        if data[self.type]:
            self.values = list()
            for e in data[self.type]:
                self.values.append({"name": e['name'], "id": e['id']})
        else:
            self.values = []

    def have_value(self, key):
        for v in self.values:
            if v['id'] == key:
                return True
        return False

    def update(self, data):
        self.values = data

    def json(self):
        return True, self.id, {self.type: self.values}

    def __str__(self):
        return super().__str__() + f': {[v["name"] for v in self.values]},'


class Number(Propertie):
    def __init__(self, name, data):
        super().__init__(name, data)
        self.value = data[self.type]

    def update(self, data):
        self.value = data['number']

    def json(self):
        return True, self.id, {self.type: self.value}

    def __str__(self):
        return super().__str__() + f': {self.value},'


class Title(Propertie):
    def __init__(self, name, data):
        super().__init__(name, data)
        self.text = data[self.type][0]['plain_text'] if data[self.type] else None

    def update(self, data):
        self.text = data[0]['text']['content']

    def json(self):
        return True, self.type, {self.type: [{"type": "text", "text": {"content": self.text}}]}

    def __str__(self):
        return super().__str__() + f': {self.text},'


class Text(Propertie):
    def __init__(self, name, data):
        super().__init__(name, data)
        self.text = data[self.type][0]['plain_text'] if data['rich_text'] else None

    def update(self, data):
        self.text = data[0]['text']['content']

    def json(self):
        return True, self.id, {self.type: [{"type": "text", "text": {"content": self.text}}]}

    def __str__(self):
        return super().__str__() + f': {self.text},'


class Checkbox(Propertie):
    def __init__(self, name, data):
        super().__init__(name, data)
        self.check = data[self.type]

    def update(self, data):
        self.check = data['checkbox']

    def json(self):
        return True, self.id, {self.type: self.check}

    def __str__(self):
        return super().__str__() + f': {self.check},'


class Status(Propertie):
    def __init__(self, name, data):
        super().__init__(name, data)
        self.value = data[self.type]['name']
        self.value_id = data[self.type]['id']

    def update(self, data):
        self.value = data['name']
        self.value_id = data['id']

    def json(self):
        return True, self.id, {self.type: {'name': self.value, 'id': self.value_id}}

    def __str__(self):
        return super().__str__() + f': {self.value},'


class Url(Propertie):
    def __init__(self, name, data):
        super().__init__(name, data)
        self.url = data[self.type] if data['url'] else None

    def update(self, data):
        self.url = data['url']

    def json(self):
        return True, self.id, {self.type: self.url}

    def __str__(self):
        return super().__str__() + f': {self.url},'


class Email(Propertie):
    def __init__(self, name, data):
        super().__init__(name, data)
        self.email = data[self.type] if data['email'] else None

    def update(self, data):
        self.email = data['email']

    def json(self):
        return True, self.id, {self.type: self.email}

    def __str__(self):
        return super().__str__() + f': {self.email},'


class PhoneNumber(Propertie):
    def __init__(self, name, data):
        super().__init__(name, data)
        self.phone_number = data[self.type] if data[self.type] else None

    def update(self, data):
        self.phone_number = data['phone_number']

    def json(self):
        return True, self.id, {self.type: self.phone_number}

    def __str__(self):
        return super().__str__() + f': {self.phone_number},'


class Date(Propertie):
    def __init__(self, name, data):
        super().__init__(name, data)
        if data[self.type]:
            self.date_start = data[self.type]['start']
            self.date_end = data[self.type]['end']
            self.time_zone = data[self.type]['time_zone']
        else:
            self.date_start = None
            self.date_end = None
            self.time_zone = None

    def update(self, data):
        self.date_start = data['start']
        self.date_end = data['end']
        self.time_zone = data['time_zone']

    def json(self):
        data = {"start": self.date_start}

        if self.date_end:
            data['end'] = self.date_end
        if self.time_zone:
            data['time_zone'] = self.time_zone

        return True, self.id, {self.type: data}

    def __str__(self):
        return super().__str__() + f': {self.date_start} -> {self.date_end} tz: {self.time_zone},'


class Created_time(Propertie):
    def __init__(self, name, data):
        super().__init__(name, data)
        self.created_time = data[self.type]

    def update(self, data):
        pass

    def json(self):
        return False, self.id, {}

    def __str__(self):
        return super().__str__() + f': {self.created_time},'
