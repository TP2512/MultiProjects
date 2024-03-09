import spacy
import pandas as pd
from textblob import TextBlob
nlp = spacy.load('en_core_web_sm')


class NewsAnalysis:
    neutral_threshold = 0.2
    positive_threshold = 0.2

    def __init__(self, news):
        self.text = news

    def get_sentiment_label(self, pol):
        if pol >= self.positive_threshold:
            return "Positive"
        elif pol <= -self.positive_threshold:
            return "Negative"
        else:
            return "Neutral"

    def sentiment_getter(self):

        clean_text = self.text.replace("\n", " ")
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
        print(polarity)
        # Apply the function to create a new column for sentiment labels
        sentiment = self.get_sentiment_label(polarity)

        return sentiment
