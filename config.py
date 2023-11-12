import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    YELP_API_KEY = os.getenv('YELP_API_KEY')
    REDDIT_CLIENT_ID = os.getenv('REDDIT_CLIENT_ID')
    REDDIT_CLIENT_SECRET = os.getenv('REDDIT_CLIENT_SECRET')
    REDDIT_USER_AGENT = os.getenv('REDDIT_USER_AGENT')

    @staticmethod
    def validate():
        if not Config.YELP_API_KEY:
            raise ValueError("No Yelp API key found. Set YELP_API_KEY as an environment variable.")
        if not Config.REDDIT_CLIENT_ID:
            raise ValueError("No Reddit Client ID found. Set REDDIT_CLIENT_ID as an environment variable.")
        if not Config.REDDIT_CLIENT_SECRET:
            raise ValueError("No Reddit Client Secret found. Set REDDIT_CLIENT_SECRET as an environment variable.")
        if not Config.REDDIT_USER_AGENT:
            raise ValueError("No Reddit User Agent found. Set REDDIT_USER_AGENT as an environment variable.")