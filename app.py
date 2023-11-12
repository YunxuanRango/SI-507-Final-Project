from flask import Flask, render_template, request, jsonify
from utils.graph_utils import RestaurantGraphBuilder  # Assuming this import is correct
from utils.crawler import FoodBlogCrawler  #
import json
import os

app = Flask(__name__)

# Load the food_word_cache.json file
# if food_word_cache.json is not empty, load it
if os.path.exists('food_word_cache.json') and os.stat('food_word_cache.json').st_size != 0:
    with open('food_word_cache.json') as f:
        food_word_cache = json.load(f)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        keywords = request.json['keywords']
        builder = RestaurantGraphBuilder(keywords.split(), keywords.split())
        
        graph_div = builder.visualize_graph_interactive()
        response = jsonify({'graph_html': graph_div})
        # Log the response for debugging
        app.logger.debug('Graph JSON Response: %s', response.get_data(as_text=True))
        
        return response
    else:
        return render_template('index.html')

@app.route('/api/keywords')
def api_keywords():
    # Check if the cache is empty
    crawler = FoodBlogCrawler(limit=5)
    urls = [
        'https://www.studocu.com/ph/document/western-institute-of-technology/asian-cuisine/introduction-to-cuisine-of-the-world/22576934#:~:text=TOPIC%201%3A%20INTRODUCTION%20TO%20CUISINE,equipment%20used%20in%20Asian',
        'https://en.wikipedia.org/wiki/List_of_cuisines#:~:text=Regional%20and%20ethnic%20cuisines,with%20its%20food%20served%20worldwide',
        'https://en.wikipedia.org/wiki/Global_cuisine#:~:text=A%20global%20cuisine%20is%20a,world%2C%20its%20food%20served%20worldwide',
        'https://www.britannica.com/topic/cuisine',
        'https://thecookscook.com/guides/ultimate-guide-to-world-cuisine/'
    ]
    keywords = crawler.crawl_multiple_websites(urls)
    print(keywords)

    # Convert sets to lists for JSON serialization
    keywords['FOOD'] = list(keywords['FOOD'])
    keywords['GPE'] = list(keywords['GPE'])

    # Endpoint to return the cached keywords for the frontend suggestions
    return jsonify(keywords)


if __name__ == '__main__':
    app.run(debug=False)
