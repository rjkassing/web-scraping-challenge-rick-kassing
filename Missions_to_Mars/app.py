from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scraping_mars

app = Flask(__name__)

# Use flask_pymongo to set up mongo connection
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"
mongo = PyMongo(app)

# Or set inline
# mongo = PyMongo(app, uri="mongodb://localhost:27017/mars_app")


@app.route("/")
def index():
    mars_data = mongo.db.mars_data.find_one()
    return render_template("index.html", mars_html=mars_data)


@app.route("/scrape")
def scrape():
    mars_data = mongo.db.mars_data
    listings_data = scraping_mars.scrape()
    mars_data.update({}, listings_data, upsert=True)
    return redirect("/", code=302)


if __name__ == "__main__":
    app.run(debug=True)
