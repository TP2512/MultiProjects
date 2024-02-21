import tweepy
from pymongo import MongoClient

# Connect to MongoDB
client = MongoClient('mongodb://localhost:27017/')
db = client['twitter_data']

# Authenticate with Twitter API
auth = tweepy.OAuthHandler('consumer_key', 'consumer_secret')
auth.set_access_token('access_token', 'access_token_secret')
api = tweepy.API(auth)

# Example: Retrieve user's followers and store in MongoDB
user = api.get_user('username')
followers = api.followers_ids(user.id)

# Store followers in MongoDB
followers_collection = db['followers']
followers_collection.insert_many([{'user_id': user.id, 'follower_id': follower_id} for follower_id in followers])

print("Followers data inserted into MongoDB.")
