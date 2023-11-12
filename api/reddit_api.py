import praw
from config import Config


def search_reddit(client_id, client_secret, user_agent, keywords, limit=10):
    # Initialize the Reddit connection using PRAW
    reddit = praw.Reddit(client_id=client_id,
                         client_secret=client_secret,
                         user_agent=user_agent)
    
    # Combine keywords into a single search query using 'OR'
    search_query = ' OR '.join(keywords)

    # Search the 'food' subreddit for the combined query
    results = reddit.subreddit('food').search(search_query, limit=limit)
    
    # Extract and return the relevant data
    discussions = [{
        'title': submission.title,
        'url': submission.url,
        'score': submission.score,
        'comments': submission.num_comments
    } for submission in results]
    
    return discussions

# Example usage with multiple keywords
# reddit_discussions = search_reddit(Config.REDDIT_CLIENT_ID, 
#                                    Config.REDDIT_CLIENT_SECRET, 
#                                    Config.REDDIT_USER_AGENT, 
#                                    ['sushi', 'pizza', 'burger'], 
#                                    limit=10)