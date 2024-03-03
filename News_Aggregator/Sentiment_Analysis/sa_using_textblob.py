import re
import nltk
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from wordcloud import WordCloud
from textblob import TextBlob
import spacy
nlp = spacy.load('en_core_web_sm')

pd.set_option("display.max_rows", None)
pd.set_option("display.max_columns", None)
pd.set_option("display.max_colwidth", None)

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
    textblob_sentiments.append([s, a, b])

df_textblob = pd.DataFrame(textblob_sentiments, columns=['Sentences', 'Polarity', 'Subjectivity'])
print(df_textblob.head())
print(df_textblob.info())
df_textblob.to_csv("sample_news_sentiment.csv")
sns.displot(df_textblob["Polarity"], height=5, aspect=1.8)
plt.xlabel("Sentence Polarity(Textblob)")
plt.show()
sns.displot(df_textblob["Subjectivity"], height=5, aspect=1.8)
plt.xlabel("Sentence Subjectivity(Textblob)")
plt.show()

word_tokens = nltk.tokenize.word_tokenize(clean_text)
special_chars_pattern = re.compile(r'[^a-zA-Z0-9\s]')
tokens = [special_chars_pattern.sub('', token) for token in word_tokens]
tokens = [token for token in tokens if token]
words = []
for word in tokens:
    words.append(word.lower())

words_new = []
stopwords = nltk.corpus.stopwords.words('english')
for word in words:
    if word not in stopwords:
        words_new.append(word)
print(len(words_new))

freq_dist = nltk.FreqDist(words_new)
plt.subplots(figsize=(16, 10))
freq_dist.plot(20)

# words cloud is used for plotting words

res = ' '.join([i for i in words_new if not i.isdigit()])
plt.subplots(figsize=(16, 10))
wordcloud = WordCloud(
                          background_color='black',
                          max_words=100,
                          width=1400,
                          height=1200
                         ).generate(res)
plt.imshow(wordcloud)
plt.title('NEWS ARTICLE (100 words)')
plt.axis('off')
plt.show()
