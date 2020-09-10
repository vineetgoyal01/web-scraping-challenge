from flask import Flask, render_template, redirect

# Import our pymongo library, which lets us connect our Flask app to our Mongo database.
from flask_pymongo import PyMongo

# Import Scrape.py
import scrape

# Create an instance of our Flask app.
app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"


# Use flask_pymongo to set up mongo connection

mongo = PyMongo(app)

@app.route("/")
def index():
    mars = mongo.db.collection.find_one()
    return render_template("index.html", mars=mars)

@app.route("/scrape")
def scrape():
    #mars = mongo.db.mars 
    mars_data = scrape_mars.scrape()
    mongo.db.collection.update({}, mars_data, upsert=True)
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)