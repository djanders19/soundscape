'''mixer.py
Name: David J. Anderson
Email: djanders@bowdoin.edu
Date: 5/30/2016 - 


This program takes two sound tracks and mixes them together in a random way
so that they will sound different every time. It is designed to be used at
the Maine Maritime Museum installation, and is not licensed for other use.'''

from pydub import AudioSegment
from pydub.playback import play
import random

def random_number_generator():
    '''This will get the random seed information and produce a pan value to be
    used with pydub.'''
    return random.randrange(0, 100) / 100


def get_tracks_as_segments(track1, track2):
    '''gets the mp3 tracks that are to be mixed across the soundscape'''
    sound1 = AudioSegment.from_file(track1)
    sound2 = AudioSegment.from_file(track2)
    return (sound1, sound2)


def set_pans_and_overlay(sounds):
    '''sets the pan for each track based on the results of 
    random_number_generator'''
    panned_right = sounds[0].pan(random_number_generator())
    panned_left = sounds[1].pan(-random_number_generator())
    overlay = panned_right.overlay(panned_left)
    return overlay


def main():
	'''stitches everything together'''
	track1 = input('What is the first track you would like to mix? ')
	track2 = input('What is the second track you would like to mix? ')

	sounds = get_tracks_as_segments(track1, track2)

	sound = set_pans_and_overlay(sounds)
	play(sound)

main()

