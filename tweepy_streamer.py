from tweepy.streaming import StreamListener
'''
Class from tweepy module responsible for to listen tweets,
on the basis of certain Hashtags,
'''

from tweepy import OAuthHandler
'''
Class responsible for authenticating
credentials which we stored in other files.
'''

from tweepy import Stream

import twitter_credentials
# Importing credential file

class TwitterStreamer():
	'''
	Class for streaming and processing live tweets.
	'''
	def __init__(self):
		pass

	def stream_tweets(self,fetched_tweets_filename, hash_tag_list):
		'''
		This handles Twitter authentication and connection to the Twitter Streaming API,
		along with printing the tweets in compiler as well as 
		saving them in dump file with stated format
		'''
		listener = StdOutListener(fetched_tweets_filename)
		auth = OAuthHandler(twitter_credentials.CONSUMER_KEY, twitter_credentials.CONSUMER_SECRET)
		auth.set_access_token(twitter_credentials.ACCESS_TOKEN, twitter_credentials.ACCESS_TOKEN_SECRET)

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
		# if error occurs, prints it out
		print(status)

if __name__ == "__main__":
	
	hash_tag_list = ["kubernetes","open","source"]
	# list of the hashtags which will be used to filter out needed tweets

	fetched_tweets_filename = "garbage_tweets.json"
	# file in which filtered tweets will be saved
	
	twitter_streamer = TwitterStreamer()
	twitter_streamer.stream_tweets(fetched_tweets_filename , hash_tag_list)
