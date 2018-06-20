from flask import Flask, redirect, render_template, request, url_for
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

analyzer = SentimentIntensityAnalyzer()

app = Flask(__name__)
app.config["DEBUG"] = True

comments = []

@app.route("/", methods=["GET", "POST"])
def main():
    #if GET: render website with comments
    if request.method == "GET":
        return render_template("index.html", comments=comments)
    #if POST: extract new comments from textbox
    comment = request.form["contents"]
    vs = analyzer.polarity_scores(comment)
    print(vs)
    comments.append(comment)
    return redirect(url_for("main"))

if __name__ == "__main__":
    app.run()
