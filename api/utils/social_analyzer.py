from .nltk_tools import *
from .twitter_manager import TwitterManager


class SocialAnalizer(object):
    def __init__(self):
        self.twitter_manager = TwitterManager()

    def analyze_users_twitter(self, social_name):
        report = []
        user_tweets = self.twitter_manager.get_user_tweets(social_name)
        for tweet in user_tweets:
            tweet_content = self.twitter_manager.get_tweet_content(tweet)
            clean_tweet = self.twitter_manager.clean_tweet(tweet_content)
            keywords = get_keywords(clean_tweet)
            analysis = analyze_sentiment(clean_tweet)
            analysis['tweet'] = tweet_content
            analysis['keywords'] = keywords
            report.append(analysis)
        return report



