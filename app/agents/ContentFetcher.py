from newspaper import Article, Config


# Article Fetcher Class
class ContentFetcher:
    @staticmethod
    def fetch_article(link: str):
        user_agent = (
            "osint/0.0.1 (Unix; Intel) AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/50.0.2661.102 Safari/537.36"
        )
        config = Config()
        config.browser_user_agent = user_agent
        config.request_timeout = 3
        config.fetch_images = True
        config.memoize_articles = True
        config.follow_meta_refresh = True

        article = Article(link, config=config, keep_article_html=False)
        article.download()
        article.parse()
        return article
