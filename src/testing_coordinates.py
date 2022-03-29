#!/usr/env bin python3
from datetime import datetime
from shapely.geometry import Point, shape
import json
import sys
import os

load_json = "/Users/bryanlonso/proyectos/django_project/src/static/peru_distritos.geojson"

if not os.path.isfile(load_json):
    sys.exit(3)

with open(load_json, 'r') as read_json:
    data = json.load(read_json)

point = Point(-77.015550, -12.147115)

for feature_coordinates in data['features']:
    try:
        polygon = shape(feature_coordinates['geometry'])
        if polygon.contains(point):
            column_shape = feature_coordinates['properties']
            print(column_shape)
    except:
        None
