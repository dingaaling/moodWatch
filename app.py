import numpy as np
from flask import Flask, redirect, render_template, request, url_for
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

analyzer = SentimentIntensityAnalyzer()

app = Flask(__name__)
app.config["DEBUG"] = True

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
