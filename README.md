# SI-507 Final Project
## This is my SI 507 Final Project: Analysis of Restaurant Reviews and Social Media Trends with Enhanced Retrieval

### 1. Introduction
This report documents the progress made in accessing and importing data from my sources for a dining recommendation system. My goal is to combine trending topics and keywords from online social media and restaurant review platforms to provide users with more accurate and up-to-date dining recommendations.

### 2. Data Sources

#### Web Crawling:
I have successfully employed web crawling techniques using `BeautifulSoup` and `Scrapy` to extract trending topics and keywords from food blogs and restaurant review websites. This foundational step has laid the groundwork for capturing real-time trends in the culinary domain.

#### Yelp Fusion API:
I tapped into the Yelp Fusion API to search for restaurants using the keywords obtained from my web crawling phase. This rich dataset comprises critical information such as restaurant names, ratings, review counts, and user comments which are central to our recommendation logic.

#### Reddit API:
Further, I integrated discussions from Reddit to add depth to my data, allowing me to gauge public sentiment and spot emerging trends. By focusing on posts with high engagement metrics, I ensured that my dataset is reflective of the most current and popular food-related discussions.

### 3. Data Structure

I have structured my data into a graph format, where nodes represent individual restaurants and discussions, and edges signify the relationship based on shared keywords and sentiments. This graph not only aids in visualizing connections but also serves as the backbone for our recommendation algorithms.

### 4. Interaction and Presentation Plans

My Flask-based web application, the "Keyword Graph Visualizer," serves as the platform for user interaction. It allows users to input or select keywords, returning a visualization of the related restaurants and discussions. Users can explore this network graph to discover new dining experiences aligned with trending topics.

### Main Page Layout

![Main Page Screenshot](https://github.com/YunxuanRango/SI-507-Final-Project/assets/150485789/5385496c-fd33-4119-99d3-2fa15775d180)
