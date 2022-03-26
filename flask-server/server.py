from flask import Flask
from insightly.insightly import Insightly
import os

app = Flask(__name__)

@app.route("/clients")
def clients():
    return {"clientele": ["Bob Jones", "Bobby123"]}

@app.route("/exampleMethod")
def exampleMethod():
    i = Insightly(apikey=os.environ["INSIGHTLY_APIKEY"])
    first_500_contacts = i.read('contacts')
    return str(first_500_contacts)


if __name__ == "__main__":
    app.run(debug=True)