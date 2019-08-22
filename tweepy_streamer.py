from tweepy.streaming import StreamListener 
# class from tweepy module responsible for to listen tweets,
# on the basis of certain Hashtags,
from tweepy import OAuthHandler
# class responsible for authenticating
# credentials which we stored in other files.
from tweepy import Stream

import twitter_credentials
# importing credential file

class TwitterStreamer():
	'''
	Class for streaming and processing live tweets.
	'''
	def __init(self):
		pass

	def stream_tweets(self,fetched_tweets_filename, hash_tag_list):
		# this handles Twitter authentication and connection to the Twitter Streaming API.

		listener = StdOutListener()
		auth = OAuthHandler(twitter_credentials.CONSUMER_KEY, twitter_credentials.CONSUMER_SECRET)
		auth.set_access_token(twitter_credentials.ACCESS_TOKEN, twitter_credentials.ACCESS_TOKEN_SECRET)

		stream = Stream(auth,listener)

		stream.filter(track = hash_tag_list)

class StdOutListener( StreamListener ):
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
				tf.write(data)
			return True
		except BaseException as e:
			print("Error on_data: %s" % str(e))
		return True

	def on_error(self, status):
		# if error occurs
		print(status)

if __name__ == "__main__":
	
	hash_tag_list = ["kubernetes","open","source"]
	fetched_tweets_filename = "tweets.json"
	
	twitter_streamer = TwitterStreamer()
	twitter_streamer.stream_tweets(fetched_tweets_filename , hash_tag_list)