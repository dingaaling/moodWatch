from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

text = ["I can't believe she did that!", "Road rage is the worst", "LOL", "YAY!!!", "It was not good.", "That sux", "😁",  "love the music hehe"]
analyzer = SentimentIntensityAnalyzer()
for sentence in text:
    wordCount = len(sentence.split())
    vs = analyzer.polarity_scores(sentence)
    print("{:-<35} {} {} {}".format(sentence, str(vs), "wordcount: ", wordCount))
