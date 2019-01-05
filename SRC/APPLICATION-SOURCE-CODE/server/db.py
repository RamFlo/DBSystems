import MySQLdb as mdb
import sql_queries
import simplejson
from log import Logger

localhost_name = "mysqlsrv1.cs.tau.ac.il"
username = "DbMysql04"
password = "DbMysql04"
db_name = "DbMysql04"


class Database:
    def __init__(self):
        self.con = mdb.connect(localhost_name, username, password, db_name)
        self.con.set_character_set('utf8')
        self.cur = self.con.cursor()
        self.logger = Logger("error").logger

    def run_sql_query(self, query):
        try:
            self.cur.execute(query)
            return self.get_query_result_as_json()
        except Exception as ex:
            self.logger.error("Failed at run_sql_query: %s" % ex)
            return -1

    def find_ingredients_by_prefix(self, prefix):
        """
        Searches the database for all ingredients that begin with a given
        prefix. The result is limited to 20 values, and the values are
        ordered by their frequency in the database.
        """
        prefix = "%s%%" % prefix
        try:
            self.cur.execute(sql_queries.find_ingredient_by_prefix, [prefix])
            return self.get_query_result_as_json()
        except Exception as ex:
            self.logger.error("Failed at find_ingredients_by_prefix: %s"
                              % ex)
            return -1

    def discover_new_cuisines_from_cuisine(self, cuisine_id):
        """
        Returns the top three cuisines matching the given cuisine in the
        amount of shared ingredients, weighted by the number of recipes.
        """
        try :
            self.cur.execute(sql_queries.discover_new_cuisines_from_cuisine,
                             [cuisine_id])
            return self.get_query_result_as_json()
        except Exception as ex:
            self.logger.error("Failed at discover_new_cuisines_from_cuisine: %s" % ex)
            return -1

    def get_cuisines(self):
        try:
            self.cur.execute(sql_queries.get_cuisine_list)
            return self.get_query_result_as_json()
        except Exception as ex:
            self.logger.error("Failed at get_cuisines: " % ex)
            return -1

    @staticmethod
    def restaurant_query_builder(base_query, lat_range=None, lng_range=None,
                                 price_category=None, min_agg_review=None,
                                 online_delivery=None, establishment_id=None):
        """
        Returns a query based on a given query, with extension given
        specific parameters, such as extra condition on the query.
        :param base_query: a query that returns at least, the following
        columns from the Restaurant database:
        restaurant_name, lat, lng, price_category, agg_review,
        online_delivery, featured_photo_url, establishment_id
        :param lat_range: (lat_min, lat_max)
        :param lng_range: (lng_min, lng_max)
        :param price_category:  1 <= int <= 4
        :param min_agg_review: 0 <= float <= 5
        :param online_delivery: 0 or 1
        :param establishment_id: valid establishment_id
        :return:
        """
        wrapped_query = sql_queries.restaurant_query_wrapper % base_query

        query_prefix = " WHERE"
        if lat_range is not None:
            wrapped_query += "%s %f <= source.lat AND source.lat <= %f" \
                             % (query_prefix, lat_range[0], lat_range[1])
            query_prefix = " AND"
        if lng_range is not None:
            wrapped_query += "%s %f <= source.lng AND source.lng <= %f" \
                             % (query_prefix, lng_range[0], lng_range[1])
            query_prefix = " AND"
        if price_category is not None:
            wrapped_query += "%s source.price_category = %d" % (
                query_prefix, price_category)
            query_prefix = " AND"
        if min_agg_review is not None:
            wrapped_query += "%s source.agg_review >= %f" % (query_prefix, min_agg_review)
            query_prefix = " AND"
        if online_delivery is not None:
            wrapped_query += "%s source.has_online_delivery = %d" % (
                query_prefix, online_delivery)
            query_prefix = " AND"
        if establishment_id is not None:
            wrapped_query += "%s source.establishment_id = %d" % (
                query_prefix, establishment_id)

        return wrapped_query

    def get_query_result_as_json(self):
        """
        :return: the last query results as a list of dictionaries,
        each dictionary has the column name as keys and row values as values
        """
        column_headers = [x[0] for x in self.cur.description]
        results = self.cur.fetchall()
        json_data = []
        for result in results:
            json_data += [dict(zip(column_headers, result))]
        return simplejson.dumps(json_data)