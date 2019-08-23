# Source : https://tweepy.readthedocs.io/en/latest/cursor_tutorial.html#introduction
# Other Refernces : http://docs.tweepy.org/en/v3.5.0/api.html

from tweepy import Stream

from tweepy import API

from tweepy import Cursor
'''
Cursor object, responsible for Iterating through timelines, user lists,
direct messages, etc. and other pagination usage
'''
from tweepy.streaming import StreamListener
'''
class from tweepy module responsible for to listen tweets,
on the basis of certain Hashtags,
'''

from tweepy import OAuthHandler
'''
Class responsible for authenticating
credentials which we stored in other files.
'''

import twitter_credentials
# importing credential file

import numpy as np
import pandas as pd


class TwitterClient():
    def __init__(self, twitter_user=None):
    	'''
    	Contructor, where authentication method is called, 
    	and API module is used to store that authentication
    	get to the user and it's timeline tweets, default is own timeline
    	'''
        self.auth = TwitterAuthenticator().authenticate_twitter_app()
        self.twitter_client = API(self.auth)

        self.twitter_user = twitter_user

    def get_twitter_client_api(self):
        return self.twitter_client

    def get_user_timeline_tweets(self, num_tweets):
        # since it is a class method, so required itself as parameter.
        tweets = []
        for tweet in Cursor(self.twitter_client.user_timeline, id = self.twitter_user).items(num_tweets):
            '''
			this class allows to get specified user timeline tweets, 
			with giving default user as logged in user ( if not specified )
			along with number of tweets to be extracted.
            '''
            tweets.append(tweet)
        return tweets

    def get_friend_list(self, num_friends):
    	'''
    	Utility class function to store name of the friends in list of specified user.
    	'''
        friend_list = []
        for friend in Cursor(self.twitter_client.friends, id=self.twitter_user).items(num_friends):
            friend_list.append(friend)
        return friend_list

    def get_home_timeline_tweets(self, num_tweets):
    	'''
    	Utility class function to store top tweets from home feed of the user.
    	'''
        home_timeline_tweets = []
        for tweet in Cursor(self.twitter_client.home_timeline, id=self.twitter_user).items(num_tweets):
            home_timeline_tweets.append(tweet)
        return home_timeline_tweets

class TwitterAuthenticator():

	def authenticate_twitter_app(self):
		# class taking itself as parameter.
		auth = OAuthHandler(twitter_credentials.CONSUMER_KEY, twitter_credentials.CONSUMER_SECRET)
		auth.set_access_token(twitter_credentials.ACCESS_TOKEN, twitter_credentials.ACCESS_TOKEN_SECRET)
		return auth


class TwitterStreamer():
	'''
	Class for streaming and processing live tweets.
	'''
	def __init__(self):
		self.twitter_authenticator = TwitterAuthenticator()
		pass

	def stream_tweets(self,fetched_tweets_filename, hash_tag_list):
		'''
		This handles Twitter authentication and connection to the Twitter Streaming API,
		along with printing the tweets in compiler as well as 
		saving them in dump file with stated format
		'''
		listener = TwitterListener(fetched_tweets_filename)

		auth = self.twitter_authenticator.authenticate_twitter_app()
		# object from above defined class, for authentication
		
		stream = Stream(auth,listener)
		'''
		Main twitter stream, which has authentication token and 
		method of how the data to be handle.
		'''

		stream.filter(track = hash_tag_list)
		'''
		Inbuilt method to filter out the required tweets from all received tweets
		on the basis of parameters in form of list, keywords, etc.
		'''
class TwitterListener( StreamListener ):
	'''
	Class to print received tweets to StdOUT,
	which inherit from StreamListener class,
	( which provides many in built methods. )
	'''
	def __init__(self, fetched_tweets_filename):
		self.fetched_tweets_filename = fetched_tweets_filename

	def on_data(self, data):
		# used to read data from Streamlistner
		try:
			print(data)

			with open(self.fetched_tweets_filename,'a') as tf:
				'''
				Utility to write tweets [ which are in form of JSON format dict. object ]
				containing all the information, about the tweet, origin of tweet
				who retweeted, etc.
				'''
				tf.write(data)
			return True

		except BaseException as e:
			print("Error on_data: %s" % str(e))
		return True

	def on_error(self, status):
		if status == 420:
			'''
			As twitter have rates of limit, and if twitter thinks that you are extracting the data
			excessively, then the twitter will give error 420, which will stop extracting operation
			
			So, for returning  False on_data method, in case rate limit occurs. 
			'''
			return False
		print(status)

class TweetAnalyzer():
    """
    Functionality for analyzing and categorizing content from tweets.
    """
    def tweets_to_data_frame(self, tweets):
        df = pd.DataFrame(data=[tweet.text for tweet in tweets], columns=['Tweets'])

        df['id'] = np.array([tweet.id for tweet in tweets])
        df['len'] = np.array([len(tweet.text) for tweet in tweets])
        df['date'] = np.array([tweet.created_at for tweet in tweets])
        df['source'] = np.array([tweet.source for tweet in tweets])
        df['likes'] = np.array([tweet.favorite_count for tweet in tweets])
        df['retweets'] = np.array([tweet.retweet_count for tweet in tweets])

        return df

def information_dumper(username):

	twitter_client = TwitterClient(username)
	print("username specified:", username)

	print("",twitter_client.get_user_timeline_tweets(1))
	print("\n\n\n")
	print("friends of the specified users are:",twitter_client.get_friend_list(10))
	print("\n\n\n")
	print("some tweets from home feed are:\n",twitter_client.get_home_timeline_tweets(5))	

if __name__ == "__main__":
	
	twitter_client = TwitterClient()
    tweet_analyzer = TweetAnalyzer()

    api = twitter_client.get_twitter_client_api()

    tweets = api.user_timeline(screen_name="transwert", count=20)

    #print(dir(tweets[0]))
    #print(tweets[0].retweet_count)

    df = tweet_analyzer.tweets_to_data_frame(tweets)
    
    print(df.head(10))
