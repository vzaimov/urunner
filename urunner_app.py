# ---- This is URunner App ---- #
# import the Flask class from the flask package
from flask import Flask
# create the application object
app = Flask(__name__)
# use the decorator pattern to
# link the view function to a url


@app.route("/")
# define the view using a function, which returns a string
def hello_uruner():
    return "Hello, Urunner!"


@app.route("/hello")
def hello_world():
    return "Hello, World!"


# dynamic route
@app.route("/test/<search_query>")
def search(search_query):
    return search_query


# start the development server using the run() method


if __name__ == "__main__":
    app.run()
