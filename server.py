from flask import Flask, render_template, request
from flask_cors import CORS


app = Flask(__name__, template_folder="templates", static_folder="statics")
CORS(app)


@app.route("/", methods=["GET"])
def home():
    return render_template("home.html")


if __name__ == "__main__":
    print("Server is running ...")
    app.run(debug=True)
