from flask import Flask
from db import Database
import json
from datetime import datetime, timedelta
from log import Logger
logger = Logger().logger 
app = Flask(__name__)
port_number = 40327

database = Database()

cuisine_discovery_cache = {}
cuisine_discovery_cache_persistence = timedelta(days=1)


@app.before_request
def log_request():
    return  # TODO: add request logger


@app.route('/ingredient_prefix/<string:prefix>')
def get_ingredient_by_prefix(prefix):
    query_res = database.find_ingredients_by_prefix(prefix)
    if query_res == -1:
        return None
    logger.info("GET get_ingredient_by_prefix query")
    return json.dumps(query_res)


@app.route('/get_cuisines')
def get_cuisines():
    query_res = database.get_cuisines()
    if query_res == -1:
        return None
    logger.info("GET get_cuisines query")
    return json.dumps(query_res)


@app.route('/discover_new_cuisines/<int:cuisine_id>')
def discover_new_cuisines(cuisine_id):
    if cuisine_id in cuisine_discovery_cache:
        insert_time, data = cuisine_discovery_cache[cuisine_id]
        if datetime.now() < insert_time + cuisine_discovery_cache_persistence:
            return data

    query_res = database.discover_new_cuisines_from_cuisine(cuisine_id)
    if query_res == -1:
        return None
    logger.info("GET discover_new_cuisines query")
    encoded_res = json.dumps(query_res)
    cuisine_discovery_cache[cuisine_id] = (datetime.now(), encoded_res)
    return encoded_res


if __name__ == '__main__':
    app.run(port=port_number)