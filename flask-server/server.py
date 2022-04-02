import re
from flask import Flask
import pymysql, sys
import os
import requests, base64, pprint,json
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)


# an example of an endpoint, prints all the clients in the db
@app.route("/exampleMethod")
def exampleMethod():
    try:
        conn = pymysql.connect(host=os.environ.get("RDS_HOST_NAME"), 
                            user=os.environ.get("RDS_USER"), 
                            passwd=os.environ.get("RDS_PASSWORD"), 
                            db=os.environ.get("DATABASE"), 
                            connect_timeout=5)
    except pymysql.MySQLError as e:
        print("ERROR: Unexpected error: Could not connect to MySQL instance.")
        print(e)
        sys.exit(1)

    with conn.cursor() as cur:
        # stores all the column names in columns
        columns = []
        sqlQuery = "SHOW COLUMNS FROM Clients;" #example
        cur.execute(sqlQuery)
        cols = cur.fetchall()
        for col in cols:
            columns.append(col[0])

        # stores all the clients in the database in result
        sqlQuery = "SELECT * FROM Clients;" # example
        cur.execute(sqlQuery)
        result = cur.fetchall()

        # creates a list of dictionaries of clients from the DB
        clients = []
        for res in result:  # res is one big array of all the columns
            clients.append({})
            for i in range(len(columns)):   # the col names themselves
                clients[-1][columns[i]] = res[i]


    conn.close()
    return str(clients)

if __name__ == "__main__":
    app.run(debug=True)
