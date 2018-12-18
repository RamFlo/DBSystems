import json
import requests

zamato_api_keys = ["321da0bc263eda93da9f3d9497876d2e",
                   "d7afaabbb3109389a42d21af7bb3b3a5",
                   "367e4e949648279a9951d011ee3a1f9d"]
user_key_header = "user-key"
zamatao_base_url = "https://developers.zomato.com/api/v2.1/"
zamato_ny_city_id = "280"
headers = {"Accept": "application/json"}


def fetch_cuisines():
    full_url_request = zamatao_base_url + "cuisines?" + "city_id=" + zamato_ny_city_id
    headers[user_key_header] = zamato_api_keys[0]
    request = requests.post(full_url_request, headers=headers)
    json_response = request.json()
    print(json_response)


fetch_cuisines()
