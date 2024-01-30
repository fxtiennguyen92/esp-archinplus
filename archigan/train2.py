import glob

import os
import cv2
import geopandas as gpd
from shapely.geometry import Polygon, MultiPolygon
from svglib import svglib
from collections import defaultdict

from archigan.datalayer import Layer
from archigan.pipeline import ArchiPipeline
from archigan.boston import ParcelInputLayer, ParcelOutputLayer, parse_GIS_bostonbuildings_2016
from archigan.cvc_fp import FootprintInputLayer, RepartitionInputLayer, RepartitionOutputLayer, parse_CVC_FP_svg

svgs = glob.glob('datasets/ImagesGT2/*.svg')
classes = (
    'Door',
    'Window',
    'Room',
    'Wall',
    'Separation',
    'Parking',
)

def find_polygons_and_classes(element):
    if hasattr(element, 'getContents'):
        for sub_element in element.getContents():
            find_polygons_and_classes(sub_element)
    elif hasattr(element, 'class_'):
        # Check if the element has a class attribute
        if element.class_ == 'Wall':
            print("Found Polygon with class 'Wall'")

for svg in svgs:
    drawing = svglib.svg2rlg(svg)
    for py in drawing.getContents():
        print(dir(py))
        for i in py.__class__:
            print(str(i))
        #find_polygons_and_classes(py)
    break

#parsed = {svg: parse_CVC_FP_svg(svg, classes) for svg in svgs}
#directory = './tmp/'

#FootprintInputLayer.samples_to_imgs(parsed, directory)
#RepartitionInputLayer.samples_to_imgs(parsed, directory)
#RepartitionOutputLayer.samples_to_imgs(parsed, directory)