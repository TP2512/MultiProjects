import spacy
nlp = spacy.load('en_core_web_sm')
import pandas as pd
from textblob import TextBlob
from News_Aggregator.Database import mongodb_connection as mc

db_name = "news_articles"
collection = "articles"
db_handler = mc.MongoDBConnection(db_name, collection)
text = db_handler.collection.find_one({}, {"full_content": 1, "_id": 0})["full_content"]

clean_text = text.replace("\n", " ")
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

df_textblob = pd.DataFrame(textblob_sentiments,columns=['Sentences', 'Polarity', 'Subjectivity'])
print(df_textblob.head())
print(df_textblob.info())

