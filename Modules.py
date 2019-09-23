#########################_Imports_############################
# Import section for extracting jpeg image information. This #
# includes gps stamps as well as time and date.              #
##############################################################

# Written in Python 2.7.15 using pip 19.2.3
# Older version of pip used for try and except pip install method.
# Check pip version via command line by using pip --version command

# Import os and lisdir to idenfify image files in Image folder
import os

# import listdir to identify both files and folder paths 
# in a given location
from os import listdir

# import isfile and join to identify files only in 
# a givem location
from os.path import isfile, join

# Import sys for modifying paths to search for data
import sys

# Import subprocess for installing GPSPhoto
import subprocess

#***GPSPhoto failed to import without pip***
try:
	import GPSPhoto
except:
	print ('Failed to import GPSPhoto...\nWill use subprocess...')
	subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'GPSPhoto'])
import GPSPhoto

#***gpsohoto failed to import without:***
# 		exifread and piexif

#Import exifread
try:
	import exifread
except:
	print ('Failed to import exifread...\nWill use subprocess...')
	subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'exifread'])
import exifread

#Import piexif
try:
	import piexif
except:
	print ('Failed to import piexif...\nWill use subprocess...')
	subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'piexif'])
import piexif

#Import Image
try:
	import Image
except:
	print ('Failed to import Image...\nWill use subprocess...')
	subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'Image'])
# import Image

# Can now import gpsphoto since other dependancies have been met 
from GPSPhoto import gpsphoto

# Import datetime for date conversion

from datetime import datetime

# Import module for progress bar

try:
	import tqdm
except:
	print ('Failed to import tqdm...\nWill use subprocess...')
	subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'tqdm'])
import tqdm

# Import pandas

try:
	import pandas as pd
except:
	print ('Failed to import pandas...\nWill use subprocess...')
	subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'pandas'])
import pandas as pd

# If pip main fails, check pip version and find alternative pip install method.
