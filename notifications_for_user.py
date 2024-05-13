from pyinaturalist import *

import string
import sys
import requests
from time import sleep
from datetime import datetime, timedelta, time

user = sys.argv[1]
nfty_id = sys.argv[2]
timestamp_hour = sys.argv[3]

def getObservations(user_id, last_check):
	recent_observations = get_observations(user_id=user_id, d1=last_check)
	observations = recent_observations["results"]
	for observation in observations:
		#pprint(observation)

		# Identification with common name based on best guess
		id_guess = observation["species_guess"]
		if id_guess is None:
			if "preferred_common_name" in observation["taxon"].keys():
				id_guess = observation["taxon"]["preferred_common_name"]
			elif "name" in observation["taxon"].keys():
				id_guess = observation["taxon"]["name"]
			else:
				id_guess = "Something Strange"
		id_guess = string.capwords(id_guess)

		# Track if observation is new or previously seen
		if id_guess != "Something Strange":
			previous_observations = get_observations(user_id=user_id, taxon_name=id_guess)["results"]
			#pprint(previous_observations)
			if len(previous_observations) > 1 and len(previous_observations) <= 14:
				seen_previous = " (again!) "
			if len(previous_observations) > 15:
				seen_previous = " (a lot!) "
			if len(previous_observations) <= 1:
				seen_previous = " (for the first time!) "

		# Retrieve information about location, link to observation, and default img
		location_guess = observation["place_guess"]
		observation_link = observation["uri"]
		img_url = observation["taxon"]["default_photo"]["square_url"]
		taxon_id = observation["taxon"]["iconic_taxon_name"]

		# Send observation as request
		observation_data = f"{user} spotted {id_guess}{seen_previous}in {location_guess}"
		print(f"Sending new observation: {id_guess}")
		sendRequest(observation_data, observation["taxon"]["iconic_taxon_name"], observation["uri"], observation["taxon"]["default_photo"]["square_url"])

def sendRequest(data_string, taxon, url, icon_img):
	plant = "herb"         # Plantae
	fungi = "mushroom"     # Fungi
	insect = "bug"         # Insecta
	bird = "parrot"        # Aves
	mammal = "rat"         # Mammalia
	fish = "tropical_fish" # Actinopterygii
	arachnid = "spider"    # Arachnida
	reptile = "snake"      # Reptilia
	amphibian = "frog"      # Amphibia
	mollusk = "snail"      # Mollusca
	other = "worm"         # Animalia
	unknown = "feet"       # Unknown

	taxon_dict = {"Plantae": plant,
				  "Fungi": fungi,
				  "Insecta": insect,
				  "Aves": bird,
				  "Mammalia": mammal,
				  "Actinopterygii": fish,
				  "Arachnida": arachnid,
				  "Reptilia": reptile,
				  "Amphibia": amphibian,
				  "Mollusca": mollusk,
				  "Animalia": other
				  }

	# Set tags based on taxon, with default tag for unknown type
	if taxon in taxon_dict:
		taxon_tag = taxon_dict[taxon]
	else:
		taxon_tag = unknown

	# testing request: testing314
	requests.post(f"https://ntfy.sh/{nfty_id}",
				data=data_string,
				headers = {
					"Title": "New Observation!",
					"Tags": taxon_tag,
					"Click": url,
					"Icon":icon_img
				})

if __name__ == '__main__':
	# day: UTC: 12-23,0-1 and night: 2-11
	timestamp_hour = int(timestamp_hour)
	if timestamp_hour >= 12 and timestamp_hour <= 23:
		last_timecheck = (0, 10)
	if timestamp_hour >= 0 and timestamp_hour <= 1:
		last_timecheck = (0, 10)
	if timestamp_hour >= 2 and timestamp_hour <= 11:
		last_timecheck = (4, 0)
	print(last_timecheck)
	last_check_datetime = datetime.now() - timedelta(hours=last_timecheck[0], minutes=last_timecheck[1])
	getObservations(user, last_check_datetime)
