from twitter import Twitter, OAuth, TwitterHTTPError, TwitterStream

try:
	from HTMLParser import HTMLParser
except ImportError:
	from html.parser import HTMLParser

ACCESS_TOKEN = 'GET YOUR OWN ACCESS TOKEN!'
ACCESS_SECRET = 'GET YOUR OWN ACCESS TOKEN SECRET'
CONSUMER_KEY = 'GET YOUR OWN API KEY'
CONSUMER_SECRET = 'GET YOUR OWN API SECRET'

oauth = OAuth(ACCESS_TOKEN, ACCESS_SECRET, CONSUMER_KEY, CONSUMER_SECRET)

twitter = Twitter(auth=oauth)

html_parser = HTMLParser()


def get_tweets(username):
	for page in xrange(3200/20):
		try:
			tweets_this_page = twitter.statuses.user_timeline(screen_name=username, page=page+1, tweet_mode='extended')
		except Exception:
			break
		for tweet in tweets_this_page:
			yield tweet

def edit_distance(s1, s2):
    m=len(s1)+1
    n=len(s2)+1

    tbl = {}
    for i in range(m): tbl[i,0]=i
    for j in range(n): tbl[0,j]=j
    for i in range(1, m):
        for j in range(1, n):
            cost = 0 if s1[i-1] == s2[j-1] else 1
            tbl[i,j] = min(tbl[i, j-1]+1, tbl[i-1, j]+1, tbl[i-1, j-1]+cost)

    return tbl[i,j]


def same(tweet_text, search_text):
	tweet_text = tweet_text.strip().replace('- ', '').split('https://t.co/')[0].strip()
	search_text = search_text.strip().replace('- ', '')

	min_len = min(len(tweet_text), len(search_text))

	if edit_distance(tweet_text, search_text) < 0.1*min_len:
		return True

	if min_len > 10 and (tweet_text in search_text or search_text in tweet_text):
		return True

	return False


def search_tweet(username, search_tweet):
	tweets = get_tweets(username)
	key_to_text = 'full_text'

	print
	for user_tweet in tweets:
		
		text = html_parser.unescape(user_tweet[key_to_text])#.decode('utf-16')
		# print(text + '\n')
		if same(text, search_tweet):
			id = user_tweet['id']
			url = 'https://twitter.com/{uname}/status/{tid}'.format(uname=username, tid=id)
			print
			return url
	return None

