from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import spacy
from newspaper import Article, Config
from markdownify import markdownify as md
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import yake
import socials
import socid_extractor
import socialshares
from spacy import displacy

# Initialize FastAPI Router
router = APIRouter()

# Load SpaCy Model
nlp = spacy.load("en_core_web_md")

# Initialize Sentiment Analyzer
sentiment_analyzer = SentimentIntensityAnalyzer()

# Constants
EXCLUDED_ENTITY_TYPES = {"TIME", "DATE", "LANGUAGE", "PERCENT", "MONEY", "QUANTITY", "ORDINAL", "CARDINAL"}

# Request Models
class ArticleAction(BaseModel):
    link: str


class SummarizeAction(BaseModel):
    text: str


# Helper Functions
def fetch_article(link: str) -> Article:
    """Fetch and parse an article using the Newspaper library."""
    try:
        user_agent = (
            "NLP/0.0.1 (Unix; Intel)"
            "Chrome/123.0.0"
        )
        config = Config()
        config.browser_user_agent = user_agent
        config.request_timeout = 10
        config.fetch_images = True
        config.memoize_articles = True
        config.follow_meta_refresh = True

        article = Article(link, config=config, keep_article_html=True)
        article.download()
        article.parse()
        return article
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to fetch article: {str(e)}")


def extract_keywords(
        text: str, language: str = "en", n: int = 1, dedup_lim: float = 0.9, top: int = 5
) -> list[tuple[str, float]]:
    """Extract keywords using YAKE."""
    extractor = yake.KeywordExtractor(lan=language, n=n, dedupLim=dedup_lim, top=top)
    return sorted(extractor.extract_keywords(text), key=lambda x: x[1])


def filter_entities(doc) -> list[tuple[str, str]]:
    """Filter and deduplicate named entities."""
    return list(
        dict.fromkeys(
            (ent.label_, ent.text) for ent in doc.ents if ent.label_ not in EXCLUDED_ENTITY_TYPES
        )
    )


def perform_social_analysis(link: str, text: str) -> dict:
    """Perform social and sentiment analysis on the article."""
    try:
        social_accounts = socials.extract(link).get_matches_per_platform()
        social_shares = socialshares.fetch(
            link, platforms=["facebook", "pinterest", "linkedin", "google", "reddit"]
        )
        sentiment_scores = sentiment_analyzer.polarity_scores(text)
        accounts = socid_extractor.extract(text)
        return {
            "social_accounts": social_accounts,
            "social_shares": social_shares,
            "sentiment": sentiment_scores,
            "accounts": accounts,
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Social analysis failed: {str(e)}")


# Routes
@router.post("/nlp/article")
async def process_article(article: ArticleAction):
    try:
        # Fetch and process article
        fetched_article = fetch_article(article.link)
        doc = nlp(fetched_article.text)
        filtered_entities = filter_entities(doc)

        # Social and Sentiment Analysis
        social_analysis = perform_social_analysis(article.link, fetched_article.text)

        # Generate SpaCy HTML
        spacy_html = displacy.render(
            doc, style="ent", options={"ents": [e[0] for e in filtered_entities]}
        )

        # Extract Keywords
        keywords = extract_keywords(fetched_article.text, top=5)

        # Response
        return {
            "data": {
                "title": fetched_article.title,
                "date": fetched_article.publish_date,
                "text": fetched_article.text,
                "markdown": md(
                    fetched_article.article_html,
                    newline_style="BACKSLASH",
                    strip=["a"],
                    heading_style="ATX",
                ),
                "html": fetched_article.article_html,
                "summary": fetched_article.summary,
                "keywords": keywords,
                "authors": fetched_article.authors,
                "banner": fetched_article.top_image,
                "images": fetched_article.images,
                "entities": filtered_entities,
                "videos": fetched_article.movies,
                "social": social_analysis["social_accounts"],
                "spacy": spacy_html,
                "spacy_markdown": md(
                    spacy_html, newline_style="BACKSLASH", strip=["a"], heading_style="ATX"
                ),
                "sentiment": social_analysis["sentiment"],
                "accounts": social_analysis["accounts"],
                "social-shares": social_analysis["social_shares"],
            }
        }
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {str(e)}")


@router.post("/nlp/tags")
async def extract_tags(article: SummarizeAction):
    try:
        keywords = extract_keywords(article.text, n=3, top=5)
        return {"data": keywords}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Keyword extraction failed: {str(e)}")
