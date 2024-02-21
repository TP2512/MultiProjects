import nltk
from nltk.corpus import stopwords
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.stem import PorterStemmer,WordNetLemmatizer

stemmer = PorterStemmer()

example_string = """give me the status of node restid 2?"""
words_in_quote= word_tokenize(example_string)
# print(sent_tokenize(example_string))
# print(word_tokenize(sent_tokenize(example_string)[0]))

stop_words = set(stopwords.words("english"))
filtered_list = [word for word in words_in_quote if word.casefold() not in stop_words ]
print(filtered_list)
stemmed_words = [stemmer.stem(word) for word in words_in_quote]
print("stemmed question",stemmed_words)

print(nltk.pos_tag(words_in_quote))

#tokensation -sentence,word
#stemming - helper,helping --> help
#tagging -tags POS --> tarkesh NN(Noun)
lemmatizer = WordNetLemmatizer()
lemmatize_words = [lemmatizer.lemmatize(word) for word in words_in_quote]
print("lemmatize_words of question",lemmatize_words)
