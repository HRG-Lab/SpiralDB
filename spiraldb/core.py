import os
import json
import pandas
from io import StringIO

from .database import Spiral

def create_spiral(session, *, id, nodes, frequency_results, phase_results):
    ''' Creates a spiral with nodes, frequency, and phase data
    Has empty rf and vision json objects
    '''
    if session is None:
        raise ConnectionError("No connection to database")
    # TODO is more error checking necessary?

    with open(nodes) as f:
        nodes = f.read()

    with open(frequency_results) as f:
        frequency_results = f.read()

    with open(phase_results) as f:
        phase_results = f.read()

    if session.query(Spiral).get(id) is None:
        new_spiral = Spiral(
            id=id,
            nodes=nodes,
            frequency_results=frequency_results,
            phase_results=phase_results,
            # These fields cannot be null, so populate with empty JSON object
            rf_data = json.dumps({}), 
            vision_data = json.dumps({}),
        )

        session.add(new_spiral)
        session.commit()

    return id

def delete_spiral(session, id):
    if session is None:
        raise ConnectionError("No connection to database")
    # TODO is more error checking necessary?

    spiral = session.query(Spiral).get(id)

    if spiral is None:
        # Is this necessary? If we're trying to delete a spiral
        # and it turns out it doesn't exist, haven't we...succeeded?
        raise LookupError("No object to delete")

    session.delete(spiral)
    session.commit() 

    # For now, returns id of deleted spiral
    return id

def get_rf_data(session, id, key):
    return get_rf_data_dict(session, id)[key]

def get_rf_data_dict(session, id):
    if session is None:
        raise ConnectionError("No connection to database")
    # TODO is more error checking necessary?

    spiral = session.query(Spiral).get(id)

    if spiral is None:
        raise LookupError("Spiral {:d} does not exist".format(id))

    return json.loads(spiral.rf_data)

def update_rf_data(session, id, key, value):
    if session is None:
        raise ConnectionError("No connection to database")
    # TODO is more error checking necessary?

    spiral = session.query(Spiral).get(id)

    if spiral is None:
        raise LookupError("Spiral {:d} does not exist".format(id))

    rf_data = json.loads(spiral.rf_data)
    rf_data[key] = value

    spiral.rf_data = json.dumps(rf_data)
    session.commit()

def delete_rf_data_item(session, id, key):
    rf_data = get_rf_data_dict(session, id)
    del rf_data[key]
    _replace_rf_data_dict(session, id, rf_data)

def _replace_rf_data_dict(session, id, rf_data):
    if session is None:
        raise ConnectionError("No connection to database")
    # TODO is more error checking necessary?

    spiral = session.query(Spiral).get(id)

    if spiral is None:
        raise LookupError("Spiral {:d} does not exist".format(id))

    spiral.rf_data = json.dumps(rf_data)
    session.commit()

def get_vision_data(session, id, key):
    return get_vision_data_dict(session, id)[key]

def get_vision_data_dict(session, id):
    if session is None:
        raise ConnectionError("No connection to database")
    # TODO is more error checking necessary?

    spiral = session.query(Spiral).get(id)

    if spiral is None:
        raise LookupError("Spiral {:d} does not exist".format(id))

    return json.loads(spiral.vision_data)

def update_vision_data(session, id, key, value):
    if session is None:
        raise ConnectionError("No connection to database")
    # TODO is more error checking necessary?

    spiral = session.query(Spiral).get(id)

    if spiral is None:
        raise LookupError("Spiral {:d} does not exist".format(id))

    vision_data = json.loads(spiral.vision_data)
    vision_data[key] = value

    spiral.vision_data = json.dumps(vision_data)
    session.commit()

def delete_vision_data_item(session, id, key):
    vision_data = get_vision_data_dict(session, id)
    del vision_data[key]
    _replace_vision_data_dict(session, id, vision_data)

def _replace_vision_data_dict(session, id, vision_data):
    if session is None:
        raise ConnectionError("No connection to database")
    # TODO is more error checking necessary?

    spiral = session.query(Spiral).get(id)

    if spiral is None:
        raise LookupError("Spiral {:d} does not exist".format(id))

    spiral.vision_data = json.dumps(vision_data)
    session.commit()

def column_as_data_frame(session, id, column_name):
    if column_name not in {'nodes', 'frequency_results', 'phase_results'}:
        raise KeyError("Invalid column name: {:s}".format(column_name))
    
    query = session.query(Spiral).get(id)
    if column_name == 'nodes':
        df = pandas.read_csv(StringIO(query.nodes), sep=',', header=None)
    elif column_name == 'frequency_results':
        df = pandas.read_csv(StringIO(query.frequency_results), sep=',', header=0)
    elif column_name == 'phase_results':
        df = pandas.read_csv(StringIO(query.phase_results), sep=',', header=0)

    return df