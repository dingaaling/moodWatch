import numpy as np
from flask import Flask, redirect, render_template, request, url_for, flash
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from textAlert import sendText

analyzer = SentimentIntensityAnalyzer()

app = Flask(__name__)

comments, moods = [], []
baselineMood, sessionMood = 0.2, 0.0

@app.route("/", methods=["GET", "POST"])
def main():

    sessionMood = np.mean(moods)

    # text alert trigger
    if sessionMood < -0.8:
        sendText()

    # mood ring hsl changing
    s, l = 100, 50
    if np.isnan(sessionMood):
        h = 300
    else:
        h = (((sessionMood+0.7)*100)/1.4)+250

    color = "hsl({}, {}%, {}%)".format(str(h), str(s), str(l))

    #if GET: render website with comments
    if request.method == "GET":
        return render_template("index.html", comments=comments, moods=moods, baselineMood=baselineMood, sessionMood=sessionMood, color=color)

    #if POST: add comment to list and calculate mood score
    comment = request.form["contents"]
    comments.append(comment)

    vs = analyzer.polarity_scores(comment)
    moods.append(vs["compound"])

    return redirect(url_for("main"))

if __name__ == "__main__":
    app.config["DEBUG"] = True
    app.run()
