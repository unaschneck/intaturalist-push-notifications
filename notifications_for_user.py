import sys                                             # collect command line arguments
import math                                            # round time to next nearest minute (rounds up)
import string                                          # capitalize each word in a string
import requests                                        # send ntfy request, collect recent observations
from datetime import datetime, timedelta, time         # track time and collection observations

# Command Line Arguments set from observation_reporter.yml
user = sys.argv[1]
ntfy_id = sys.argv[2]
last_workflow_ran_at = datetime.strptime(sys.argv[3], "%Y-%m-%dT%H:%M:%SZ") # UTC

def getObservations(user_id, last_check):
	recent_observations = requests.get(f"https://api.inaturalist.org/v1/observations?user_id={user}&d1={time_range_to_check}").json()
	observations = recent_observations["results"]
	for observation in observations:

		# Identification with common name based on best guess
		id_guess = observation["species_guess"]
		if id_guess is None:
			if observation["taxon"] is None:
				id_guess = "Something Strange"
			if "preferred_common_name" in observation["taxon"].keys():
				id_guess = observation["taxon"]["preferred_common_name"]
			elif "name" in observation["taxon"].keys():
				id_guess = observation["taxon"]["name"]
		id_guess = string.capwords(id_guess)

		# Track if observation is new or previously seen
		seen_previous = ' ' # default
		if id_guess != "Something Strange":
			previous_observations = requests.get(f"https://api.inaturalist.org/v1/observations?user_id={user}&taxon_name={id_guess}").json()["results"]

			if len(previous_observations) > 1 and len(previous_observations) <= 14:
				seen_previous = " (again!) "
			if len(previous_observations) >= 15:
				seen_previous = " (a lot!) "
			if len(previous_observations) <= 1:
				seen_previous = " (for the first time!) "

		# Retrieve information about location, link to observation, and default img
		location_guess = "a Strange Place"
		if observation["place_guess"] is not None:
			location_guess = observation["place_guess"]

		observation_link = "www.inaturalist.org" # default
		if observation["uri"] is not None:
			observation_link = observation["uri"]

		img_url = "https://static.inaturalist.org/wiki_page_attachments/3154-original.png" # default
		if observation["taxon"]["default_photo"] is not None:
			img_url = observation["taxon"]["default_photo"]["square_url"]

		taxon_id = "unknown" # default
		if observation["taxon"]["iconic_taxon_name"] is not None:
			taxon_id = observation["taxon"]["iconic_taxon_name"]

		# Send observation as request
		observation_data = f"{user} spotted {id_guess}{seen_previous}in {location_guess}"
		print(f"Sending new observation: {id_guess}")
		sendRequest(observation_data, taxon_id, observation_link, img_url)

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
	if "(for the first time!)" in data_string: # first time observation
		additional_tags = ", star2"
	if "(a lot!)" in data_string: # multiple observations
		additional_tags = ", fire"

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
