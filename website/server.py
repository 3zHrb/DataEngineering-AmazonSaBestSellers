from flask import Flask, render_template, request, url_for, jsonify, session
import amazon_sa_bestSellers_scrapper
import pandas as pd
import uuid
import os
import boto3
import secrets

app = Flask(__name__, template_folder="templates", static_folder="statics")
app.secret_key = secrets.token_hex(16)


@app.route("/", methods=["GET"])
def home():

    return render_template("home.html")


@app.route("/BestSellers", methods=["GET"])
def getBestSellers():
    print("getBestSellers is triggered ...")
    df = pd.DataFrame(amazon_sa_bestSellers_scrapper.amazonScrapper())
    print("we got the dataframe ...")
    df["Number_Of_Reviews"] = df["Number_Of_Reviews"].astype("Int64")
    currentDirectory = os.getcwd()

    session["user_session_id"] = str(uuid.uuid4())
    print("current working directory")
    print(currentDirectory)
    df.to_csv(f'{currentDirectory}/csv_Files/{session.get("user_session_id")}.csv')
    df_html = df.to_html()
    print("html table is loaded ...")
    return render_template("home.html", df_html=df_html)


@app.route("/LoadData", methods=["POST"])
def LoadData():
    currentDirectory = os.getcwd()
    df = pd.read_csv(
        f'{currentDirectory}/csv_Files/{session.get("user_session_id")}.csv'
    )

    s3 = boto3.resource(
        service_name="s3",
        region_name="us-west-2",
        aws_access_key_id=os.environ.get("aws_access_key_id"),
        aws_secret_access_key=os.environ.get("aws_secret_access_key"),
    )

    s3.Bucket("amazon-best-sellers-bucket").upload_file(
        Filename=f'{currentDirectory}/csv_Files/{session.get("user_session_id")}.csv',
        Key=f'uploadedBybutton-{session.get("user_session_id")}.csv',
    )

    os.remove(f'{currentDirectory}/csv_Files/{session.get("user_session_id")}.csv')

    return render_template("home.html", bucketName="amazon-best-sellers-bucket")


if __name__ == "__main__":
    print("Server is running ...")
    app.run(debug=True)
