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

from pydub import AudioSegment
from pydub.playback import play
from os import listdir
from os.path import isfile, join
import random
import pyowm

def random_seed_generator():
	'''This will get the random seed information based on weather in the area'''
	try: # Access weather data using the pyowm package and OpenWeatherMaps API
		owm = pyowm.OWM(API_key='48ac48853b61a5d4e7b59a5a6aaac2d4')
		observe_weather = owm.weather_at_place('Bath,us')
		weather = observe_weather.get_weather()
		wind = weather.get_wind()
		windspeed = wind['speed']
		print(windspeed)
	# In case internet goes out at installation, we include this exception:
	except:
		windspeed = random.random()

	return windspeed


def get_tracks_as_randomized_list():
	'''gets the naemes of the mp3 tracks that are to be mixed across the 
	soundscape and and returns them as a list'''
	# Create a list of input track names using pydub
	files = [f for f in listdir('more_clips') if isfile(join('more_clips', f))]
	random.shuffle(files)
	return files


def get_audio_segments_make_playlist(randomized_ls_of_files):
	playlist = AudioSegment.empty()
	#random.seed(random_seed_generator)
	for filename in randomized_ls_of_files:
		clip_to_be_appended = 'more_clips/' + filename
		print(clip_to_be_appended.upper())
		seg_to_be_appended = AudioSegment.from_file(clip_to_be_appended)
		panned_to_be_appended = seg_to_be_appended.pan(random.choice([-1, 1]))
		choice = random.randrange(1, 4)
		if choice == 1:
			print("Appending")
			playlist += panned_to_be_appended
		else:
			mix_position = len(playlist) - len(panned_to_be_appended)
			if mix_position > 0:
				print("Overlaying at", mix_position)
				playlist = \
				playlist.overlay(panned_to_be_appended, position=mix_position)
			else:
				print("Appending")
				playlist += panned_to_be_appended
	return playlist


def main():
	'''stitches everything together'''
	randomized_ls_of_files = get_tracks_as_randomized_list()

	track_to_play = get_audio_segments_make_playlist(randomized_ls_of_files)
	print(len(track_to_play))
	play(track_to_play)

main()
	

