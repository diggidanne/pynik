# coding: utf-8

from __future__ import with_statement
import pickle
import sys
import re
import utility
from plugins import Plugin
from commands import Command
import command_catcher

class Spot(object):
	def __init__(self, protocol, spotify_resource):
		self.prot = protocol
		self.spot = spotify_resource

class SpotifyConvertPlugin(Command): 
	hooks = ['on_privmsg']   
	spots = {}
	spot_list = []

	def __init__(self):
		pass
	
	def on_privmsg(self, bot, source, target, message):
		m = re.search(r'http://open\.spotify\.com/track/(\w+)', message)
		prot = 'http'
		if not m: 
			prot = 'spotify'
			m = re.search(r'spotify:track:(\w+)', message)
		if m:
			spot = m.group(1)
			self.spots[target] = Spot(prot, spot)
			self.save_last_spot(target)

	def save_last_spot(self, target):
		self.spot_list.append(self.spots[target])
		self.save_spots()
	
	def trig_spotify(self, bot, source, target, trigger, argument):
		if target in self.spots.keys():
			m = self.spots[target].title

			if m:
				return m
			else:
				return 'I can\'t find a title for ' + self.urls[target].url
		else:
			return 'I haven\'t seen any urls here yet.'

	def save_spots(self):
		file = open('data/spots.txt', 'w')
		p = pickle.Pickler(file)
		p.dump(self.spot_list)
		file.close()

	def load_spotslf):
		try:
			with open('data/spots.txt', 'r') as file:
				self.spot_list = pickle.Unpickler(file).load()
		except IOError:
			pass

	def on_load(self):
		self.load_spots()

	def save(self):
		pass

	def on_modified_options(self):
		self.save()
