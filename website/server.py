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
    df = pd.DataFrame(amazon_sa_bestSellers_scrapper.amazonScrapper())
    df["Number_Of_Reviews"] = df["Number_Of_Reviews"].astype("Int64")
    currentDirectory = os.getcwd()

    session["user_session_id"] = str(uuid.uuid4())

    lastDirectory = os.path.split(currentDirectory)[-1]
    if lastDirectory == "AmazonSaBestSellers":
        session["filesDirectory"] = f"{os.getcwd()}/website/csv_Files"
    else:
        session["filesDirectory"] = f"{os.getcwd()}/csv_Files"

    df.to_csv(f'{session.get("filesDirectory")}/{session.get("user_session_id")}.csv')
    df_html = df.to_html()

    return render_template("home.html", df_html=df_html)


@app.route("/LoadData", methods=["POST"])
def LoadData():
    currentDirectory = os.getcwd()

    df = pd.read_csv(
        f'{session.get("filesDirectory")}/{session.get("user_session_id")}.csv'
    )

    s3 = boto3.resource(
        service_name="s3",
        region_name="us-west-2",
        aws_access_key_id=os.environ.get("aws_access_key_id"),
        aws_secret_access_key=os.environ.get("aws_secret_access_key"),
    )

    s3UploadingMessage = (
        "File was successfully loaded to s3 bucket: amazon-best-sellers-bucket ✅"
    )
    try:
        s3.Bucket("amazon-best-sellers-bucket").upload_file(
            Filename=f'{session.get("filesDirectory")}/{session.get("user_session_id")}.csv',
            Key=f'uploadedBybutton-{session.get("user_session_id")}.csv',
        )
    except:
        s3UploadingMessage = "File was not successfully loaded to s3 bucket: amazon-best-sellers-bucket ❌"

    os.remove(f'{session.get("filesDirectory")}/{session.get("user_session_id")}.csv')

    return render_template("home.html", s3UploadingMessage=s3UploadingMessage)


if __name__ == "__main__":
    print("Server is running ...")
    app.run(debug=True)
