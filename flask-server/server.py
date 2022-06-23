from calendar import month
from config import Config
from flask import Flask
import atexit
from utils.DB import DBConnection
from scheduler.jobs import initScheduler
from dotenv import load_dotenv
from datetime import date, datetime, timedelta

load_dotenv()

app = Flask(__name__)
app.config.from_object(Config)
db = DBConnection(app)
appScheduler = initScheduler(app)

def onExit():
    # Close the connection upon exitting the application
    appScheduler.shutdown()
    db.close()

# an example of an endpoint, prints all the clients in the db
@app.route("/exampleMethod")
def exampleMethod():
    with db.conn.cursor() as cur:
        # stores all the column names in columns
        columns = []
        sqlQuery = "SHOW COLUMNS FROM Clients;"  # example
        cur.execute(sqlQuery)
        cols = cur.fetchall()
        for col in cols:
            columns.append(col[0])

        # stores all the clients in the database in result
        sqlQuery = "SELECT * FROM Clients;"  # example
        cur.execute(sqlQuery)
        result = cur.fetchall()

        # creates a list of dictionaries of clients from the DB
        clients = []
        for res in result:  # res is one big array of all the columns
            clients.append({})
            for i in range(len(columns)):  # the col names themselves
                clients[-1][columns[i]] = res[i]
    
    return str(clients)

  
# TODO: Update this function to return the opposite of what getInactiveUsers() returns.
# Returns most active users
@app.route("/get-active-clients")
def getMostActiveUsers():

    # Initialize specification variables
    responseSize = 20
    endDate = datetime.today()
    # Get the date 31 days ago.
    startDate = endDate - timedelta(days=31)

    response = []

    with db.conn.cursor() as cur:
        columns = []
        sqlQuery = "SHOW COLUMNS FROM Clients;"
        cur.execute(sqlQuery)
        cols = cur.fetchall()
        for col in cols:
            columns.append(col[0])
        columns.append("frequency")

        sqlQuery = """
                SELECT clients.*, freq.frequency FROM Clients clients
                INNER JOIN (
                    SELECT client_id, count(client_id) frequency FROM Client_Attendance
                    WHERE event_id in (
                        SELECT id FROM Events
                        WHERE date_created BETWEEN '{start}' AND '{end}'
                    )
                    GROUP BY client_id
                    ORDER BY frequency DESC
                    LIMIT {limit}
                ) freq ON clients.id = freq.client_id;
            """.format(start=startDate, end=endDate, limit=responseSize)
        
        cur.execute(sqlQuery)
        clientsWithFreq = cur.fetchall()

        for client in clientsWithFreq:
            response.append({})
            for i in range(len(columns)):
                response[-1][columns[i]] = client[i]

    return str(response)


def calculate_age(birthdate):
    today = date.today()
    age = today.year - birthdate.year - ((today.month, today.day) < (birthdate.month, birthdate.day))
    return age
    
    
@app.route("/ageGroups")
def getAgeGroups():
    with db.conn.cursor() as cur: #creating a connection to the database
        sqlQuery = "SELECT date_of_birth FROM sunday_friends.Clients"
        cur.execute(sqlQuery)
        date_of_births = cur.fetchall()

    exact_age = list()
    age_map = {"0-10": 0, "11-20":0, "21-30":0, "31-40":0 , "41-50":0, "51-60":0, "61-70":0}

    
    for x in date_of_births: 
        if(x[0]==None or x[0] == "None"):
            continue
        dateObject = datetime.fromisoformat(x[0])
        age = calculate_age(dateObject)
        if age < 0:
            continue

        if age == 0:
            age = 1

        if 0<=age<=10:
            age_map["0-10"] = age_map["0-10"] + 1
        if 11<=age<=20:
            age_map["11-20"] = age_map["11-20"] + 1
        if 21<=age<=30:
            age_map["21-30"] = age_map["21-30"] + 1
        if 31<=age<=40:
            age_map["31-40"] = age_map["31-40"] + 1
        if 41<=age<=50:
            age_map["41-50"] = age_map["41-50"] + 1
        if 51<=age<=60:
            age_map["51-60"] = age_map["51-60"] + 1
        if 61<=age<=70:
            age_map["61-70"] = age_map["61-70"] + 1
            
    return age_map

# isInactiveClient returns true if a client is active, otherwise false.
def isInactiveClient(client):
    # client structure: (id, first_name, last_name, days_registered, events_attended, days_inactive)

    # default threshold (in days), used on a contition that user has not attended any events
    threshold = 169

    if client[4] == 0:
        return client[3] >= threshold
    
    # threshold for inactivity is calculated by:
    # v: max(30, days_registered) --> 30 if first month, else use days_registered
    # min(v, 365) --> if registered for over a year, only consider past year, else consider user's days_registered
    # divide by events_attended to calculate average time between each event attended
    # multiply by two to increase threshold
    threshold = (2 * min(max(30, client[3]), 365)) / client[4]

    # NOTE: every client has a different threshold, calculated based on their previous event attendance

    return threshold < client[5]
        


@app.route("/get-inactive-clients")
def getInactiveUsers():

    response = []
    inactiveClients = []

    # Only consider the events from 'startDate' to 'endDate' 
    endDate = datetime.today()
    startDate = endDate - timedelta(days=365)

    # 1: 64.9 ms
    # 2: 
    with db.conn.cursor() as cur:
        sqlQuery = """
            SELECT c.id, first_name, last_name, DATEDIFF('{end}', date_created) days_registered, 
            COUNT(e.id) events_attended, DATEDIFF('{end}', last_attendance) days_inactive FROM Clients c
            LEFT JOIN (
                SELECT * FROM Client_Attendance
            ) ca ON id = ca.client_id
            LEFT JOIN (
                SELECT id, MAX(date_created) last_attendance FROM Events
                WHERE date_created BETWEEN '{start}' AND '{end}'
                GROUP BY id
            ) e ON event_id = e.id
            WHERE date_created IS NOT NULL
            GROUP BY c.id;
        """.format(start=startDate, end=endDate)

        cur.execute(sqlQuery)
        inactiveClients = cur.fetchall()
    
    for i in range(len(inactiveClients)):
        if isInactiveClient(inactiveClients[i]):
            response.append({
                "id": inactiveClients[i][0],
                "first_name": inactiveClients[i][1],
                "last_name": inactiveClients[i][2]
            })
    
    return str(response)


if __name__ == "__main__":
    # Adding onExit event handler
    atexit.register(onExit)

    appScheduler.start()

    app.run(debug=app.config["DEBUG"])
