import re
import nltk
import pandas as pd
from pattern.text.en import sentiment
import spacy
nlp = spacy.load('en_core_web_sm')

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

# Calculate average polarity and subjectivity for each news article
df_textblob = df_textblob[['Polarity', 'Subjectivity']].mean()
print(df_textblob)
# Merge sentiment analysis results with original DataFrame containing news articles
# Assuming you have a DataFrame named 'news_df' containing news articles
# news_df = pd.DataFrame({'News': sentences})  # Sample DataFrame, replace with your actual DataFrame
# news_with_sentiment = pd.concat([news_df, avg_sentiment[['Polarity', 'Subjectivity']]], axis=1)
#
# # Save the DataFrame to CSV
# news_with_sentiment.to_csv("sample_news_with_sentiment.csv", index=False)

# import pandas as pd

# Load the DataFrame containing sentiment analysis results
# df_textblob = pd.read_csv("sample_news_sentiment.csv")

# Define threshold values for polarity
neutral_threshold = 0.2
positive_threshold = 0.2

# Define a function to categorize polarity into sentiment labels
def get_sentiment_label(polarity):
    if polarity >= positive_threshold:
        return "Positive"
    elif polarity <= -positive_threshold:
        return "Negative"
    else:
        return "Neutral"

# Apply the function to create a new column for sentiment labels
df_textblob["Sentiment"] = df_textblob["Polarity"].apply(get_sentiment_label)

# Display the DataFrame with the new sentiment column
print(df_textblob.head())

