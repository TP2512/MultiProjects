import pandas as pd
from pattern.text.en import sentiment
import spacy
nlp = spacy.load('en_core_web_sm')


# Define a function to categorize polarity into sentiment labels
def get_sentiment_label(polarity):
    if polarity >= positive_threshold:
        return "Positive"
    elif polarity <= -positive_threshold:
        return "Negative"
    else:
        return "Neutral"


# Read news articles from file
with open("sample_article.txt", 'r') as f:
    text = f.read()

# Clean the text
clean_text = text.replace("\n", " ")
clean_text = clean_text.replace("/", " ")
clean_text = "".join([c for c in clean_text if c != "'"])

# Tokenize the text into sentences
sentences = [sent.text.strip() for sent in nlp(clean_text).sents]

# Perform sentiment analysis on each sentence
pattern_sentiments = []
for s in sentences:
    txt = sentiment(s)
    polarity = txt[0]
    subjectivity = txt[1]
    pattern_sentiments.append([s, polarity, subjectivity])

# Create a DataFrame with sentiment analysis results
df_textblob = pd.DataFrame(pattern_sentiments, columns=['Sentences', 'Polarity', 'Subjectivity'])

# Calculate average polarity news article
polarity = df_textblob['Polarity'].mean()
print(polarity)

# Define threshold values for polarity
neutral_threshold = 0.2
positive_threshold = 0.2

# Apply the function to create a new column for sentiment labels
sentiment = get_sentiment_label(polarity)

# Display the DataFrame with the new sentiment column
print(sentiment)
