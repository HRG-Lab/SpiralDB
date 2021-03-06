import os
import json
import pandas

from context import spiraldb

db = "tests/test.db"
session = spiraldb.connect(db)

def test_insert():
    example_data_path = os.path.join(os.getcwd(), "tests", "ExampleData")
    nodal_data_path = os.path.join(example_data_path, "NODAL-COORDINATES-spiral_contour_image_18.txt")
    frequency_results = os.path.join(example_data_path, "FREQUENCY-RESULTS-spiral_contour_image_18.csv")
    phase_results = os.path.join(example_data_path, "PHASE-RESULTS-spiral_contour_image_phase_18.csv")

    spiraldb.create_spiral(
        session,
        id=18,
        nodes=nodal_data_path,
        image_path="2_X_13660_Y_5000.jpg",
        frequency_results=frequency_results,
        phase_results=phase_results
    )

    assert session.query(spiraldb.Spiral).get(18) is not None

def test_update_image_path():
    spiraldb.update_image_path(session, 18, '2_X_13660_Y_5001.jpg')
    assert session.query(spiraldb.Spiral).get(18).image_path == '2_X_13660_Y_5001.jpg'

def test_image_path():
    image_path = spiraldb.image_path(session, 18)
    assert image_path == '2_X_13660_Y_5001.jpg'

def test_update_rf_data():
    spiraldb.update_rf_data(session, 18, 'bandwidth', 5)
    spiraldb.update_rf_data(session, 18, 'center', 2)
    rf_data = json.loads(session.query(spiraldb.Spiral).get(18).rf_data)
    assert rf_data == {
        'bandwidth': 5,
        'center': 2
    }

def test_get_rf_data():
    assert spiraldb.get_rf_data(session, 18, 'bandwidth') == 5
    
def test_delete_rf_data_item():
    spiraldb.delete_rf_data_item(session, 18, 'center')
    rf_data = json.loads(session.query(spiraldb.Spiral).get(18).rf_data)
    assert rf_data == {
        'bandwidth': 5
    }

def test_update_vision_data():
    spiraldb.update_vision_data(session, 18, 'thing', 'is thing')
    spiraldb.update_vision_data(session, 18, 'thing2', 'is 2 thing')
    vision_data = json.loads(session.query(spiraldb.Spiral).get(18).vision_data)
    assert vision_data == {
        'thing': 'is thing',
        'thing2': 'is 2 thing'
    }

def test_get_vision_data():
    assert spiraldb.get_vision_data(session, 18, 'thing') == 'is thing'
    
def test_delete_vision_data_item():
    spiraldb.delete_vision_data_item(session, 18, 'thing2')
    vision_data = json.loads(session.query(spiraldb.Spiral).get(18).vision_data)
    assert vision_data == {
        'thing': 'is thing',
    }

def test_column_as_data_frame():
    df = spiraldb.column_as_data_frame(session, 18, 'nodes')
    assert list (df.columns.values) == [0, 1]
    assert isinstance(df, pandas.DataFrame)
    assert len(df.columns) == 2

    df = spiraldb.column_as_data_frame(session, 18, 'frequency_results')
    assert list(df.columns.values) == ['Freq [GHz]', 'dB(S(FloquetPort2,FloquetPort1)) []']
    assert isinstance(df, pandas.DataFrame)
    assert len(df.columns) == 2

    df = spiraldb.column_as_data_frame(session, 18, 'phase_results')
    assert list(df.columns.values) == ['Freq [GHz]', 'cang_deg(S(FloquetPort1,FloquetPort1)) [deg]']
    assert isinstance(df, pandas.DataFrame)
    assert len(df.columns) == 2

def test_delete():
    spiraldb.delete_spiral(session, 18)
    assert session.query(spiraldb.Spiral).get(18) is None

session.close()