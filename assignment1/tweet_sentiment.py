import sys
import json
import string
from collections import defaultdict

sentiment_dict = defaultdict(float)
allchars = string.maketrans('', '')
nonletters = allchars.translate(allchars, string.letters)

possible_sentiment_dict = defaultdict(list)

# Populates sentiment dictionary
def populate_sentiment_dict(fp):
	lines = fp.readlines()
	for line in lines: 
		pair = line.rsplit('\t', 1)
		sentiment_dict[pair[0].strip()] = pair[1].strip()

# Sentiment analysis of bunch of tweets, 
# plus sentiment estimation of new found terms 
def calculate_sentiment(fp):
	lines = fp.readlines()
	for line in lines:
		tweet = json.loads(line)
		total_sentiment = 0.0
		if 'text' in tweet:
			text = tweet['text'].encode('utf-8')
			termlist = generate_terms(text)
			nontermlist = diff(text.split(), termlist)
			total_sentiment = generate_sentiment(termlist)
			for nonterm in nontermlist:
				possible_sentiment_dict[nonterm].append(total_sentiment)

# Calculates and prints possible sentiment of a term by simply averaging candidate sentiments
def calculate_possible_sentiment():
	for k,v in possible_sentiment_dict.iteritems():
		print k, sum(v) / len(v)			

# Calculate sentiment of a tweet by simply adding up all sentiments of terms in tweet
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

# Set-difference operation 
def diff(a, b):
    b = set(b)
    return set([aa for aa in a if aa not in b])


def main():
	sent_file = open(sys.argv[1])
	tweet_file = open(sys.argv[2])

	populate_sentiment_dict(sent_file)
	calculate_sentiment(tweet_file)
	calculate_possible_sentiment()

if __name__ == '__main__':
	main()
