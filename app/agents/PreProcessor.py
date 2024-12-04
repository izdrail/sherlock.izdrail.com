from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from spacy import displacy
import spacy

# Constants
EXCLUDED_ENTITY_TYPES = {"TIME", "DATE", "LANGUAGE", "PERCENT", "MONEY", "QUANTITY", "ORDINAL", "CARDINAL"}


# Base NLP Processor Class
class PreProcessor:
    def __init__(self):
        self.nlp = spacy.load("en_core_web_md")
        self.sentiment_analyzer = SentimentIntensityAnalyzer()

    def analyze_sentiment(self, text: str):
        return self.sentiment_analyzer.polarity_scores(text)

    def extract_entities(self, text: str):
        doc = self.nlp(text)
        entities = [
            (ent.label_, ent.text) for ent in doc.ents if ent.label_ not in EXCLUDED_ENTITY_TYPES
        ]
        return list(dict.fromkeys(entities))  # Deduplicate by text

    def generate_spacy_html(self, text: str, entities):
        doc = self.nlp(text)
        return displacy.render(doc, style="ent", options={"ents": [e[0] for e in entities]})
