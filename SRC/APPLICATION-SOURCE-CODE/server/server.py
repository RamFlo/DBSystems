from flask import Flask
from db import Database
from datetime import datetime, timedelta
from log import Logger
import sql_queries
import request

logger = Logger().logger 
app = Flask(__name__)
port_number = 40327

database = Database()

cuisine_discovery_cache = {}
cuisine_discovery_cache_persistence = timedelta(days=1)

geodist = 0.12  # used for restaurant geosearching - defines L1 radius

@app.before_request
def log_request():
    return  # TODO: add request logger


@app.route('/')
def index():
    return app.send_static_file('TheFoodCourt.html')


@app.route('/ingredient_prefix/<string:prefix>')
def get_ingredient_by_prefix(prefix):
    query_res = database.find_ingredients_by_prefix(prefix)
    if query_res == -1:
        return None
    logger.info("GET get_ingredient_by_prefix query")
    return query_res


@app.route('/get_cuisines')
def get_cuisines():
    query_res = database.get_cuisines()
    if query_res == -1:
        return None
    logger.info("GET get_cuisines query")
    return query_res


@app.route('/discover_new_cuisines/<int:cuisine_id>')
def discover_new_cuisines(cuisine_id):
    logger.info("GET discover_new_cuisines query")
    if cuisine_id in cuisine_discovery_cache:
        insert_time, data = cuisine_discovery_cache[cuisine_id]
        if datetime.now() < insert_time + cuisine_discovery_cache_persistence:
            return data

    query_res = database.discover_new_cuisines_from_cuisine(cuisine_id)
    if query_res == -1:
        return None
    cuisine_discovery_cache[cuisine_id] = (datetime.now(), query_res)
    return query_res


@app.route('/restaurants/<ingredient>/')
def query_restaurants(ingredient):
    loclat, loclng = request.args.get('loclat'), request.args.get('loclng')
    price_category = request.args.get('price_category')
    online_delivery = request.args.get('online_delivery')
    min_review = request.args.get('min_review')
    base_query = sql_queries.restaurants_by_cuisine % ingredient
    if loclat != None and loclng != None:
        lat_range = [float(loclat) - geodist, float(loclat) + geodist]
        lng_range = [float(loclng) - geodist, float(loclng) + geodist]
    else:
        lat_range = None
        lng_range = None
    filtered_query = database.restaurant_query_builder(base_query,
                                                       lat_range, lng_range,
                                                       price_category,
                                                       min_review, online_delivery)
    limited_query = database.order_by_and_limit_query(filtered_query,
                                                    "agg_review DESC", 20)
    query_res = database.run_sql_query(limited_query)
    if query_res == -1:
        return None
    return query_res


if __name__ == '__main__':
    app.run(port=port_number)