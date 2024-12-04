from classes.SentimentAnalysis import SentimentRescoring
from classes.TextSummarizer import TextProcessor


# Integrate this into the existing TextProcessor class:
class TextProcessorWithSentiment(TextProcessor, SentimentRescoring):
    def __init__(self, sentences):
        TextProcessor.__init__(self, sentences)
        SentimentRescoring.__init__(self)

    # Overriding the `score_sentences` method to include sentiment re-scoring
    def score_sentences(self, tf_idf_matrix):
        sentenceScore = {}

        for sent, f_table in tf_idf_matrix.items():
            total_tfidf_score_per_sentence = 0

            total_words_in_sentence = len(f_table)
            for word, tf_idf_score in f_table.items():
                total_tfidf_score_per_sentence += tf_idf_score

            if total_words_in_sentence != 0:
                original_score = total_tfidf_score_per_sentence / total_words_in_sentence
                # Apply sentiment rescoring
                adjusted_score = self.rescore_sentiment(sent.text, original_score)
                sentenceScore[sent] = adjusted_score

        return sentenceScore

    # Overriding the `summarize_article` method to reflect sentiment scoring
    def summarize_article(self, tf_matrix, idf_matrix):
        tf_idf = self.tf_idf_matrix(tf_matrix, idf_matrix)
        sentence_score = self.score_sentences(tf_idf)
        avg_score = self.average_score(sentence_score)
        summary = self.create_summary(sentence_score, avg_score)
        return summary
