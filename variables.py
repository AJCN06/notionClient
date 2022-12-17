SEARCH_URL = 'https://api.notion.com/v1/search'
QUERY_DB = 'https://api.notion.com/v1/databases/{}/query'
QUERY_PAGE = 'https://api.notion.com/v1/pages/{}'
NEW_PAGE = 'https://api.notion.com/v1/pages'

TYPES_TEMPLATE = {
    'title': [{'type': 'text', 'text': {'content': str()}}],
    'rich_text': [{'type': 'rich_text', 'text': {'content': str()}}],
    'number': {'number': int()},
    'select': {'name': str(), 'id': str()},
    'status': {'name': str(), 'id': str()},
    'multi_select': [{'name': str(), 'id': str()}],
    'date': {'start': str(), 'end': str(), 'time_zone': str()},
    'relation': [{'id': str()}],
    'checkbox': {'checkbox': bool()},
    'url': {'url': str()},
    'email': {'email': str()},
    'phone_number': {'phone_number': str()},

    'created_time': 'no editable',
    'created_by': 'no editable',
    'last_edited_time': 'no editable',
    'last_edited_by': 'no editable',

    'formula': 'pending to add',
    'rollup': 'pending to add',
    'people': 'pending to add',
    'files': 'pending to add',
}
