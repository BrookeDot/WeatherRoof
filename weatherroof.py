#!/usr/bin/python

############################################################################
#
#    WeatherRoof.py a Python Script which takes pictures using the Pi Camera
#    Version 3.1
#    Copyright (C) 2014-2018 Brooke Dukes ( brooke.codes/contact )
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public Licensec
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
############################################################################

import picamera as cam
import datetime

date = datetime.datetime.now()

# ------------- Start Config -------------- #

# Path from script to local folder for image storage (with trailing slash)
filedir = '/home/pi/weatherroof/'

# Format of image filename
filename = 'image_' + date.strftime("%Y-%m-%d_%H-%M-%S") + '.jpg'

# Set image resolution
# V1 max: 2592×1944
# V2 max: 3280 x 2464
image_width = 800
image_height = 600

# Should we only take pictures when it's light out? Requires Arstral library
only_daylight_hours = True

# If true set your location below see: https://astral.readthedocs.io/en/stable/index.html#cities
location = 'Seattle'

# ------- Amazon S3 setup (requires the boto3 lib) ------- #
# ---- If True stores the image in defined S3 Bucket ----- #
use_s3_upload = True

# S3 bucket name
s3_bucket_name = 's3.bucket.name'
# Access key with access to above bucket
s3_access_key = 'S3_KEY_GOES_HERE'
# Secret access key associated with above key
s3_secret_access_key = 'S3_SECRET_HERE'

# ------- File deletion setup (require os) ------- #
# ---- If True removes image from local disk ---- #

use_remove_file = True

#-------------- End Config -------------- #

# ----  S3 Upload function ---- #
def s3_upload( file ):
	# Import aws lib (boto) and timedelta for our expiration
	import boto3

	# Connect to S3
	s3 = boto3.resource(
    's3',
    aws_access_key_id=s3_access_key,
    aws_secret_access_key=s3_secret_access_key,
)
	# Upload time-stamped file
	s3.Object( s3_bucket_name, filename ).put( ACL='public-read', Body=open(filedir + filename , 'rb' ), StorageClass='REDUCED_REDUNDANCY', CacheControl='max-age=2592000', ContentType='image/jpeg' )
	# Upload latest.jpg to be used on the site itself
	s3.Object( s3_bucket_name, 'latest.jpg' ).put( ACL='public-read', Body=open(filedir + filename , 'rb' ), StorageClass='REDUCED_REDUNDANCY', CacheControl='max-age=0', ContentType='image/jpeg' )

	return

# ---- Capture image function ---- #
def capture_image():

	# Set up camera
	camera = cam.PiCamera()

	# Flip image over as camera is upside down (:
	camera.vflip = True

	# Set camera brightness
	# camera.brightness = 40

	# Set meter mode
	camera.meter_mode = 'matrix'

	# Set camera resolution
	camera.resolution = ( image_width, image_height )

	# Store the image
	camera.capture( filedir + filename )

	# End picture capture
	return

# ---- Delete image function ---- #
def delete_file( file ):
	# Import OS Lib
	import os

	# Remove the file from the pi
	os.remove( filedir + file )

	# End file deletion
	return

# ---- Check_for daylight function ---- #
def lightOut():
	# Only do this if we care about daylight hours
	if only_daylight_hours:

		# Get daylight library and set things up
		from astral import Astral
		s = Astral()
		sun_data = s[location].sun( date=datetime.date( date.today().year, date.today().month, date.today().day ), local=True )

		dawn = sun_data[ 'dawn' ]
		dusk = sun_data[ 'dusk' ]

		# Check if it's between dawn and dusk an dif so return True
		if datetime.datetime.now().time() > datetime.datetime.time( dawn ) and datetime.datetime.now().time() < datetime.datetime.time( dusk ):
			return True

		else:
			# Dark out return False
			return False

	# We're not checking daylight return True
	else:
		return True


# ---- Here is where the magic happens ---- #

# Capture the image if it's daylight out
if  lightOut():
	capture_image() #capture the image

	# Check if S3 Upload is on and if so handle upload
	if use_s3_upload:
		s3_upload( filename )

	# Check if we should remove the rile and is so remove it.
	if use_remove_file:
		delete_file( filename )
