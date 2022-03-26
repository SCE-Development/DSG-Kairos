from flask import Flask
from insightly.insightly import Insightly
import os

app = Flask(__name__)

@app.route("/clients")
def clients():
    return {"clients": ["Bob Jones", "Bobby123"]}


def exampleMethod():
    i = Insightly(apikey=os.environ("INSIGHTLY_API_KEY"))
    first_500_contacts = i.read('contacts')
    return first_500_contacts


if __name__ == "__main__":
    app.run(debug=True)