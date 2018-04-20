# WeatherRoof

WeatherRoof.py is a simple Python3 script designed to work with Raspbian to  take pictures at a regular interval using the Pi Camera by the Raspberry Pi Foundation.  

This script is being used on [weatherroof.com](htps://weatherroof.com/).


# Initial Setup and Configuration

## Requirements
The following setup is working for me, other distributions and/or cameras may work but have not been tested.

- Raspberry Pi running Raspbian (Currently I'm using Stretch Headless)
- Pi Camera
- Python3 with `picamera` library. Some other libraries such as `datetime`, `ftplib`, and `os` are used but should be installed by default.  
- For S3 support install `boto3`. For daylight only setting install `astral`.

## Detailed Setup Steps

### Setup the Raspberry Pi, Rasbian, and Pi Camera

1) Set up a Raspberry Pi with Raspbian and connect to Wifi or plugin an ethernet cable.

If you get stuck see the following guides provided by the Raspberry Pi Foundation.  

- [Hardware Setup]( https://www.raspberrypi.org/learning/hardware-guide/)
- [Software Setup](https://www.raspberrypi.org/learning/software-guide/)
 - [Installing Rasbian with Noobs](https://www.raspberrypi.org/learning/software-guide/quickstart/) (beginner friendly)
  - [Installing Rasbian Manually](https://www.raspberrypi.org/documentation/installation/installing-images/README.md)
- [Connect to Wifi]()
 - [Using Graphical User Interface](https://www.raspberrypi.org/learning/software-guide/wifi/) (beginner friendly)
 - [Using Command Line](https://www.raspberrypi.org/documentation/configuration/wireless/wireless-cli.md) (headless)

2) Connect a Pi Camera
([Official Getting Started Guide](https://www.raspberrypi.org/learning/getting-started-with-picamera/))

### Install Software and Libraries
3) Open the Terminal and run the following command to make sure you have the required Python packages.
`apt-get install python3 python3-pip`   

**Note**: You may may need to run `sudo` before each command in this guide depending on which user you are logged in as.

4) Make sure you have the PiCamera Library installed
`pip3 install picamera`

5) Install optional libraries.

If you plan to upload to Amazon S3 you'll need to install the `boto3` which handles all the heavy lifting to Amazon Web Services with this command. `pip3 install boto3`

To use the daylight feature  which allows you to stop taking pictures at night you'll need `astral` which also requires the `requests` package. This library uses your location for real time dawn/dusk detection.
`pip3 install astral requests`

To install both enter the following command:
`pip3 install boto3 astral requests`

### Add and Configure `Weatherroof.py`
6) Now that the initial install is complete you will want to copy the `weatherroof.py` script onto your Pi.

 This can be done with a copy and paste of the code found in the `weatherroof.py` file into a new file on your pi to some location such as the home folder `~/` or Desktop (`/home/pi/Desktop` by default).

Alternatively, download the `zip` file from GitHub and extract it onto your SD card.

For more advanced usage and easier upgrades you may use Git to clone the repository using the `git clone` command. If you're new to Git check out [this guide](https://projects.raspberrypi.org/en/projects/getting-started-with-git).

To install `git` use the following command ` apt-get install git`

To clone the repository use `git clone https://github.com/BandonRandon/weatherroof.git`

7) Once you have the files saved locally navigate to them. Open `weatherroof.py` and edit the configuration options from just below the `Start Config` tag and ending at `End Config` as appropriate.

8) Now it's time to test things out! From the terminal navigate to the folder where your placed `weatherroof.py`

**Hint**: you can use `cd` to move around. For example: `cd /home/pi/weatherroof`
Once in the main folder run
`python3 weatherroof.py`

If things are setup correctly this will take a picture and upload it to the location(s) of your choice.

**Important**: for the initial test it's recommend to keep `use_remove_file = False` allowing the file to be saved locally. Otherwise the file will be deleted after creation.

### Automatically Capture Images
9) To have pictures taken at a regular interval set up a `cron job`. Alternatively, you could also use a loop within `weatherroof.py`.

Make the script executable by running the following command in the terminal:
`chmod -x /script/location/weatherroof.py`

Make sure to replace `/script/location` with where your script is being stored

Now that the file can be executed with a cron open your cron file with the following command:
` crontab -e`

To the bottom of this file add the following. You'll be able to customize how often the script runs as you like.

    # Run weatherroof.py every 5 minutes
    * * * * 5 /script/location/weatherroof.py

Again, remember to replace `/script/location` with your scripts location.

For more on cron refer to [this guide](https://www.raspberrypi.org/documentation/linux/usage/cron.md)

### Enjoy!
10) That it, congratulations on setting up `weatherroof.py`.

## Configuration
The `weatherrof.py` script is filled with inline comments to explain any settings. If anything is unclear please open an issue on GitHub and I'll take a look. Here are a few notes.

**filedir** will need to be writable by the user you are running the script as.

**Camera Settings** (`capture_image()`)  
You may need to adjust this function based on your needs. See the [Camera Library documentation](http://picamera.readthedocs.io/en/release-1.13/) for acceptable parameters specifically the [API Documentation](http://picamera.readthedocs.io/en/release-1.13/api_camera.html)

**Amazon S3**

- By default two images will be added each time the script is ran. The first being a unique timestamped version of the file and a second `latest.jpg` which will be replaced. This allows a website to always show the latest image by calling `bucket/latest.jpg`. If you have changed `filename` to be a static variable you may remove the `latest.jpg` part of the script.

- Files uploaded will be public and have a [StorageClass](https://aws.amazon.com/s3/storage-classes/) of `REDUCED REDUNDANCY`.

- Timestamped files will have a caching header of 30 days (2592000 seconds) and `latest.jpg` will have no caching headers added and will expire right away.

**astral**

- By default the astral library will take one parameter, the city. If your city is not on the [provided city list](https://astral.readthedocs.io/en/stable/index.html#cities) You will need to modify the script add your location. See the Astral Documentation for [locations](https://astral.readthedocs.io/en/stable/index.html#locations).

- Images will be taken between *Dawn* and *Dusk* by default you may change this to fit your projects needs. Again, see the [documentation](https://astral.readthedocs.io/en/stable/index.html) for accepted calculations.

# Your Next Steps
Hack the planet (or at least this script) to your liking. Use it as a learning ground to get your feet wet with Python. Already an expert? See Contributing for ways to help me improve it.

You may want to use the images uploaded to build a slideshow or learn to make a website site like https://weatherroof.com. The sky's the limit.

If you've found this script useful then please share it with your friends.

# Contributing
This script was developed for my specific use case. I hope others find it useful for their needs. If you have a problem using this script or want to make it better please open an issue or submit a Pull Request. I will always do my best to help out where I am able.


# To Do (future enhancements)
- Turn off LED light on Pi Camera ( V2 of Pi Camera doesn't have a LED so this only applies to V1 of the camera )
- Think about adding SFTP support
- Add more options to Amazon S3 in the script configuration such as StorageClass, caching headers, and the ability to control if `latest.jpg` gets added.
- Allow any location to be used for astral


# Changelog

*V3.1 2018-04-19*

 - First public release.
 - Adding this `README.md` file to help get people started.
 - Removed FTP Stuff, it wasn't tested since V1 (from 2014) and I have no intrest in supporting vanilla FTP. This may come back at a later date as SFTP.

*V3 2017-10-01*

 - Updated to work with Python 3.
 - Rewrite of large portion of the code base.
 - Updated boto to boto3.
 - Added automated daylight support instead of manual hour variables.
 - Removed support for LED lights. Now using PiZero W without headers.

*V2  2015-05-09*

 - Updated for Python 2.7.
 - Manual support for only taking pictures when it's light out.
 - Switched from using bulky LED lights to the [LEDBorg](https://www.piborg.org/ledborg) module.
 - Fixed S3 upload with boto.
 - Some code cleanup and slightly better documentation.

*V1 2014-04-27*

 - First time writing Python and things got messy.
 - Added Crontab and was taking images. Life is good.

# Thank You and Credit Where Credit is Due

Thanks for those this project builds on such as the Raspberry Pi Foundation, the Raspbian Team, Simon Kennedy for Astral, Dave Jones for PiCamera, and the Boto team.

Thanks also those who shared their thoughts in blog and forum posting that helped make this project possible.

# License

    WeatherRoof.py a Python Script which takes pictures using the Pi Camera
    Copyright (C) 2014-2018 Brooke. ( brooke.codes/contact )

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public Licensec
    along with this program.  If not, see <http://www.gnu.org/licenses/>
