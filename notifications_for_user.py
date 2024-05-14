from pyinaturalist import *

import string
import sys
import requests
from time import sleep
from datetime import datetime, timedelta, time

# Command Line Arguments from observation_reporter.yml
user = sys.argv[1]
ntfy_id = sys.argv[2]
timestamp_hour = sys.argv[4]
timestamp_minute = sys.argv[5]

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
		location_guess = "a Strange Place"
		if observation["place_guess"] is not None:
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

	# Additional specialty tags
	timestamp_month = int(sys.argv[3])
	additional_tags = ""
	if timestamp_month == 10:
		# October
		additional_tags = ", jack_o_lantern"
	if timestamp_month == 11:
		# November
		additional_tags = ", turkey"
	if timestamp_month == 12:
		# December
		additional_tags = ", snowman_with_snow"

	# Set tags based on taxon, with default tag for unknown type
	if taxon in taxon_dict:
		taxon_tag = taxon_dict[taxon]
	else:
		taxon_tag = unknown

	all_tags = taxon_tag + additional_tags

	# testing request: testing314
	requests.post(f"https://ntfy.sh/{ntfy_id}",
				data=data_string,
				headers = {
					"Title": "New Observation!",
					"Tags": all_tags,
					"Click": url,
					"Icon":icon_img
				})

if __name__ == '__main__':
	timestamp_hour = int(timestamp_hour)
	timestamp_minute = int(timestamp_minute)

	last_timecheck = (0, 10) # last ten minutes (by default)
	if timestamp_hour == 14 and timestamp_minute < 13:
		# start of the day: collect all overnight observations
		last_timecheck = (13, 0) # last 13 hours

	print(f"Checking the last: {last_timecheck[0]} hours and {last_timecheck[1]} minutes")
	last_check_datetime = datetime.now() - timedelta(hours=last_timecheck[0], minutes=last_timecheck[1])
	getObservations(user, last_check_datetime)
