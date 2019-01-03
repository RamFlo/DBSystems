from Flask import Flask
from db import Database
import json

app = Flask(__name__)

database = Database()

cuisine_discovery_cache = {}

@app.before_request
def log_request():
    return # TODO: add request logger


@app.route('/ingredient_prefix/<string:prefix>')
def get_ingredient_by_prefix():
    query_res = database.find_ingredients_by_prefix(prefix)
    if query_res == -1:
        return None
    return json.dumps(query_res)


@app.route('/get_cuisines')
def get_cuisines():
    query_res = database.get_cuisines()
    if query_res == -1:
        return None
    return json.dumps(query_res)


@app.route('/discover_new_cuisines/<int:cuisine_id')
def discover_new_cuisines():
    if cuisine_id in cuisine_discovery_cache:
        return cuisine_discovery_cache[cuisine_id]
    else:
        query_res = database.discover_new_cuisines_from_cuisine(cuisine_id)
        if query_res == -1:
            return None
        encoded_res = json.dumps(query_res)
        cuisine_discovery_cache[cuisine_id] = encoded_res
        return encoded_res