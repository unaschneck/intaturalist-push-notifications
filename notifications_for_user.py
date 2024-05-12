from pyinaturalist import *
import string
from datetime import datetime, timedelta

user = "test-user"
last_check_datetime = datetime.now() - timedelta(days=1, hours=3, minutes=1)

def getObservations(user_id):
	recent_observations = get_observations(user_id=user_id, d1=last_check_datetime)
	observations = recent_observations["results"]
	for observation in observations:
		#pprint(observation)
		id_guess = observation["species_guess"]
		if id_guess is None:
			id_guess = observation["taxon"]["preferred_common_name"]
		id_guess = string.capwords(id_guess)
		print(f"{user} spotted: {id_guess}")
		previous_observations = get_observations(user_id=user_id, taxon_name=id_guess)["results"]
		#pprint(previous_observations)
		if len(previous_observations) > 1 and len(previous_observations) <= 14:
			print(f"Seen before {len(previous_observations)} times")
		if len(previous_observations) > 15:
			print(f"Seen before a lot! ({len(previous_observations)} times)")
		if len(previous_observations) <= 1:
			print("Never seen before")
		print(observation["place_guess"])
		print(observation["uri"])
		print("\n")
		#break
		"""
		print(observation.keys())
		print("\n")
		inaturalist_id = observation["id"]
		print(f"id = {inaturalist_id}")
		inaturalist_created_at = observation["created_at"]
		print(inaturalist_created_at)
		inaturalist_id_count = observation["identifications_count"]
		print(f"id count = {inaturalist_id_count}")
		inaturalist_species_guess = observation["species_guess"]
		if inaturalist_species_guess is None: inaturalist_species_guess = "Something Mysterious"
		print(f"species_guess = {inaturalist_species_guess}")
		inaturalist_location = observation["place_guess"]
		print(inaturalist_location)
		# something seen before (Again!) versus something new ("For the first time")
		inaturalist_observation_photos = observation["observation_photos"]
		inaturalist_square_img_url = []
		if len(inaturalist_observation_photos) > 0:
			for observation_photo in inaturalist_observation_photos:
				inaturalist_square_img_url.append(observation_photo["photo"]["url"])
		print(inaturalist_square_img_url)
		inaturalist_observation_url = f"https://www.inaturalist.org/observations/{inaturalist_id}"
		print(inaturalist_observation_url)
		break
		"""
	return observations

if __name__ == '__main__':
	getObservations(user)
