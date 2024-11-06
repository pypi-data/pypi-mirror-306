print("""import nltk
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize
import re

nltk.download('stopwords')
nltk.download('punkt')


file_path = 'text_doc.txt'
with open(file_path) as file:
    text = file.read()


tokens = word_tokenize(text)
stop_words = set(stopwords.words('english'))

filtered_words = [word for word in tokens if word.lower() not in stop_words]
stemmer = PorterStemmer()
stemmed_words = [stemmer.stem(token) for token in filtered_words]
stemmed_words""")

