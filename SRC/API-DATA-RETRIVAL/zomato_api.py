import requests

from database_populator import DatabasePopulator

zomato_api_keys = ["321da0bc263eda93da9f3d9497876d2e",
                   "d7afaabbb3109389a42d21af7bb3b3a5",
                   "367e4e949648279a9951d011ee3a1f9d"]
user_key_header = "user-key"
zomato_base_url = "https://developers.zomato.com/api/v2.1/"
zomato_ny_city_id = "280"
headers = {"Accept": "application/json"}


def fetch_cuisines():
    full_url_request = zomato_base_url + "cuisines?" + "city_id=" + zomato_ny_city_id
    headers[user_key_header] = zomato_api_keys[0]
    request = requests.post(full_url_request, headers=headers)
    json_response = request.json()
    cuisines_list = json_response['cuisines']

    populator = DatabasePopulator(table_name='Cuisines')
    for cuisine in cuisines_list:
        curr_cuisine = cuisine['cuisine']
        populator.insert_row([curr_cuisine['cuisine_id'], curr_cuisine['cuisine_name']])


fetch_cuisines()
