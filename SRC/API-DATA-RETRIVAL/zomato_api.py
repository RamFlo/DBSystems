import requests

from database_populator import DatabasePopulator

zomato_api_keys = ["321da0bc263eda93da9f3d9497876d2e",
                   "d7afaabbb3109389a42d21af7bb3b3a5",
                   "367e4e949648279a9951d011ee3a1f9d",
                   "4c5c438e2b3e4e998d6856482b651583"]
user_key_header = "user-key"
zomato_base_url = "https://developers.zomato.com/api/v2.1/"
zomato_ny_city_id = "280"

response_code = -1

def get_zomato_response(full_url_request, key):
    headers = {"User-agent": "curl/7.43.0", "Accept": "application/json",
               user_key_header: key}
    request = requests.post(full_url_request, headers=headers)
    response_code = request.status_code
    return request.json()


def populate_cuisines():
    full_url_request = zomato_base_url + "cuisines?city_id=" + zomato_ny_city_id
    json_response = get_zomato_response(full_url_request, zomato_api_keys[2])
    cuisines_list = json_response['cuisines']

    populator = DatabasePopulator()
    for cuisine in cuisines_list:
        curr_cuisine = cuisine['cuisine']
        populator.insert_row('Cuisines',
                             [curr_cuisine['cuisine_id'],
                              curr_cuisine['cuisine_name']]
                             )


def populate_establishments():
    full_url_request = zomato_base_url + "establishments?city_id=" + \
                       zomato_ny_city_id
    json_response = get_zomato_response(full_url_request, zomato_api_keys[2])
    establishment_list = json_response['establishments']

    populator = DatabasePopulator()
    for establishment in establishment_list:
        curr_establishment = establishment['establishment']
        populator.insert_row('Establishments',
                             [curr_establishment['id'],
                              curr_establishment['name']]
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
    json_response = get_zomato_response(cuisines_url, zomato_api_keys[3])
    cuisines_list = json_response['cuisines']
    for cuisine in cuisines_list:
        cuisine_ids += [cuisine['cuisine']['cuisine_id']]

    establishment_ids = []
    establishment_url = zomato_base_url + "establishments?city_id=" + \
                        zomato_ny_city_id
    json_response = get_zomato_response(establishment_url, zomato_api_keys[3])
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
                                        "&cuisines=%d&establishment_type=%d" + \
                                        "&category=%d") % (zomato_ny_city_id,
                                                           offset, cuisine_id,
                                                           establishment_id,
                                                           category_id)
                    json_response = get_zomato_response(full_url_request,
                                                        zomato_api_keys[
                                                            curr_key])

                    if response_code == 500:
                        curr_key += 1

                    query_count += 1
                    if query_count > (curr_key + 1) * 1000:
                        curr_key += 1
                    if curr_key == 4:
                        return (category_id, query_count, total_restaurants)

                    if len(json_response) == 0:
                        continue

                    restaurants = json_response['restaurants']
                    total_restaurants += len(restaurants)
                    for restaurant in restaurants:
                        populate_restaurant(restaurant)
                    if query_count % 100 == 0:
                        print("------ STATUS ------")
                        print("Current key = %d" % curr_key)
                        print("Total Queries = %d" % query_count)
                        print("Total Restaurants = %d" % total_restaurants)

    return (-1, query_count, total_restaurants)


def populate_restaurant(restaurant_json):
    restaurant = restaurant_json['restaurant']
    id = restaurant['id']
    name = restaurant['name'].replace("'", "")
    lat, lng = restaurant['location']['latitude'], \
               restaurant['location']['longitude']
    price_category = restaurant['price_range']
    cuisines = restaurant['cuisines']
    agg_reviews = restaurant['user_rating']['aggregate_rating']
    has_online_delivery = restaurant['has_online_delivery']
    featured_photo = restaurant['featured_image']
    establishment = restaurant['establishment_types']['establishment_type'][
        'id']

    populator = DatabasePopulator()
    populator.insert_row('Restaurants',
                         [id, name, lat, lng, price_category, agg_reviews,
                          has_online_delivery, featured_photo, establishment])

    # update the RestaurantsCuisines table
    cuisines_list = cuisines.split(', ')
    for cuisine in cuisines_list:
        cuisine_id = populator.get_cuisine_id_by_name(cuisine)
        populator.insert_row('RestaurantsCuisines', [id, cuisine_id])

    return

populate_restaurants(1)