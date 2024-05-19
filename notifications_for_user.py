from pyinaturalist import get_observations     # collect recent observations

import sys                                     # collect command line arguments
import math                                    # round time to next nearest minute (rounds up)
import string                                  # capitalize each word in a string
import requests                                # send ntfy request
from datetime import datetime, timedelta, time # track time and collection observations

# Command Line Arguments set from observation_reporter.yml
user = sys.argv[1]
ntfy_id = sys.argv[2]
last_workflow_ran_at = datetime.strptime(sys.argv[3], "%Y-%m-%dT%H:%M:%SZ") # UTC

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
	amphibian = "frog"     # Amphibia
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
	current_month = datetime.now().month
	additional_tags = ""
	if current_month == 10: # October
		additional_tags = ", jack_o_lantern"
	if current_month == 11: # November
		additional_tags = ", turkey"
	if current_month == 12: # December
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
	# Collect time since workflow last ran to determine how far to check for recent observations
	time_since_last_run = datetime.now() - last_workflow_ran_at
	time_interval = math.ceil(time_since_last_run.total_seconds() / 60)
	time_range_to_check = datetime.now() - timedelta(minutes=time_interval)

	print(f"Current Time:            {datetime.now()}")
	print(f"Last workflow ran at:    {last_workflow_ran_at}")
	print(f"Minutes Since Last Run:  {time_interval}")
	getObservations(user, time_range_to_check)
