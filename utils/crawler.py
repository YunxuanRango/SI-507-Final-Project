import requests
from bs4 import BeautifulSoup
import requests_cache
from nltk.corpus import stopwords
import spacy
from scipy.spatial.distance import cosine
import json
import os


class FoodBlogCrawler:
    def __init__(self, limit):
        
        self.food_word_cache_filename = 'food_word_cache.json'
        self.food_word_cache = self.load_food_word_cache()
        self.limit = limit
        
        if not (self.food_word_cache and \
        'FOOD' in self.food_word_cache and len(self.food_word_cache['FOOD']) == self.limit and \
        'GPE' in self.food_word_cache and len(self.food_word_cache['GPE']) == self.limit):
            print("Initializing crawler...")
            requests_cache.install_cache('crawler_cache', expire_after=1800)  # Cache for 30 minutes
            self.session = requests.Session()
            
            self.nlp = spacy.load("en_core_web_md")
            self.stop_words = set(stopwords.words('english'))
            

            
            # Define a list of food-related words
            food_words = ['food', 'cuisine', 'dish', 'meal', 'ingredient']
            # Calculate the average vector for the food-related words
            self.food_vector = self.average_vector(food_words)
        
    def save_keywords_cache(self, all_keywords):
        """Save the keywords to a JSON file."""
        try:
            # Since all_keywords['FOOD'] and all_keywords['GPE'] are sets, we can directly convert them to lists
            # No need to check for numpy booleans because sets only contain the keywords, not the True/False values

            # Combine the 'FOOD' and 'GPE' keywords into one dictionary
            combined_keywords_to_save = {'FOOD': list(all_keywords['FOOD']), 'GPE': list(all_keywords['GPE'])}

            with open(self.food_word_cache_filename, 'w') as f:
                json.dump(combined_keywords_to_save, f, indent=4)
        except IOError as e:
            print(f"IOError while saving keywords cache: {e}")

            
    def load_food_word_cache(self):
        """Load the food word cache from a JSON file."""
        if os.path.exists(self.food_word_cache_filename):
            try:
                with open(self.food_word_cache_filename, 'r') as f:
                    loaded_cache = json.load(f)
                    # Convert the lists back to sets for consistency
                    loaded_cache['FOOD'] = set(loaded_cache.get('FOOD', []))
                    loaded_cache['GPE'] = set(loaded_cache.get('GPE', []))
                    return loaded_cache
            except json.JSONDecodeError:
                print(f"JSON decode error in {self.food_word_cache_filename}. Starting with an empty cache.")
                return {'FOOD': set(), 'GPE': set()}
        else:
            return {'FOOD': set(), 'GPE': set()}  # Return empty sets if the file does not exist



    def average_vector(self, words):
        """Calculate the average vector for a list of words using the spaCy model."""
        vectors = [self.nlp.vocab[word].vector for word in words if self.nlp.vocab[word].has_vector]
        return sum(vectors) / len(vectors) if vectors else None
        
    def is_food_word(self, word):
        """Determine if a word is related to food using vector similarity."""
        # Check if the word has been processed before
        if word in self.food_word_cache:
            return self.food_word_cache[word]
        
        # Compute the result if the word is new
        result = cosine(self.nlp.vocab[word].vector, self.food_vector) < 0.5
        self.food_word_cache[word] = result
        # Do not save the cache here
        return result
    
    def crawl(self, url):
        headers = {
            'User-Agent': 'Mozilla/5.0 ... Safari/537.36'
        }
        response = self.session.get(url, headers=headers)
        response.raise_for_status()
        return BeautifulSoup(response.text, 'html.parser')

    def extract_food_related_keywords(self, text):
        """Extract food-related keywords using spaCy NER and additional filtering."""
        doc = self.nlp(text)
        food_related_keywords = {
            "GPE": set(),
            "FOOD": set(),
        }
        for ent in doc.ents:
            if ent.label_ == "GPE":
                food_related_keywords["GPE"].add(ent.text)
        
        for token in doc:
            if token.pos_ == 'NOUN' and token.text.lower() not in self.stop_words:
                if token.is_alpha and len(token.text) > 1:
                    # Check the cache first to avoid unnecessary calculations
                    if token.text.lower() in self.food_word_cache:
                        if self.food_word_cache[token.text.lower()]:
                            food_related_keywords["FOOD"].add(token.text.lower())
                    else:
                        if self.is_food_word(token.text):
                            food_related_keywords["FOOD"].add(token.text.lower())
        
        return food_related_keywords

    def crawl_multiple_websites(self, urls):
        # Check if the cache is not empty and the length matches the current limit
        if self.food_word_cache and \
        'FOOD' in self.food_word_cache and len(self.food_word_cache['FOOD']) == self.limit and \
        'GPE' in self.food_word_cache and len(self.food_word_cache['GPE']) == self.limit:
            return self.food_word_cache

        # If the cache is empty or the number of food-related keywords doesn't match the limit,
        # proceed with crawling and updating the cache
        all_keywords = {
            "GPE": set(),
            "FOOD": set(),
        }
        for url in urls:
            soup = self.crawl(url)
            food_related_keywords = self.extract_food_related_keywords(soup.get_text())
            all_keywords["GPE"].update(food_related_keywords["GPE"])
            all_keywords["FOOD"].update(food_related_keywords["FOOD"])

        # After aggregating the results from all URLs, apply the limit
        all_keywords['FOOD'] = set(list(all_keywords['FOOD'])[:self.limit])
        all_keywords['GPE'] = set(list(all_keywords['GPE'])[:self.limit])
        
        # Update the cache with the new keywords for both 'FOOD' and 'GPE'
        for keyword_type in all_keywords:
            for keyword in all_keywords[keyword_type]:
                self.food_word_cache[keyword] = True

        # Save the updated cache
        self.save_keywords_cache(all_keywords)

        return all_keywords

# Example usage:
# crawler = FoodBlogCrawler(limit=5)
# urls = [
#     'https://www.studocu.com/ph/document/western-institute-of-technology/asian-cuisine/introduction-to-cuisine-of-the-world/22576934#:~:text=TOPIC%201%3A%20INTRODUCTION%20TO%20CUISINE,equipment%20used%20in%20Asian',
#     'https://en.wikipedia.org/wiki/List_of_cuisines#:~:text=Regional%20and%20ethnic%20cuisines,with%20its%20food%20served%20worldwide',
#     'https://en.wikipedia.org/wiki/Global_cuisine#:~:text=A%20global%20cuisine%20is%20a,world%2C%20its%20food%20served%20worldwide',
#     'https://www.britannica.com/topic/cuisine',
#     'https://thecookscook.com/guides/ultimate-guide-to-world-cuisine/'
# ]
# keywords = crawler.crawl_multiple_websites(urls)
# print(keywords)
