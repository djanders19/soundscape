'''mixer.py
Name: David J. Anderson
Email: djanders@bowdoin.edu
Date: 5/30/2016 - 5/31/2016


This program takes two sound tracks and mixes them together in a random way
so that they will sound different every time. It is designed to be used at
the Maine Maritime Museum installation, envisioned by Erin Johnson and built
by Erin Johnson and David Anderson. It uses the pydub module by jiarro 
(https://github.com/jiaaro) to manage audio and the pyowm package by 
csparpa (https://github.com/csparpa) to collect data from 
OpenWeatherMap (http://openweathermap.org)'''

from pydub import AudioSegment
from pydub.playback import play
import random
import pyowm

def random_number_generator():
    '''This will get the random seed information and produce a pan value to be
    used with pydub.'''
    # Access weather data using the pyowm package and OpenWeatherMaps API
    owm = pyowm.OWM(API_key='48ac48853b61a5d4e7b59a5a6aaac2d4')
    observe_weather = owm.weather_at_place('Bath,us')
    weather = observe_weather.get_weather()
    wind = weather.get_wind()
    windspeed = wind['speed']
    print(windspeed)

    # Generate two random numbers using the windspeed as a seed:
    random.seed(a=windspeed)
    random_number1 = random.randrange(-100, 100) / 100
    random_number2 = random.randrange(-100, 100) / 100

    # Return both random numbers in a tuple structure
    random_nums = (random_number1, random_number2)
    return random_nums


def get_tracks_as_segments(track1, track2):
    '''gets the mp3 tracks that are to be mixed across the soundscape and
    and returns them as a tuple of AudioSegment objects'''
    # Create workable audiosegments from the input tracks using pydub
    sound1 = AudioSegment.from_file(track1)
    sound2 = AudioSegment.from_file(track2)
    sounds = (sound1, sound2)
    return sounds


def set_pans_and_overlay(sounds):
    '''sets the pan (L/R balance) for each track based on the results of 
    random_number_generator. Returns an AudioSegment object'''
    random_nums = random_number_generator()
    panned_1= sounds[0].pan(random_nums[0])
    panned_2 = sounds[1].pan(random_nums[1])
    overlay = panned_1.overlay(panned_2)
    return overlay


def main():
	'''stitches everything together'''
	# These are both just test files on my computer right now, but will be
	# replaced with the correct files when I get my handos on them:
	track1 = 'bach_1.mp3'
	track2 = 'bach_2.mp3'

	sounds = get_tracks_as_segments(track1, track2)

	sound = set_pans_and_overlay(sounds)
	play(sound)

while True:
	main()

