import numpy as np
from flask import Flask, redirect, render_template, request, url_for
from flask_sqlalchemy import SQLAlchemy
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

analyzer = SentimentIntensityAnalyzer()

app = Flask(__name__)
app.config["DEBUG"] = True

SQLALCHEMY_DATABASE_URI = "sqlite:///comments.db"
app.config["SQLALCHEMY_DATABASE_URI"] = SQLALCHEMY_DATABASE_URI
app.config["SQLALCHEMY_POOL_RECYCLE"] = 299
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

comments, sentiment= [], []

@app.route("/", methods=["GET", "POST"])
def main():

    #if GET: render website with comments
    if request.method == "GET":
        return render_template("index.html", comments=comments, mood=sentiment)

    #if POST: add comment to list and calculate mood score
    comment = request.form["contents"]
    comments.append(comment)

    vs = analyzer.polarity_scores(comment)
    sentiment.append(vs["compound"])
    print(np.mean(sentiment))

    return redirect(url_for("main"))

if __name__ == "__main__":
    app.run()
