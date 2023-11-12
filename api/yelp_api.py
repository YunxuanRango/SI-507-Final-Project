import requests
from config import Config

# Assuming the Yelp API key is passed as a parameter to the function
def search_yelp(api_key, keywords, location='New York', limit=10):
    # Set up the endpoint and parameters
    search_url = "https://api.yelp.com/v3/businesses/search"
    headers = {'Authorization': f'Bearer {api_key}'}
    params = {
        'term': ' '.join(keywords),  # Combine keywords into a single string
        'location': location,
        'limit': limit  # Limit the number of results
    }
    
    # Make the request to the Yelp API
    response = requests.get(search_url, headers=headers, params=params)
    if response.status_code == 200:
        # Parse the response to extract relevant data if the request was successful
        return response.json()['businesses']
    else:
        # Handle potential errors - for example, logging or retrying
        response.raise_for_status()

# Example usage:
yelp_data = search_yelp(Config.YELP_API_KEY, ['pizza', 'Italian'], 'Chicago')
print(yelp_data)
