import os
import re

import tweepy


class TwitterManager(object):
    def __init__(self):
        self.consumer_key = os.environ.get('CONSUMER_KEY', '')
        self.consumer_key_secret = os.environ.get('CONSUMER_KEY_SECRET', '')
        self.access_token = os.environ.get('ACCESS_TOKEN', '')
        self.access_token_secret = os.environ.get('ACCESS_TOKEN_SECRET', '')
        self.auth = tweepy.OAuthHandler(self.consumer_key, self.consumer_key_secret)
        self.auth.set_access_token(self.access_token, self.access_token_secret)
        self.api = tweepy.API(self.auth)

    def get_user_tweets(self, screen_name, count=20):
        return self.api.user_timeline(screen_name=screen_name, count=count, tweet_mode='extended')

    def get_tweet_content(self, tweet):
        return tweet.retweeted_status.full_text if 'retweeted_status' in tweet._json else tweet.full_text

    def clean_tweet(self, tweet):
        '''
        Cleans tweet text by removing links,
        special characters - using regex statements.
        '''

        return ' '.join(re.sub("([^0-9A-Za-z.,!:%’ \t])|(\w+:\/\/\S+)", " ", tweet).split())
