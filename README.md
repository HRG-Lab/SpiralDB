SpiralDB
========

## Introduction
SpiralDB attempts to provide a better way of storing and interacting with spiral data. All interaction with the database is abstracted away. 

## Use
### Installation
Simpy download this module and run 
```
python setup.py install
```
Then in your code, just include the module
```python
import spiraldb

...
```
### Connecting to the database
Spiraldb uses sqlalchemy on the backend, and all of the functions used in interacting with the database require a sqlalchemy session as an argument. Because this is very basic database interaction, the easiest way to provide the session is to create one at global scope. 
```python
import spiraldb

db = "tests/test.db"
session = sprialdb.connect(db)
```

### Spiral object
The database contains Spiral objects with the following structure:

| id | nodes | frequency_results | phase_results | rf_data | vision_data |
|---|---|---|---|---|---
| id of the spiral | comma delimited list of nodal coordinates | csv file of frequency results stored as a string (handled during object creation) | csv file of frequency results stored as a string (handled during object creation) | a dictionary of rf related data stored as a JSON string | a dictionary of computer vision related data stored as a JSON string |

RF Data and Vision Data were made to be dictionaries so as to allow arbitrary fields to be added to the object withouth having to manipulate the structure of the database

### Creating spiral objets
Here is an example of creating a Spiral object
```python
example_data_path = os.path.join(os.getcwd(), "tests", "ExampleData")
nodal_data_path = os.path.join(example_data_path, "NODAL-COORDINATES-spiral_contour_image_18.txt")
frequency_results = os.path.join(example_data_path, "FREQUENCY-RESULTS-spiral_contour_image_18.csv")
phase_results = os.path.join(example_data_path, "PHASE-RESULTS-spiral_contour_image_phase_18.csv")

spiraldb.create_spiral(
    session,
    id=18,
    nodes=nodal_data_path,
    frequency_results=frequency_results,
    phase_results=phase_results
)
```

### Interacting with data
All functions for interacting with data have the same two first arguments: the session (discussed above) and the id of the spiral. For example, the `get_rf_data()` function takes these two paramaters, and a key used to address the data:
```python
...
get_rf_data(session, 1, 'bandwidth')
...
```

### All available functions
```python
# Returns a sqlalchemy.orm.session.Session object. Required for all other functions
# Takes a path to the database file
connect(db)

# Creates a spiral. All parameters except `session` must be passed by keyword
create_spiral(session, *, id, nodal_data, frequency_data, phase_data)

# Deletes a spiral from the database. Will throw an exception if the object does not exist
delete_spiral(session, id)

# Gets a piece of data from the rf_data dictionary. `key` is a string 
get_rf_data(session, id, key)

# Deletes an item from the rf_data dictionary by key. 'key' is a string
delete_rf_data_item(session, id, key)

# Gets the whole rf_data dictionary
get_rf_data_dict(session, id)

# Writes `val` to `key` in the rf_data dictionary. `key` is a string, `val` can be anything
# If the key already exists, its current value will be overwritten
update_rf_data_dict(session, id, key, value)

# The following three are counterparts of the rf_data functions
get_vision_data(session, id, key)
get_vision_data_dict(session, id, key)
delete_vision_data_item(session, id, key)
update_vision_data_dict(session, id, key, value)

# Looks up the `column_name` column in the specified object and returns the data
# as a pandas dataframe. 
# `column_name` is a string in ['nodes', 'frequency_results', 'phase_results']
column_as_data_frame(session, id, column_name)
```
