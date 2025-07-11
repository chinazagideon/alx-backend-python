from contextlib import contextmanager
import functools
from itertools import islice
from os import pread
import mysql.connector
import json

# Load the mysql config file
with open('python-decorators-0x01/config.json', 'r') as f:
    config = json.load(f)

# task: a context manager that accepts query input
class ExecuteQuery:
    def __init__(self, query=None):
        self.config = config #add database configuration to context object
        self.connector = mysql.connector
        self.query = query #assign query to query attr
        self.cursor = None
        self.conn = None
        self.results = None
    def __enter__(self):
        print(f"Context start Query -> {self.query}")
        try:
            self.conn = self.connector.connect(**self.config) #open connection
            self.cursor = self.conn.cursor() #initialise cursor
            self.executeQuery() #execute query
            return self #return context object
        except self.connector.Error as exc:
            print (f"mysql error: {type(exc).__name__}: {exc}")
        
    def executeQuery(self):
        try:
            cursor = self.cursor
            cursor.execute(self.query)
            self.results = cursor.fetchall()
            return self
        except self.connector.Error as exc:
            print(f"sql error #{type(exc).__name__}{exc}")
    def __exit__(self, exc_type, exc_val, exc_tb):
        print('operation complete')
        try:
            # clean up 
            if(self.cursor):
                self.cursor.close()
            if(self.conn):
                self.conn.close()
        except self.connector.InternalError as Error:
            print(f"Internal Exception {type(Error).__name__}{Error}")
            return False
# generate rows
def generate_rows(iteratable):
    for row in iteratable:
        yield row

# execute query using with
# TEST CASE ONE age > 25
with ExecuteQuery(query="SELECT * FROM users WHERE age > 25") as data: #assign context object to data
    exc_query = generate_rows(data.results) #assign results and generate each row using a generator
    for users in (islice(exc_query, 10)): #
        print (users)

# execute query using with
# TEST CASE TWO age < 25
with ExecuteQuery(query="SELECT * FROM users WHERE age < 25") as data: #assign context object to data
    exc_query = generate_rows(data.results) #assign results and generate each row using a generator
    for users in (islice(exc_query, 10)): #
        print (users)


# Response
# Context start Query -> SELECT * FROM user_data WHERE age > 25
# (1, 'Johnnie Mayer', 'Crawford_Cartwright@hotmail.com', Decimal('35'))
# (2, 'Myrtle Waters', 'Edmund_Funk@gmail.com', Decimal('99'))
# (3, 'Flora Rodriguez I', 'Willie.Bogisich@gmail.com', Decimal('84'))
# (4, 'Dr. Cecilia Konopelski-Lakin', 'Felicia75@gmail.com', Decimal('87'))
# (5, 'Chelsea Boyle-Stoltenberg', 'Regina.Emard97@yahoo.com', Decimal('83'))
# (8, 'Thomas Hane', 'Dominic24@yahoo.com', Decimal('93'))
# (9, 'Della Hickle', 'Leon_Rohan@hotmail.com', Decimal('35'))
# (10, 'Kristi Durgan', 'Maria_Schmeler9@hotmail.com', Decimal('70'))
# (11, 'Brad Sawayn', 'Tyler.Dach57@gmail.com', Decimal('112'))
# (12, 'Isabel Crist Jr.', 'Cecilia_Braun54@yahoo.com', Decimal('63'))
# operation complete
# Context start Query -> SELECT * FROM user_data WHERE age < 25
# (6, 'Seth Mraz', 'Cecilia_Blanda89@gmail.com', Decimal('24'))
# (7, 'Thelma Kris-Schinner', 'Johnnie.Jast93@hotmail.com', Decimal('6'))
# (15, 'Martin Flatley', 'Gabriel23@hotmail.com', Decimal('13'))
# (17, 'Blanca Durgan', 'Christina27@gmail.com', Decimal('1'))
# (27, 'Santos Skiles', 'Joey22@gmail.com', Decimal('17'))
# (31, 'Hubert Gerlach', 'Alice99@hotmail.com', Decimal('3'))
# (41, 'Inez Walker', 'Fannie_Wolff-Schinner@gmail.com', Decimal('19'))
# (43, 'Angela Emmerich', 'Martin12@yahoo.com', Decimal('1'))
# (44, 'Sidney Kertzmann', 'Angelo_Krajcik@yahoo.com', Decimal('10'))
# (46, 'Cedric McLaughlin', 'Al.Towne@yahoo.com', Decimal('21'))
# operation complete