import spacy
import pandas as pd
from textblob import TextBlob
from News_Aggregator.Web_Scrapper.Database import mongodb_connection as mc
nlp = spacy.load('en_core_web_sm')


def get_sentiment_label(pol):
    if pol >= positive_threshold:
        return "Positive"
    elif pol <= -positive_threshold:
        return "Negative"
    else:
        return "Neutral"


db_name = "news_articles"
collection = "articles"
db_handler = mc.MongoDBConnection(db_name, collection)
articles = db_handler.collection.find({}, {"content": 1, "full_content": 1, "article_id": 1, "_id": 0}).limit(200)
for text in articles:
    article_id = text["article_id"]
    try:
        clean_text = text["full_content"].replace("\n", " ")
    except KeyError:
        clean_text = text["content"].replace("\n", " ")
    clean_text = clean_text.replace("/", " ")
    clean_text = "".join([c for c in clean_text if c != "'"])

    sentences = []
    token = nlp(clean_text)
    for sent in token.sents:
        sentences.append(sent.text.strip())

    textblob_sentiments = []
    for s in sentences:
        txt = TextBlob(s)
        a = txt.sentiment.polarity
        b = txt.sentiment.subjectivity
        textblob_sentiments.append([s, a, b])

    df_textblob = pd.DataFrame(textblob_sentiments, columns=['Sentences', 'Polarity', 'Subjectivity'])

    polarity = df_textblob['Polarity'].mean()

    # Define threshold values for polarity
    neutral_threshold = 0.2
    positive_threshold = 0.2

    # Apply the function to create a new column for sentiment labels
    sentiment = get_sentiment_label(polarity)

    if sentiment != 'Neutral':
        print("article id", article_id)
        print("polarity", polarity, end=" ")
        print("sentiment", sentiment)
