'''mixer.py
Name: David J. Anderson
Email: djanders@bowdoin.edu
Date: 5/30/2016 - 5/31/2016


This program takes two mp3s and mixes them together in a random way
so that they will sound different every time, using weather data as a seed. 
It is designed to be used at the Maine Maritime Museum installation, 
envisioned by Erin Johnson and built by Erin Johnson and David Anderson. 
It uses the pydub module by jiarro  (https://github.com/jiaaro) to manage audio
and the pyowm package by csparpa (https://github.com/csparpa) to collect data 
from OpenWeatherMap (http://openweathermap.org)'''

# This version just swaps the tracks; no blending

from pydub import AudioSegment
from pydub.playback import play
import random
import pyowm

def random_number_generator():
	'''This will get the random seed information and produce a pan value to be
	used with pydub.'''
	try: # Access weather data using the pyowm package and OpenWeatherMaps API
		owm = pyowm.OWM(API_key='48ac48853b61a5d4e7b59a5a6aaac2d4')
		observe_weather = owm.weather_at_place('Bath,us')
		weather = observe_weather.get_weather()
		wind = weather.get_wind()
		windspeed = wind['speed']
		print(windspeed)
	except:
		windspeed = random.random()

	# Generate two random numbers using the windspeed as a seed:
	# random.seed(a=windspeed) <-- Uncomment this once weather is worked out
	rand_num1 = random.choice([-1, 1])
	rand_num2 = random.choice([-1, 1])
	rand_num3 = random.choice([-1, 1])
	rand_num4 = random.choice([-1, 1])

	# Return both random numbers in a tuple structure
	random_nums = (rand_num1, rand_num2, rand_num3, rand_num4)
	print(random_nums)
	return random_nums


def get_tracks_as_segments(track1, track2, track3, track4):
	'''gets the mp3 tracks that are to be mixed across the soundscape and
	and returns them as a tuple of AudioSegment objects'''
	# Create workable audiosegments from the input tracks using pydub
	sound1 = AudioSegment.from_file(track1)
	sound2 = AudioSegment.from_file(track2)
	sound3 = AudioSegment.from_file(track3)
	sound4 = AudioSegment.from_file(track4)
	sounds = (sound1, sound2, sound3, sound4)
	return sounds


def set_pans_and_overlay(sounds):
	'''sets the pan (L/R balance) for each track based on the results of 
	random_number_generator. Returns an AudioSegment object'''
	random_nums = random_number_generator()

	# Randomly set each track's L/R balance:
	panned_1= sounds[0].pan(random_nums[0])
	panned_2 = sounds[1].pan(random_nums[1])
	panned_3 = sounds[2].pan(random_nums[2])
	panned_4 = sounds[3].pan(random_nums[3])

	# Overlay the tracks, mixing them together:
	overlay1 = panned_1.overlay(panned_2)
	overlay2 = panned_3.overlay(panned_4)
	total_overlay = overlay1.overlay(overlay2)
	return total_overlay


def main():
	'''stitches everything together'''
	track1 = '4mp3s/group1.mp3'
	track2 = '4mp3s/group2.mp3'
	track3 = '4mp3s/group3.mp3'
	track4 = '4mp3s/group4.mp3'

	sounds = get_tracks_as_segments(track1, track2, track3, track4)

	sound = set_pans_and_overlay(sounds)
	play(sound)

while True:
	main()

