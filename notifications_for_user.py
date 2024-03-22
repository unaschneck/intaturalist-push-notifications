from pyinaturalist import *

user = "test-user"

def getObservations(user_id):
	total_results_dict = get_observations(user_id=user_id)
	observations = total_results_dict["results"]
	for observation in observations:
		print(observation.keys())
		print("\n")
		inaturalist_id = observation["id"]
		print(inaturalist_id)
		inaturalist_created_at = observation["created_at"]
		print(inaturalist_created_at)
		inaturalist_species_guess = observation["species_guess"]
		print(inaturalist_species_guess)
		inaturalist_location = observation["place_guess"]
		print(inaturalist_location)
		inaturalist_observation_photos = observation["observation_photos"]
		inaturalist_square_img_url = []
		if len(inaturalist_observation_photos) > 0:
			for observation_photo in inaturalist_observation_photos:
				inaturalist_square_img_url.append(observation_photo["photo"]["url"])
		print(inaturalist_square_img_url)
		inaturalist_observation_url = f"https://www.inaturalist.org/observations/{inaturalist_id}"
		print(inaturalist_observation_url)
		break
	return observations

if __name__ == '__main__':
	getObservations(user)
