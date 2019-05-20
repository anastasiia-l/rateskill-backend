import re

from nltk.sentiment.vader import SentimentIntensityAnalyzer
from rake_nltk import Rake
from textblob import TextBlob


def clean_keyword(text):
    return str.strip(' '.join(re.sub("([^A-Za-z ])", " ", text).split()))


def get_keywords(text):
    r = Rake(max_length=3)
    r.extract_keywords_from_text(text)
    return [clean_keyword(word) for word in r.get_ranked_phrases() if len(clean_keyword(word)) > 2]


def analyze_sentiment(text, sentiment_coef=0.2):
    sid = SentimentIntensityAnalyzer()
    polarity_sc = sid.polarity_scores(text)
    textblob = TextBlob(text)
    analysis = dict()
    analysis['polarity'] = polarity_sc['compound']
    analysis['subjectivity'] = textblob.sentiment[1]
    analysis['sentiment'] = 'Positive' if polarity_sc['compound'] >= sentiment_coef \
        else 'Negative' if polarity_sc['compound'] <= -sentiment_coef else 'Neutral'
    return analysis




#
# public_tweets = []
# tf = {}
#
# tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')
# with open('tweets_full.json', 'r') as f:
#     public_tweets = json.load(f)
# # for tweet in public_tweets:
# #
# #     tokens = tokenizer.tokenize(tweet['tweet_text'])
# #     lemmatizer = nltk.stem.WordNetLemmatizer()
# #     tokens = [lemmatizer.lemmatize(token) for token in tokens]
# #     stopwords = set(stopwords.words('english'))
# #     tokens = [token for token in tokens if token not in stopwords]
# #     tf[tweet['tweet_text']] = Counter(tokens)
# #     idf = {}
# #     tfidf = {}
# #     for t in tf[tweet['tweet_text']]:
# #
# #         freeq = len([tweet['tweet_text'].find(t) > 0 for tweet in public_tweets])
# #         freeq = freeq if freeq > 0 else 1
# #         idf[t] = math.log(len(public_tweets) / freeq)
# #
# #         tfidf[t] = tf[tweet['tweet_text']][t] * idf[t]
# #     terms_sorted_tfidf_desc = sorted(tfidf.items(), key=lambda x: -x[1])
# #     terms, scores = zip(*terms_sorted_tfidf_desc)
# #     k = 5
# #     keywords = terms[:k]
# #     print(tweet['tweet_text'])
# #     print(keywords)
#
#