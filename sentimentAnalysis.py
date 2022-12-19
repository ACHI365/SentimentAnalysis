import nltk
import pandas as pd
import csv
import timeit
from nltk.sentiment import SentimentIntensityAnalyzer

# read csv file
file = pd.read_csv("tempCSV.csv", encoding="utf-8")

# initialize analyzer
analyzer = SentimentIntensityAnalyzer()

# read message column
comments = file["MESSAGE"]
ID = file["ID"]
likes = file["LIKE_COUNT"]

# csv file fields
fieldnames = ["COMMENT_ID", "SENTIMENT"]


def analyze(text, like_count):
    sentiment = analyzer.polarity_scores(text)
    if round(sentiment['compound'], 3) > 0:
        return 0
    elif round(sentiment['compound'], 3) < 0:
        return 2
    else:
        if like_count > 4:
            if sentiment['pos'] > sentiment['neg']:
                return 0
            else:
                return 2
        return 1

def createFinalCSV():
    # rows to insert into csv file
    rows = []

    for i in range(len(comments)):
        sentence = comments[i]
        curr_id = ID[i]
        curr_like_count = likes[i]

        sentiment_score = analyze(sentence, curr_like_count)

        data = {'COMMENT_ID': curr_id,
                'SENTIMENT': sentiment_score}

        rows.append(data)
        print(data)

    with open('result.csv', 'w', encoding='UTF8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


if __name__ == '__main__':
    createFinalCSV()
    pass
