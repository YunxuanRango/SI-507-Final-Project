import networkx as nx
from config import Config
from api.reddit_api import search_reddit
from api.yelp_api import search_yelp
from heapq import nlargest
from fuzzywuzzy import fuzz
import plotly
import plotly.graph_objs as go
from plotly.offline import plot
from datetime import datetime, timedelta
import json
import os

class RestaurantGraphBuilder:
    def __init__(self, yelp_keywords, reddit_keywords, location='Chicago'):
        self.graph = nx.Graph()
        self.yelp_data = self.fetch_yelp_data(yelp_keywords, location, limit=50)
        self.reddit_data = self.fetch_reddit_data(reddit_keywords, limit=50)
        self.build_graph()

    def calculate_similarity(self, restaurant_info, discussion_title):
        match_score = fuzz.partial_ratio(restaurant_info['name'].lower(), discussion_title.lower())
        #print(f"Matching '{restaurant_info['name'].lower()}' with '{discussion_title.lower()}': Score {match_score}")
        return match_score >= 30  # Temporarily lower the threshold for debugging
    
    def fetch_yelp_data(self, keywords, location, limit):
        cache_file = f"yelp_data_{location}.json"
        # Check if we have cached data
        if os.path.exists(cache_file):
            with open(cache_file, 'r') as f:
                cached_data = json.load(f)
                # Check if the cache is still valid
                if datetime.now() - datetime.strptime(cached_data['timestamp'], '%Y-%m-%dT%H:%M:%S.%f') < timedelta(hours=1):
                    return cached_data['data']
        
        # If not, fetch new data and cache it
        data = search_yelp(Config.YELP_API_KEY, keywords, location,limit=50)
        with open(cache_file, 'w') as f:
            json.dump({'data': data, 'timestamp': datetime.now().isoformat()}, f)
        return data

    def fetch_reddit_data(self, keywords, limit):
        cache_file = f"reddit_data.json"
        # Check if we have cached data
        if os.path.exists(cache_file):
            with open(cache_file, 'r') as f:
                cached_data = json.load(f)
                # Check if the cache is still valid
                if datetime.now() - datetime.strptime(cached_data['timestamp'], '%Y-%m-%dT%H:%M:%S.%f') < timedelta(hours=1):
                    return cached_data['data']
        
        # If not, fetch new data and cache it
        data = search_reddit(Config.REDDIT_CLIENT_ID, Config.REDDIT_CLIENT_SECRET, Config.REDDIT_USER_AGENT, keywords,limit=50)
        with open(cache_file, 'w') as f:
            json.dump({'data': data, 'timestamp': datetime.now().isoformat()}, f)
        return data


    def build_graph(self):
        #print("Building graph...")
        # Add nodes for restaurants
        for restaurant in self.yelp_data:
            #print(f"Adding restaurant node: {restaurant['name']}")
            self.graph.add_node(restaurant['id'], type='restaurant', **restaurant)
        
        # Add nodes for discussions and edges based on similarity
        for discussion in self.reddit_data:
            #print(f"Adding discussion node: {discussion['title']}")
            self.graph.add_node(discussion['url'], type='discussion', **discussion)
            for restaurant in self.yelp_data:
                if self.calculate_similarity(restaurant, discussion['title']):
                    #print(f"Adding edge between: {restaurant['name']} and discussion {discussion['title']}")
                    self.graph.add_edge(restaurant['id'], discussion['url'])

        #print(f"Graph built with {self.graph.number_of_nodes()} nodes and {self.graph.number_of_edges()} edges")


    def analyze_graph(self):
        # Find the restaurant with the highest degree (most discussions connected)
        restaurant_degrees = {node: val for node, val in self.graph.degree() if self.graph.nodes[node]['type'] == 'restaurant'}
        most_discussed_restaurant = max(restaurant_degrees, key=restaurant_degrees.get)
        return self.graph.nodes[most_discussed_restaurant]['name']
    
    def calculate_similarity_scores(self):
        """
        Calculate similarity scores for each pair of restaurants.
        This method assumes that if two restaurants are mentioned in the same discussions, they are similar.
        """
        similarity_scores = {}
        for node1, node2 in self.graph.edges():
            if self.graph.nodes[node1]['type'] == 'restaurant' and self.graph.nodes[node2]['type'] == 'restaurant':
                similarity_scores[(node1, node2)] = similarity_scores.get((node1, node2), 0) + 1
        return similarity_scores

    def recommend_similar_restaurants(self, restaurant_id, top_n=5):
        # First, ensure the restaurant exists in the graph
        if restaurant_id not in self.graph:
            print(f"Restaurant ID {restaurant_id} does not exist in the graph.")
            return []
        
        # Calculate similarity scores for the given restaurant
        similarity_scores = {node: 0 for node in self.graph.nodes() if self.graph.nodes[node]['type'] == 'restaurant'}
        for node in self.graph.neighbors(restaurant_id):
            if self.graph.nodes[node]['type'] == 'discussion':
                for rest in self.graph.neighbors(node):
                    if rest != restaurant_id and self.graph.nodes[rest]['type'] == 'restaurant':
                        similarity_scores[rest] += 1

        # Debugging print statements
        print(f"Similarity scores: {similarity_scores}")

        # Get the top N similar restaurants based on the similarity score
        most_similar = nlargest(top_n, similarity_scores, key=similarity_scores.get)
        print(f"Most similar restaurants: {most_similar}")
        return [(self.graph.nodes[rest]['name'], similarity_scores[rest]) for rest in most_similar if similarity_scores[rest] > 0]

    def visualize_graph_interactive(self):
        # Get positions for the nodes in the graph
        pos = nx.spring_layout(self.graph)

        # Create edge trace
        edge_trace = go.Scatter(
            x=[],
            y=[],
            line=dict(width=0.5, color='#888'),
            hoverinfo='none',
            mode='lines')

        for edge in self.graph.edges():
            x0, y0 = pos[edge[0]]
            x1, y1 = pos[edge[1]]
            edge_trace['x'] += (x0, x1, None)
            edge_trace['y'] += (y0, y1, None)

        # Create node trace for restaurants
        node_trace_restaurant = go.Scatter(
            x=[],
            y=[],
            text=[],
            mode='markers+text',
            textposition='top center',
            hoverinfo='text',
            marker=dict(
                showscale=True,
                colorscale='YlGnBu',
                color=[],
                size=10,
                colorbar=dict(
                    thickness=15,
                    title='Node Connections',
                    xanchor='left',
                    titleside='right'
                ),
                line_width=2))

        # Create node trace for discussions
        node_trace_discussion = go.Scatter(
            x=[],
            y=[],
            text=[],
            mode='markers+text',
            textposition='top center',
            hoverinfo='text',
            marker=dict(
                color='rgb(255,0,0)',
                size=10,
                line=dict(width=2)))

        for node in self.graph.nodes():
            x, y = pos[node]
            if self.graph.nodes[node]['type'] == 'restaurant':
                node_trace_restaurant['x'] += (x,)
                node_trace_restaurant['y'] += (y,)
                node_trace_restaurant['text'] += (self.graph.nodes[node]['name'],)
                node_trace_restaurant['marker']['color'] += (self.graph.degree[node],)
            else:  # 'type' == 'discussion'
                node_trace_discussion['x'] += (x,)
                node_trace_discussion['y'] += (y,)
                node_trace_discussion['text'] += (self.graph.nodes[node]['title'],)

        # Create the figure
        fig = go.Figure(data=[edge_trace, node_trace_restaurant, node_trace_discussion],
                        layout=go.Layout(
                            title='Restaurant and Discussion Graph',
                            titlefont_size=16,
                            showlegend=False,
                            hovermode='closest',
                            margin=dict(b=20, l=5, r=5, t=40),
                            xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                            yaxis=dict(showgrid=False, zeroline=False, showticklabels=False))
                        )

        # Instead of plotting the figure, return it as a JSON object
        graph_json = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
        return graph_json

# # Initialize the builder with API calls
# builder = RestaurantGraphBuilder(['pizza', 'Italian'], ['pizza', 'Italian'])

# # Assuming you have a valid restaurant ID from the Yelp data, use it here
# valid_restaurant_id = builder.yelp_data[0]['id']  # Just as an example, take the first restaurant's ID

# # Get recommendations for the valid restaurant ID
# similar_restaurants = builder.recommend_similar_restaurants(valid_restaurant_id)

# # Print out the recommendations
# for name, score in similar_restaurants:
#     print(f"Restaurant: {name}, Similarity Score: {score}")
    
# # After building the graph
# builder.visualize_graph_interactive()