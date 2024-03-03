import spacy
nlp = spacy.load('en_core_web_sm')
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from wordcloud import WordCloud
from textblob import TextBlob
from News_Aggregator.Database import mongodb_connection as mc

pd.set_option("display.max_rows", None)
pd.set_option("display.max_columns", None)
pd.set_option("display.max_colwidth", None)
# db_name = "news_articles"
# collection = "articles"
# db_handler = mc.MongoDBConnection(db_name, collection)
# test_art = db_handler.collection.find_one({}, {"full_content": 1, "_id": 0})["full_content"]
# print(test_art)

with open("sample_article.txt", 'r') as f:
    text = f.read()

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
    textblob_sentiments.append([s,a,b])

df_textblob = pd.DataFrame(textblob_sentiments,columns=['Sentences', 'Polarity', 'Subjectivity'])
print(df_textblob.head())
print(df_textblob.info())
df_textblob.to_csv("sample_news_sentiment.csv")
sns.displot(df_textblob["Polarity"], height= 5, aspect=1.8)
plt.xlabel("Sentense Polarity(Textblob)")
plt.show()
sns.displot(df_textblob["Subjectivity"], height=5, aspect=1.8)
plt.xlabel("Sentense Subjectivity(Textblob)")
plt.show()
