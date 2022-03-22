from flask import Flask

app = Flask(__name__)

@app.route("/clients")
def clients():
    return {"clients": ["Bob Jones", "Bobby123"]}


def exampleMethod():
    return {"blah blah "}

if __name__ == "__main__":
    app.run(debug=True)