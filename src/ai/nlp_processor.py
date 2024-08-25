import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import LatentDirichletAllocation

class NLPProcessor:
    def __init__(self):
        self.stop_words = set(stopwords.words('english'))
        self.vectorizer = TfidfVectorizer(stop_words='english')
        self.lda = LatentDirichletAllocation(n_components=5, random_state=42)

    def preprocess_text(self, text):
        tokens = word_tokenize(text.lower())
        return [token for token in tokens if token.isalnum() and token not in self.stop_words]

    def extract_topics(self, documents):
        tfidf_matrix = self.vectorizer.fit_transform(documents)
        lda_output = self.lda.fit_transform(tfidf_matrix)
        return lda_output