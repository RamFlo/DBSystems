import MySQLdb as mdb

localhost_name = "localhost"
username = "username"
password = "password"
db_name = ""

class DatabasePopulator:

    def __init__(self, table_name):
        self.table_name = table_name
        self.con = mdb.connect(localhost_name, username, password, db_name)
        self.cur = self.con.cursor()

    def insert_row(self, values):
        sql_query = "INSERT INTO %s" \
                    "VALUES %s"
        input_values = ', '.join(map(lambda x: '%s', values))
        input_values = input_values % tuple(values)
        sql_query = sql_query % (self.table_name, input_values)
        self.cur.execute(sql_query)