import sys
import json
import string
from collections import defaultdict

sentiment_dict = defaultdict(float)
state_sents = defaultdict(int)
 
def populate_sentiment_dict(fp):
	lines = fp.readlines()
	for line in lines: 
		pair = line.rsplit('\t', 1)
		sentiment_dict[pair[0].strip()] = pair[1].strip()

# Sentiment analysis from bunch of tweets
def calculate_sentiment(fp):
	lines = fp.readlines()
	for line in lines:
		tweet = json.loads(line)
		# user,text and place objects are available in tweet
		if 'user' in tweet and 'text' in tweet and 'place' in tweet and tweet['place'] is not None: 
			# filter out non-english tweets
			if 'lang' in tweet['user'] and tweet['user']['lang'] == 'en': 
				# filter out non-US located tweets
				if 'country_code' in tweet['place'] and tweet['place']['country_code'] == 'US':
					fullname = tweet['place']['full_name']
					state_code = fullname.split()[-1]
					sent = generate_sentiment(generate_terms(tweet['text']))
					state_sents[state_code] += int(sent) 

# Calculates happiest state from state-sentiment dictionary
def calculate_happiest_state():
	print max(state_sents.iterkeys(), key = lambda x: state_sents[x])		

# Generates total sentiment by adding up sentiments of individual terms
def generate_sentiment(termlist):
	total_sentiment = 0.0
	for term in termlist: total_sentiment += float(sentiment_dict[term])
	return total_sentiment

# Gets a twitter text and returns terms out of it
def generate_terms(text):
	terms = []
	words = text.split()
	i = 0
	n = len(words)
	while i < n:
		poss_term = ' '.join(words[i:i+3])
		if poss_term in sentiment_dict:
			terms.append(poss_term)
			i += 3
			continue
		poss_term = ' '.join(words[i:i+2])
		if poss_term in sentiment_dict:
			terms.append(poss_term)
			i += 2
			continue
		poss_term = ' '.join(words[i:i+1])
		if poss_term in sentiment_dict:
			terms.append(poss_term)
		i += 1
	return terms

def main():
	sent_file = open(sys.argv[1])
	tweet_file = open(sys.argv[2])

	populate_sentiment_dict(sent_file)
	calculate_sentiment(tweet_file)
	calculate_happiest_state()

if __name__ == '__main__':
	main()
