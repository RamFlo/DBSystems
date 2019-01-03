import MySQLdb as mdb
import sql_queries

localhost_name = "mysqlsrv1.cs.tau.ac.il"
username = "DbMysql04"
password = "DbMysql04"
db_name = "DbMysql04"


class Database:
    def __init__(self):
        self.con = mdb.connect(localhost_name, username, password, db_name)
        self.con.set_character_set('utf8')
        self.cur = self.con.cursor()

    def find_ingredients_by_prefix(self, prefix):
        """
        Searches the database for all ingredients that begin with a given
        prefix. The result is limited to 20 values, and the values are
        ordered by their frequency in the database.
        """
        prefix = "%s%%" % prefix
        try:
            self.cur.execute(sql_queries.find_ingredient_by_prefix, prefix)
            return self.cur.fetchall()
        except Exception as ex:
            # TODO: log exception here
            return -1

    def discover_new_cuisines_from_cuisine(self, cuisine_id):
        """
        Returns the top three cuisines matching the given cuisine in the
        amount of shared ingredients, weighted by the number of recipes.
        """
        try :
            self.cur.execute(sql_queries.discover_new_cuisines_from_cuisine,
                             cuisine_id)
            return self.cur.fetchall()
        except Exception as ex:
            # TODO: log exception here
            return -1

    def get_cuisines(self):
        try:
            self.cur.execute(sql_queries.get_cuisine_list)
            return self.cur.fetchall()
        except Exception as ex:
            # TODO
            return -1