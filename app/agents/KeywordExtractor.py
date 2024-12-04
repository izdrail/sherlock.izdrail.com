import yake


# Keyword Extractor Class
class KeywordExtractor:
    @staticmethod
    def extract_keywords(text: str, language="en", n=1, dedup_lim=0.9, top=5):
        extractor = yake.KeywordExtractor(lan=language, n=n, dedupLim=dedup_lim, top=top)
        return sorted(extractor.extract_keywords(text), key=lambda x: x[1])
