import pymysql, sys, requests, json
sys.path.append("..")

class DBConnection():
    def __init__(self, app):
        self._encodedAPIKey = app.config.get("APIKEY")
        try:
            self.conn = pymysql.connect(host=app.config["HOST"][0], 
                                user=app.config.get("USER")[0], 
                                passwd=app.config.get("PASSWORD")[0], 
                                db=app.config.get("DATABASE")[0], 
                                connect_timeout=5)
        except pymysql.MySQLError as e:
            print("ERROR: Unexpected error: Could not connect to MySQL instance.")
            print(e)
            sys.exit(1)
    
    def close(self):
        self.conn.close()

    def _parseClientsJson(self, clients: list):
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
            cleanedClients[-1]["date_created"] = client.get("DATE_CREATED_UTC")

            customFields = client.get("CUSTOMFIELDS")
            for ele in customFields:
                if ele['CUSTOM_FIELD_ID'] == "Gender__c":
                    cleanedClients[-1]["gender"] = ele["FIELD_VALUE"]
                elif ele['CUSTOM_FIELD_ID'] == "Primary_Language__c":
                    cleanedClients[-1]["primary_language"] = ele["FIELD_VALUE"]
                elif ele['CUSTOM_FIELD_ID'] == "Marital_Status__c":
                    cleanedClients[-1]["marital_status"] = ele["FIELD_VALUE"]

        return cleanedClients

    def populateClientsDB(self):
        header = {"Authorization": "Basic " + self._encodedAPIKey}

        # collects all of the clients from insightly in clientList, a list of dictionaries
        # cleans and extracts the data into clientList
        skipCount = 0
        clientList = []

        while True:
            # get the next 500 of contacts
            params={"skip": skipCount, "top": 500}
            response = requests.get("https://api.na1.insightly.com/v3.1/Contacts", headers=header, params=params)

            clients = json.loads(response.text)

            cleanedClients = self._parseClientsJson(clients)
            clientList.extend(cleanedClients) 
            if len(clients) < 500:
                break
            skipCount += 500

        # insert the data into the database
        with self.conn.cursor() as cur:
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
                cur.execute(sqlQuery, colValues)

        self.conn.commit()

    def _parseCategoriesJSON(self, categories: list):
        res = []
        for category in categories:
            res.append({
                "id": category.get("CATEGORY_ID"),
                "name": category.get("CATEGORY_NAME")
            })
        return res

    def populateCategoriesDB(self):
        header = {"Authorization": "Basic " + self._encodedAPIKey}

        skipCount = 0
        categories = []

        while True:
            params={"skip": skipCount, "top": 500}
            response = requests.get("https://api.na1.insightly.com/v3.1/ProjectCategories", headers=header, params=params)

            data = json.loads(response.text)
            categories.extend(self._parseCategoriesJSON(data))

            if len(data) < 500:
                break
            skipCount += 500

        with self.conn.cursor() as cur:
            for category in categories:     
                cols = category.keys()
                colsString = ",".join(cols)
                placeholders = ', '.join(['%s'] * len(category.values()))
            
                # query in case client already exists in database
                colValues = tuple(category.values())
                update_query = ""
                for i, col in enumerate(cols):
                    if col == "id":
                        continue
                    update_query += col + "=\"" + str(colValues[i])+"\""
                    if i < len(cols) - 1:
                        update_query += ", "
                update_query += ";"


                sqlQuery = "INSERT INTO Categories (" + colsString + ") VALUES({}) ON DUPLICATE KEY UPDATE {}".format(placeholders, update_query)
                cur.execute(sqlQuery, colValues)

        self.conn.commit()

    def _parseEventsJSON(self, events: list):
        res = []
        for event in events:
            res.append({
                "id": event.get("PROJECT_ID"),
                "name": event.get("PROJECT_NAME"),
                "description": event.get("PROJECT_DETAILS"),
                "date_created": event.get("DATE_CREATED_UTC"),
                "category_id": event.get("CATEGORY_ID")
            })

        return res

    def populateEventsDB(self):
        header = {"Authorization": "Basic " + self._encodedAPIKey}

        skipCount = 0
        events = [] 

        while True:
            params={"skip": skipCount, "top": 500}
            response = requests.get("https://api.na1.insightly.com/v3.1/Projects", headers=header, params=params)

            data = json.loads(response.text)
            events.extend(self._parseEventsJSON(data))

            if len(data) < 500:
                break
            skipCount += 500
        
        with self.conn.cursor() as cur:
            for event in events:
                cols = event.keys()
                colsString = ",".join(cols)
                placeholders = ', '.join(['%s'] * len(event.values()))
        
                colValues = tuple(event.values())
                update_query = ""
                for i, col in enumerate(cols):
                    if col == "id":
                        continue
                    update_query += col + "=\"" + str(colValues[i])+"\""
                    if i < len(cols) - 1:
                        update_query += ", "
                update_query += ";"

                # Filter out Events with unknown category id
                if not cur.execute("SELECT * FROM Categories WHERE id = " + str(event.get("category_id"))):
                    continue
                sqlQuery = "INSERT INTO Events (" + colsString + ") VALUES({}) ON DUPLICATE KEY UPDATE {}".format(placeholders, update_query)
                cur.execute(sqlQuery, colValues)

        self.conn.commit()

    def _parseClientAttendanceJSON(self, events: list):
        res = []
        for event in events:
            links = event.get("LINKS")
            event_id = event.get("PROJECT_ID")
            for link in links:
                if link.get("LINK_OBJECT_NAME") == "Contact":
                    client_id = link.get("LINK_OBJECT_ID")
                    res.append({
                        "event_id": event_id,
                        "client_id": client_id
                    })
        return res

    def populateClientAttendanceDB(self):
        header = {"Authorization": "Basic " + self._encodedAPIKey}

        skipCount = 0
        attendance = [] 

        while True:
            params={"skip": skipCount, "top": 500}
            response = requests.get("https://api.na1.insightly.com/v3.1/Projects", headers=header, params=params)
            
            data = json.loads(response.text)
            attendance.extend(self._parseClientAttendanceJSON(data))

            if len(data) < 500:
                break
            skipCount += 500
        
        with self.conn.cursor() as cur:
            for event_client in attendance:
                cols = event_client.keys()
                colsString = ",".join(cols)
                placeholders = ', '.join(['%s'] * len(event_client.values()))
        
                colValues = tuple(event_client.values())
                update_query = ""
                for i, col in enumerate(cols):
                    if col == "id":
                        continue
                    update_query += col + "=\"" + str(colValues[i])+"\""
                    if i < len(cols) - 1:
                        update_query += ", "
                update_query += ";"

                # Filter out Client_Attendance where the event is not stored in our database
                if not cur.execute("SELECT * FROM Events WHERE id = " + str(event_client.get("event_id"))):
                    continue

                sqlQuery = "INSERT INTO Client_Attendance (" + colsString + ") VALUES({}) ON DUPLICATE KEY UPDATE {}".format(placeholders, update_query)
                cur.execute(sqlQuery, colValues)

        self.conn.commit()

    def testMethod(self):
        header = {"Authorization": "Basic " + self._encodedAPIKey}
        params={"skip": 0, "top": 1}
        response = requests.get("https://api.na1.insightly.com/v3.1/Projects", headers=header, params=params)
        data = json.loads(response.text)
        output = self._parseClientAttendanceJSON(data)
        print(len(output))

        with self.conn.cursor() as cur:
            sqlQuery = "SHOW COLUMNS FROM Clients;"
            cur.execute(sqlQuery)
            cols = cur.fetchall()
            print(len(cols))


    def populateAllDB(self):
        # TODO: Slow. Gotta make it faster later.
        self.populateClientsDB()
        self.populateCategoriesDB()
        self.populateEventsDB()
        self.populateClientAttendanceDB()