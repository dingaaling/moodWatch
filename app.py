import numpy as np
from flask import Flask, redirect, render_template, request, url_for
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

analyzer = SentimentIntensityAnalyzer()

app = Flask(__name__)
app.config["DEBUG"] = True

comments, moods = [], []
baselineMood, sessionMood = 0.2, 0.0

@app.route("/", methods=["GET", "POST"])
def main():

    sessionMood = np.mean(moods)

    #if GET: render website with comments
    if request.method == "GET":
        return render_template("index.html", comments=comments, moods=moods, baselineMood=baselineMood, sessionMood=sessionMood)

    #if POST: add comment to list and calculate mood score
    comment = request.form["contents"]
    comments.append(comment)

    vs = analyzer.polarity_scores(comment)
    moods.append(vs["compound"])

    print("session mood is: ", sessionMood)
    return redirect(url_for("main"))

if __name__ == "__main__":
    app.run()
