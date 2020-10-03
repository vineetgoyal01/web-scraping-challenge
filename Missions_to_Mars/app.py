from flask import Flask, render_template, redirect

# Import our pymongo library, which lets us connect our Flask app to our Mongo database.
from flask_pymongo import PyMongo

# Import Scrape.py
import scrape_data

# Create an instance of our Flask app.
app = Flask(__name__)
mongo = PyMongo(app, uri="mongodb://localhost:27017/mars_app")


@app.route("/")
def inde():
    mars_data = mongo.db.mars_data.find_one()
    return render_template("index.html", mars=mars_data)

@app.route("/scrape")
def scrape():
    mars_data = mongo.db.mars_data
    mars_df = scrape_data.scrape()
    mars_data.update({}, mars_df, upsert=True)
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)