import numpy as np
from flask import Flask, redirect, render_template, request, url_for, flash
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from textAlert import sendText
import pandas as pd
import string

analyzer = SentimentIntensityAnalyzer()
translator = str.maketrans('', '', string.punctuation)

df = pd.read_csv("dictionary.csv", header=None)
dictionary = df.values.T.tolist()[0]

app = Flask(__name__)

comments, thirstScore = [], []
baselineMood, sessionMood = 0.2, 0.0

@app.route("/", methods=["GET", "POST"])
def main():

    sessionMood = np.mean(thirstScore)

    # text alert trigger
    if sessionMood < -0.6:
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
        return render_template("index.html", comments=comments, moods=thirstScore, baselineMood=baselineMood, sessionMood=sessionMood, color=color)

    #if POST: add comment to list and calculate mood score
    comment_raw = request.form["contents"]
    comment = comment_raw.translate(translator)
    comments.append(comment_raw)

    commentVec = comment.split()
    dirtyWords = list(set(dictionary) & set(commentVec))

    vs = analyzer.polarity_scores(comment)
    mood = vs["compound"]

    dirtyCount = 0

    if len(dirtyWords) == 1:
        dirtyCount = 1
    elif len(dirtyWords) >= 10:
        dirtyCount = 4
    elif len(dirtyWords) >= 5:
        dirtyCount = 3
    elif len(dirtyWords) >= 2:
        dirtyCount = 2

    thirst = abs(mood + dirtyCount)
    print("Thirst score: ", mood, "+", len(dirtyWords), dirtyCount)

    thirstScore.append(thirst)

    return redirect(url_for("main"))

if __name__ == "__main__":
    app.config["DEBUG"] = True
    app.run()
