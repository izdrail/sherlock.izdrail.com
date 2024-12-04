import sys
import math
import bs4 as bs
import urllib.request
import re
import nltk
from nltk.stem import WordNetLemmatizer
import spacy
from concurrent.futures import ProcessPoolExecutor

# Execute this line if you are running this code for the first time
nltk.download('wordnet')

# Initializing few variables
nlp = spacy.load('en_core_web_md')
lemmatizer = WordNetLemmatizer()


# Defining TextProcessor Class
class TextProcessor:
    def __init__(self, sentences):
        self.sentences = sentences
        self.stopWords = nlp.Defaults.stop_words

    # Function to calculate frequency of word in each sentence
    def frequency_matrix(self):
        freq_matrix = {}

        for sent in self.sentences:
            freq_table = {}  # dictionary with 'words' as key and their 'frequency' as value

            # Getting all words from the sentence in lower case
            words = [word.text.lower() for word in sent if word.text.isalnum()]

            for word in words:
                word = lemmatizer.lemmatize(word)  # Lemmatize the word
                if word not in self.stopWords:  # Reject stopwords
                    if word in freq_table:
                        freq_table[word] += 1
                    else:
                        freq_table[word] = 1

            freq_matrix[sent[:15]] = freq_table

        return freq_matrix

    # Function to calculate Term Frequency (TF) of each word
    def tf_matrix(self, freq_matrix):
        tf_matrix = {}

        for sent, freq_table in freq_matrix.items():
            tf_table = {}  # dictionary with 'word' itself as a key and its TF as value

            total_words_in_sentence = len(freq_table)
            for word, count in freq_table.items():
                tf_table[word] = count / total_words_in_sentence

            tf_matrix[sent] = tf_table

        return tf_matrix

    # Function to find how many sentences contain a 'word'
    def sentences_per_words(self, freq_matrix):
        sent_per_words = {}

        for sent, f_table in freq_matrix.items():
            for word, count in f_table.items():
                if word in sent_per_words:
                    sent_per_words[word] += 1
                else:
                    sent_per_words[word] = 1

        return sent_per_words

    # Function to calculate Inverse Document Frequency (IDF) for each word
    def idf_matrix(self, freq_matrix, sent_per_words, total_sentences):
        idf_matrix = {}

        for sent, f_table in freq_matrix.items():
            idf_table = {}

            for word in f_table.keys():
                idf_table[word] = math.log10(total_sentences / float(sent_per_words[word]))

            idf_matrix[sent] = idf_table

        return idf_matrix

    # Function to calculate Tf-Idf score of each word
    def tf_idf_matrix(self, tf_matrix, idf_matrix):
        tf_idf_matrix = {}

        for (sent1, f_table1), (sent2, f_table2) in zip(tf_matrix.items(), idf_matrix.items()):

            tf_idf_table = {}

            # word1 and word2 are the same
            for (word1, tf_value), (word2, idf_value) in zip(f_table1.items(), f_table2.items()):
                tf_idf_table[word1] = float(tf_value * idf_value)

            tf_idf_matrix[sent1] = tf_idf_table

        return tf_idf_matrix

    # Function to rate every sentence with some score calculated on the basis of Tf-Idf
    def score_sentences(self, tf_idf_matrix):
        sentenceScore = {}

        for sent, f_table in tf_idf_matrix.items():
            total_tfidf_score_per_sentence = 0

            total_words_in_sentence = len(f_table)
            for word, tf_idf_score in f_table.items():
                total_tfidf_score_per_sentence += tf_idf_score

            if total_words_in_sentence != 0:
                sentenceScore[sent] = total_tfidf_score_per_sentence / total_words_in_sentence

        return sentenceScore

    # Function calculating average sentence score
    def average_score(self, sentence_score):
        total_score = 0
        for sent in sentence_score:
            total_score += sentence_score[sent]

        average_sent_score = (total_score / len(sentence_score))

        return average_sent_score

    # Function to return the summary of the article
    def create_summary(self, sentence_score, threshold):
        summary = ''

        for sentence in self.sentences:
            if sentence[:15] in sentence_score and sentence_score[sentence[:15]] >= threshold:
                summary += " " + sentence.text

        return summary

    # New function: parallelize processing using multiprocessing
    def parallelize_processing(self, func, *args):
        """Process text data in parallel to speed up computations."""
        with ProcessPoolExecutor() as executor:
            results = executor.map(func, *args)
        return list(results)

    # New function: Summarize article based on its TF-IDF scores
    def summarize_article(self, tf_matrix, idf_matrix):
        tf_idf = self.tf_idf_matrix(tf_matrix, idf_matrix)
        sentence_score = self.score_sentences(tf_idf)
        avg_score = self.average_score(sentence_score)
        summary = self.create_summary(sentence_score, avg_score)
        return summary
