from distutils.command.clean import clean
from turtle import update
from flask import Flask
import pymysql, os, sys, base64, requests, json
from dotenv import load_dotenv
import pprint
sys.path.append("..")

load_dotenv()

app = Flask(__name__)

def parseClientsJson(clients: list):
    cleanedClients = []
    for client in clients:
        cleanedClients.append({})
        cleanedClients[-1]["id"] = client.get("CONTACT_ID")
        cleanedClients[-1]["first_name"] = client.get("FIRST_NAME")
        cleanedClients[-1]["last_name"] = client.get("LAST_NAME")
        cleanedClients[-1]["email"] = client.get("EMAIL_ADDRESS")
        cleanedClients[-1]["date_of_birth"] = client.get("DATE_OF_BIRTH")
        cleanedClients[-1]["street_address"] = address = client.get("ADDRESS_MAIL_STREET")
        cleanedClients[-1]["city"] = client.get("ADDRESS_MAIL_CITY")  
        cleanedClients[-1]["state"] = client.get("ADDRESS_MAIL_STATE") 
        cleanedClients[-1]["postal_code"] = client.get("ADDRESS_MAIL_POSTCODE")

        customFields = client.get("CUSTOMFIELDS")
        for ele in customFields:
            if ele['CUSTOM_FIELD_ID'] == "Gender__c":
                cleanedClients[-1]["gender"] = ele["FIELD_VALUE"]
            elif ele['CUSTOM_FIELD_ID'] == "Primary_Language__c":
                cleanedClients[-1]["primary_language"] = ele["FIELD_VALUE"]
            elif ele['CUSTOM_FIELD_ID'] == "Marital_Status__c":
                cleanedClients[-1]["marital_status"] = ele["FIELD_VALUE"]

    return cleanedClients
        

        

def populateClientsDB():
    #connecting mySQL
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

    # encoding the APIkey in base64 for authorization
    encodedAPIKey = (base64.b64encode(str.encode(os.environ["INSIGHTLY_APIKEY"]))).decode()
    header = {"Authorization": "Basic " + encodedAPIKey}

    # collects all of the clients from insightly in clientList, a list of dictionaries
    # cleans and extracts the data into clientList
    skipCount = 0
    clientList = [] 
    while True:
        # get the next 500 of contacts
        params={"skip": skipCount, "top": 500}
        response = requests.get("https://api.na1.insightly.com/v3.1/Contacts", headers=header, params=params)
        clients = json.loads(response.text)

        cleanedClients = parseClientsJson(clients)
        clientList.extend(cleanedClients) 
        if len(clients) < 500:
            break
        skipCount += 500

    # insert the data into the database
    with conn.cursor() as cur:
        for client in clientList:     
            columns = client.keys()
            columnsString = ",".join(columns)
            placeholders = ', '.join(['%s'] * len(client.values()))
       
            # query in case client already exists in database
            colValues = tuple(client.values())
            update_query = ""
            for i, col in enumerate(columns):
                if col == "id":
                    continue
                update_query += col + "=\"" + str(colValues[i])+"\""
                if i < len(columns) - 1:
                    update_query += ", "
            update_query += ";"


            sqlQuery = "INSERT INTO Clients (" + columnsString + ") VALUES({}) ON DUPLICATE KEY UPDATE {}".format(placeholders, update_query)
            cur.execute(sqlQuery, colValues,)

    conn.commit()
    conn.close()
populateClientsDB()
