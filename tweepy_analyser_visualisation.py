# Source : https://tweepy.readthedocs.io/en/latest/cursor_tutorial.html#introduction
# Other Refernces : http://docs.tweepy.org/en/v3.5.0/api.html

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

import twitter_credentials
# importing credential file

from tweepy import OAuthHandler
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

class TwitterAuthenticator():
    '''
    Class responsible for authenticating
    credentials which we stored in other files.
    '''
    def authenticate_twitter_app(self):
        # class taking itself as parameter.
        auth = OAuthHandler(twitter_credentials.CONSUMER_KEY,
                            twitter_credentials.CONSUMER_SECRET)
        auth.set_access_token(twitter_credentials.ACCESS_TOKEN,
                              twitter_credentials.ACCESS_TOKEN_SECRET)
        return auth

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
        for tweet in Cursor(self.twitter_client.user_timeline, id=self.twitter_user).items(num_tweets):
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


class TweetAnalyzer():
    '''
    Functionality for analyzing and categorizing content from tweets.
    '''

    def tweets_to_data_frame(self, tweets):
        df = pd.DataFrame(
            data=[tweet.text for tweet in tweets], columns=['tweets'])

        df['id'] = np.array([tweet.id for tweet in tweets])
        df['len'] = np.array([len(tweet.text) for tweet in tweets])
        df['date'] = np.array([tweet.created_at for tweet in tweets])
        df['source'] = np.array([tweet.source for tweet in tweets])
        df['likes'] = np.array([tweet.favorite_count for tweet in tweets])
        df['retweets'] = np.array([tweet.retweet_count for tweet in tweets])

        return df


if __name__ == "__main__":

    twitter_client = TwitterClient()
    tweet_analyzer = TweetAnalyzer()
    # object of the class

    api = twitter_client.get_twitter_client_api()

    tweets = api.user_timeline(screen_name="transwert", count=500)

    # print(dir(tweets[0]))
    # utiltiy to find out what things we can extract from the tweets.

    # print(tweets[0].retweet_count)

    df = tweet_analyzer.tweets_to_data_frame(tweets)
    print(df.head(19))

    # for getting average lenght over all tweets.
    print(np.mean(df['len']))

    # for getting the number of likes for the most liked tweet
    print(np.max(df['likes']))

    # for getting the number of retweets for the most retweeted tweet.
    print(np.max(df['retweets']))

    # Plotting Time-Series:

    # for plotting number of likes (y-axis) v.s. on which date (x-axis)
    time_likes = pd.Series(data = df['likes'].values, index = df['date'])
    time_likes.plot( color='r', label = "No. of likes", legend = True)
    # plt.show()

    # for plotting number of retweets (y-axis) v.s. on which date (x-axis)
    time_retweets = pd.Series(data = df['retweets'].values, index = df['date'])
    time_retweets.plot( color='b', label = "No. of retweets", legend = True)
    plt.show()


