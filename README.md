# SI-507 Final Project
## Analysis of Restaurant Reviews and Social Media Trends with Enhanced Retrieval

### 1. Introduction
This project aims to develop a dining recommendation system by combining trending topics and keywords from online social media and restaurant review platforms. The objective is to offer users more accurate and up-to-date dining recommendations based on real-time data.

### 2. Data Sources

#### Web Crawling:
Utilizing `BeautifulSoup` and `Scrapy`, we extracted trending topics and keywords from food blogs and restaurant review websites. This process is crucial for capturing current trends in the culinary world.

#### Yelp Fusion API:
We integrated the Yelp Fusion API to search for restaurants using keywords from our web crawling. The dataset includes restaurant names, ratings, review counts, and user comments, essential for our recommendation logic.

#### Reddit API:
We also incorporated Reddit discussions to deepen our data analysis, focusing on posts with high engagement metrics to reflect the most current and popular food-related trends. Caching has been implemented to optimize data retrieval.

### 3. Data Structure

Our data is structured into a graph format, where nodes represent individual restaurants and discussions. Edges indicate relationships based on shared keywords and sentiments, facilitating the visualization of connections and powering our recommendation algorithms.

### 4. Interaction and Presentation Plans

The "Keyword Graph Visualizer," a Flask-based web application, is our user interaction platform. It allows users to input or select keywords, displaying a network graph of related restaurants and discussions. This interactive graph helps users explore new dining experiences tied to current trends.

### Main Page Layout

The main page now features pre-generated keywords and lists recommended restaurants based on a similarity score. This enhancement improves user experience by providing immediate, relevant recommendations.

![Main Page Screenshot](https://github.com/YunxuanRango/SI-507-Final-Project/assets/150485789/5385496c-fd33-4119-99d3-2fa15775d180)
