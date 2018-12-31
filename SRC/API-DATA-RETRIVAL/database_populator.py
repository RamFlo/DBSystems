import MySQLdb as mdb

localhost_name = "mysqlsrv1.cs.tau.ac.il"
username = "DbMysql04"
password = "DbMysql04"
db_name = "DbMysql04"
ssh_host = 'nova.cs.tau.ac.il'
ssh_port = 22

class DatabasePopulator:

    def __init__(self):
        con = mdb.connect(localhost_name, username, password, db_name)
        self.cur = con.cursor()

    def insert_row(self, table_name, values):
        """
        Inserts a row to the table, for all columns (a full row)
        :param table_name: the name of the table to insert the row into
        :param values: a list of the values inserted. len(values) should be
                        equal to the num of columns in the table
        """
        sql_query = "INSERT INTO %s" \
                    "VALUES %s"
        input_values = ', '.join(map(lambda x: '%s', values))
        input_values = input_values % tuple(values)
        sql_query = sql_query % (table_name, input_values)
        self.cur.execute(sql_query)

    def get_cuisine_id_by_name(self, cuisine_name):
        sql_query = "SELECT cuisine_id" \
                    "FROM Cuisines" \
                    "WHERE cuisine_name=%s" % cuisine_name
        self.cur.execute(sql_query)
        return self.cur.fetchone()[0]

    def get_recipe_id_by_yummly_id(self, yummly_id):
        sql_query = "SELECT recipe_id" \
                    "FROM Recipes" \
                    "WHERE yummly_recipe_id = %s" % yummly_id
        self.cur.execute(sql_query)
        return self.cur.fetchone()[0]