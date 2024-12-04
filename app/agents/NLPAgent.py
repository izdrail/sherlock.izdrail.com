import spacy
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import classification_report
import json

class NLPAgent:
    def __init__(self):
        # Load spaCy model and NLTK resources
        self.nlp = spacy.load("en_core_web_sm")
        self.stop_words = set(stopwords.words("english"))
        self.vectorizer = CountVectorizer()
        self.classifier = MultinomialNB()

    def preprocess_text(self, text, use_spacy=True):
        """
        Preprocess text using spaCy or NLTK
        :param text: Input text
        :param use_spacy: Use spaCy if True, else use NLTK
        :return: Cleaned text
        """
        if use_spacy:
            doc = self.nlp(text)
            tokens = [token.lemma_.lower() for token in doc if not token.is_stop and token.is_alpha]
        else:
            tokens = word_tokenize(text)
            tokens = [word.lower() for word in tokens if word.isalpha() and word not in self.stop_words]
        return " ".join(tokens)

    def train_model(self, data, labels):
        """
        Train a Naive Bayes model on the provided data
        :param data: List of input texts
        :param labels: Corresponding labels
        """
        X = self.vectorizer.fit_transform(data)
        self.classifier.fit(X, labels)

    def classify_text(self, text):
        """
        Classify a given text using the trained model
        :param text: Input text
        :return: Predicted class
        """
        processed_text = self.preprocess_text(text)
        X = self.vectorizer.transform([processed_text])
        return self.classifier.predict(X)[0]

    def generate_report(self, texts, labels):
        """
        Generate a classification report
        :param texts: List of input texts
        :param labels: True labels
        :return: Classification report
        """
        predictions = [self.classify_text(text) for text in texts]
        return classification_report(labels, predictions, output_dict=True)
