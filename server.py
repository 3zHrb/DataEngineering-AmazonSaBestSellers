from flask import Flask, render_template, request, url_for
from flask_cors import CORS
import amazon_sa_bestSellers_scrapper
import pandas as pd

app = Flask(__name__, template_folder="templates", static_folder="statics")
CORS(app)


@app.route("/", methods=["GET"])
def home():
    return render_template("home.html")


@app.route("/BestSellers", methods=["GET"])
def getBestSellers():
    df = pd.DataFrame(amazon_sa_bestSellers_scrapper.amazonScrapper())
    df["Number_Of_Reviews"] = df["Number_Of_Reviews"].astype("Int64")
    df_html = df.to_html()
    return render_template("home.html", df_html=df_html)


if __name__ == "__main__":
    print("Server is running ...")
    app.run(debug=True)
