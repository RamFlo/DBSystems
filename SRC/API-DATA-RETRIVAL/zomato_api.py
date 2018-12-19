import requests

from database_populator import DatabasePopulator

zomato_api_keys = ["321da0bc263eda93da9f3d9497876d2e",
                   "d7afaabbb3109389a42d21af7bb3b3a5",
                   "367e4e949648279a9951d011ee3a1f9d"]
user_key_header = "user-key"
zomato_base_url = "https://developers.zomato.com/api/v2.1/"
zomato_ny_city_id = "280"


def get_zomato_response(full_url_request, key):
    headers = {"Accept": "application/json", user_key_header: key}
    request = requests.post(full_url_request, headers=headers)
    return request.json()


def populate_cuisines():
    full_url_request = zomato_base_url + "cuisines?city_id=" + zomato_ny_city_id
    json_response = get_zomato_response(full_url_request, zomato_api_keys[2])
    cuisines_list = json_response['cuisines']

    populator = DatabasePopulator(table_name='Cuisines')
    for cuisine in cuisines_list:
        curr_cuisine = cuisine['cuisine']
        populator.insert_row(
            [curr_cuisine['cuisine_id'], curr_cuisine['cuisine_name']]
            )


def populate_establishments():
    full_url_request = zomato_base_url + "establishments?city_id=" + \
                        zomato_ny_city_id
    json_response = get_zomato_response(full_url_request, zomato_api_keys[2])
    establishment_list = json_response['establishments']

    populator = DatabasePopulator(table_name='Establishments')
    for establishment in establishment_list:
        curr_establishment = establishment['establishments']
        populator.insert_row(
            [curr_establishment['id'], curr_establishment['name']]
            )


def populate_restaurants(category_ids):
    # each query can return max of 20 results, and each search type can return
    # up to 100 results in total.
    # that means we need to generate as much as unique search types that will
    # allow us to get the maximum number of unique searches, in order to
    # maximize the number of restaurants we fetch (some unique searches
    # might return the same restaurants, but the database schema will
    # prevent duplicates
    # each api key is limited to 1000 calls per day
    # we pass the category_ids since its a value between 1-14 excluding 13,
    # this will help us iterate better and split the work between different
    # days

    # first, we fetch the id's which will help us to generate the unique
    # searches (cuisine_id, establishment_id)
    cuisine_ids = []
    cuisines_url = zomato_base_url + "cuisines?city_id=" + zomato_ny_city_id
    json_response = get_zomato_response(cuisines_url, zomato_api_keys[0])
    cuisines_list = json_response['cuisines']
    for cuisine in cuisines_list:
        cuisine_ids += [cuisine['cuisine']['cuisine_id']]

    establishment_ids = []
    establishment_url = zomato_base_url + "establishments?city_id=" + \
                        zomato_ny_city_id
    json_response = get_zomato_response(establishment_url, zomato_api_keys[0])
    establishment_list = json_response['establishments']
    for establishment in establishment_list:
        establishment_ids += [establishment['establishment']['id']]

    curr_key = 0
    query_count = 2
    total_restaurants = 0
    for category_id in category_ids:
        for establishment_id in establishment_ids:
            for cuisine_id in cuisine_ids:
                for offset in [x for x in range(0, 81, 20)]:
                    full_url_request = (zomato_base_url +
                                        "search?entity_id=%s" + \
                                        "&entity_type=city&start=%d" + \
                                        "cuisines=%d&establishment_type=%d" + \
                                        "&category=%d") % (zomato_ny_city_id,
                                                           offset, cuisine_id,
                                                           establishment_id,
                                                           category_id)
                    json_response = get_zomato_response(full_url_request,
                                                        zomato_api_keys[
                                                            curr_key])
                    query_count += 1
                    if query_count > 1000:
                        curr_key += 1
                    if curr_key == 3:
                        print(query_count)
                        print(total_restaurants)
                        return (category_id, query_count)

                    if len(json_response) == 0:
                        continue

                    restaurants = json_response['restaurants']
                    for restaurant in restaurants:
                        populate_restaurant(restaurant)
                    total_restaurants += len(restaurants)
                    if query_count % 100 == 0:
                        print("------ STATUS ------")
                        print(query_count)
                        print(total_restaurants)

    return


# TODO (mickey/nitzan): implement method
# the method should try and insert the restaurant to the Restaurants table,
# get the restaurants establishments from the json, compare them to existing
# establishment in the Establishments tables, and if there is a match,
# add the match to the RestaurantEstablishment table as well
def populate_restaurant(restaurant_json):
    return

