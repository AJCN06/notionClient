


# Client

## Init

To create a new client you need a notion integration token

```python
notion = Client(token)
```

## Search

Return a type page list (database, page, block) in this version only works with databases

```python
notion.search(search_type: str = 'database') -> list[Database]:
```

## Export databases

Create a file called `databases_guide.json` with all the information about the databases structure without the pages to help me understand it. Its create by default when you make a `notion.search()`

```python
notion.export_dbs() -> None:
```

## Query database
Returns a pages array for the db_id selected

```python
notion.query_databae(database_id: str = None) -> list():
```

<!-- pending code
## Create database
## Update database
## Get database
 -->

## Get page
Return a unique page from a notion id

```python
notion.get_page(page_id: str = None) -> Page:
```

## Create page
Create a new empty page in notion and return the python object 

```python
notion.create_page(parent: str = None) -> Page:
```

## Update page
Save the python object version in notion, updating the row properties

```python
notion.update_page(page: Page = None) -> bool():
```


<!-- pending code
    Block functionality
    Users functionality
 -->



# Database

## Variables
```python
id: str = 'notion database id' 
title: str = 'notion page title'
description: str = 'any description'
columns: list(Column) = 'columns python object list'
```


## Init
```python
database = Database(notion_data: dict) -> None:
```


## New page
return the parent information to create a new page in this database

```python
parent = database.new_page_parent() -> dict:
```

## Get column
return a python object Column

```python
database.get_col(name: str) -> Column:
```

<!-- ## Json -->

## Columns


### Variables
```python
id = 'notion column id'
type = 'notion column type'
title = 'notion column title'
options = 'notion column options if have availables'
template = ' template to edit from variables.TYPES_TEMPLATE[self.type]'
```

### Init
```python
col = Column(notion_data: dict) -> None:
```

### Get Options Id
Return the column id related with the option name 

```python
option_id = col.get_option_id(option_name: str) -> str():
```

### Columns update templates 
```python
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

```
# Page
## Variables
```python
page.title: str = 'notion page title'
page.properties: list = 'Propertie python objects List'
page.parent: str = 'database id'
page.id: str = 'notion id'
page.cover: str = 'notion cover'
page.database_id: str = 'database id'
page.created_time: str = 'notion created time'
page.last_edited_time: str = 'notion created time'
page.icon: str = 'notion icon url or emoji'
page.icon_type: str = 'notion icon type'

```
## Init
```python
page = Page(notion_data: dict) -> None:
```

## Get a prop
Return a python propertie with all his information

```python
page.get_prop(prop_name: str)-> Propertie:
```

## Update a prop
Update the propertie data with a new information, this imnformation should have a specific format from `variables.TYPES_TEMPLATE[page.type]`

```python
page.set_prop(prop_name: str, formated_data: dict) -> None
```



## Propertie
All prop have this methods and variables always and each specific type have his own methods and variables

```python
prop.id: str  = 'notion col id '
prop.title: str  = 'notion col title '
prop.type: str  = 'notion col type '
```

All prop have a `update` method

## Types

### Relation
```python
# variables
prop.relations: list = 'array of {id}'

# methods
prop.have_relation(relation_id:str) -> bool():
```


### Select

```python
# variables
prop.option: str = 'option name'
prop.option_id: str = 'option id'

# methods
```


### MultiSelect

```python
# variables
prop.options: list({"name": 'name', "id": 'id'}) = 'notion options selected'

# methods
prop.have_option(option_id: str) -> bool():
```


### Number

```python
# variables
prop.number: int = 'notion value'

# methods
```


### Title

```python
# variables
prop.text: str = 'notion title'

# methods
```


### Text

```python
# variables
prop.text: str = 'notion text'

# methods
```


### Checkbox

```python
# variables
prop.check: bool =  'value from notion, checked = True'

# methods
```


### Status

```python
# variables
prop.option: str = 'option name'
prop.option_id: str = 'option id'

# methods
```


### Url

```python
# variables
prop.url: str = 'notion url'

# methods
```


### Email

```python
# variables
prop.email: str = 'notion Email value'

# methods
```


### PhoneNumber

```python
# variables
prop.phone_number: str = 'notion Phone Number value'

# methods
```


### Date

```python
# variables
prop.date_start: str = 'notion start date'
prop.date_end: str = 'notion end date in case it have one'
prop.time_zone: str = 'notion start date in case it have one'

# methods
```


### Created_time

```python
# variables
prop.created_time: str = 'notion Created_time'

# methods
```

