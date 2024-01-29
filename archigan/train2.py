import glob

import os
import cv2
import geopandas as gpd
from shapely.geometry import Polygon, MultiPolygon
from svglib.svglib import svg2rlg
from collections import defaultdict

from archigan.datalayer import Layer
from archigan.pipeline import ArchiPipeline
from archigan.boston import ParcelInputLayer, ParcelOutputLayer, parse_GIS_bostonbuildings_2016
from archigan.cvc_fp import FootprintInputLayer, RepartitionInputLayer, RepartitionOutputLayer

stages = (
    'ParcelInputLayer',
    'ParcelOutputLayer',
    'FootprintInputLayer',
    'RepartitionInputLayer',
    'RepartitionOutputLayer',
)
layers = [os.path.join('./prepared/parcel2floorplan_5layer', layer) for layer in stages]
stages = [(j - 1, j) for j in range(1, len(layers))]
stages.pop(1)
directory = './prepared/parcel2floorplan_3stage'

print(layers, stages, directory)
pipeline = ArchiPipeline(layers, stages)

pipeline.setup_training(directory)