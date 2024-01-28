import glob

import os
import cv2
import geopandas as gpd
from shapely.geometry import Polygon, MultiPolygon
from svglib.svglib import svg2rlg
from collections import defaultdict
from fiona.crs import from_epsg
#from tqdm import tqdm
from tqdm import tqdm_notebook as tqdm
import numpy as np

from archigan.datalayer import Layer
from archigan.pipeline import ArchiPipeline
from archigan.boston import ParcelInputLayer, ParcelOutputLayer, parse_GIS_bostonbuildings_2016
from archigan.cvc_fp import FootprintInputLayer, RepartitionInputLayer, RepartitionOutputLayer

path = 'datasets'
x, y = 800, 1000
parsed = parse_GIS_bostonbuildings_2016(path)
parsed = {f'boston_{(j + x):04d}': sample for j, sample in enumerate(parsed[x:y])}

directory = './tmp/'

print('N:', len(parsed))

ParcelInputLayer.samples_to_imgs(parsed, directory)
ParcelOutputLayer.samples_to_imgs(parsed, directory)



def parse_CVC_FP_svg(path, classes):
    """Parser for SVGs form the CVC-FP dataset:
        http://dag.cvc.uab.es/resources/floorplans/
    """
    drawing = svg2rlg(path)
    byclass = defaultdict(list)
    for cls in classes:
        for py in drawing.contents[0].contents:
            if py.__class__ == cls:
                loop = list(zip(py.points[::2], py.points[1::2]))
                byclass[py._class].append(loop)
    sample = {
        'byclass': byclass,
        'height': drawing.height,
        'width': drawing.width,
    }
    return sample

svgs = glob.glob('datasets/ImagesGT/*.svg')
classes = (
    'Door',
    'Window',
    'Room',
    'Wall',
    'Separation',
    'Parking',
)
parsed = {svg: parse_CVC_FP_svg(svg, classes) for svg in svgs}
directory = './tmp/'

FootprintInputLayer.samples_to_imgs(parsed, directory)
RepartitionInputLayer.samples_to_imgs(parsed, directory)
RepartitionOutputLayer.samples_to_imgs(parsed, directory)