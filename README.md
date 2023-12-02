# SI-507 Final Project
## Analysis of Restaurant Reviews and Social Media Trends with Enhanced Retrieval

### 1. Introduction
This project develops a dining recommendation system by combining trending topics and keywords from online social media and restaurant review platforms, aiming to offer users more accurate and up-to-date dining recommendations based on real-time data.

### 2. How to Run This Project
**Command to run in the terminal:** `python app.py`

#### Required Python Packages

1. **networkx**: For creating and manipulating complex networks.
2. **plotly**: A graphing library for making interactive, publication-quality graphs online.
3. **praw**: Python Reddit API Wrapper, for interacting with Reddit's API.
4. **requests**: For sending HTTP requests.
5. **requests_cache**: Provides a transparent cache for `requests`.
6. **BeautifulSoup** (from bs4): For web scraping, particularly to pull data out of HTML and XML files.
7. **spacy**: Open-source library for advanced natural language processing.
8. **fuzzywuzzy**: Library for string matching.
9. **scipy**: For scientific and technical computing.
10. **flask**: Micro web framework for Python.
11. **dotenv**: Loads environment variables from a `.env` file.
12. **setuptools**: To easily download, build, install, upgrade, and uninstall Python packages.
13. **nltk**: Natural Language Toolkit, for building Python programs to work with human language data.

### 3. Data Sources

#### Web Crawling
Trending topics and keywords were extracted from food blogs and restaurant review websites using `BeautifulSoup` and `Scrapy`, capturing current trends in the culinary world.

#### Yelp Fusion API
The Yelp Fusion API was used to search for restaurants with the obtained keywords. This dataset includes names, ratings, review counts, and user comments, crucial for the recommendation logic.

#### Reddit API
Reddit discussions were integrated to enhance the data analysis. A caching mechanism was implemented to manage API rate limits and improve data retrieval efficiency, storing frequently requested data locally to reduce API calls and speed up response time.

### 4. Data Structure

The data is structured in a graph format, with nodes representing individual restaurants and discussions. Edges indicate relationships based on shared keywords and sentiments, aiding in the visualization of connections and supporting the recommendation algorithms.

### 5. Interaction and Presentation Plans

The "Keyword Graph Visualizer," a Flask-based web application, is the platform for user interaction. It allows users to input or select keywords, displaying a network graph of related restaurants and discussions, enabling users to explore new dining experiences linked to current trends.

### Main Page Layout

The main page features pre-generated keywords and lists recommended restaurants based on a similarity score, providing immediate, relevant recommendations.

![Main Page Screenshot](https://github.com/YunxuanRango/SI-507-Final-Project/assets/150485789/f368ae39-d7d2-4d13-80db-91921a0d754e)
