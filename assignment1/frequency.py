import sys
import json
from collections import defaultdict

hist = defaultdict(float)
total = 0

# Populates word frequency in tweets
def create_histogram(fp):
	lines = fp.readlines()
	for line in lines:
		tweet = json.loads(line)
		if 'text' in tweet:
			text = tweet['text'].encode('utf-8')
			wordlist = text.split()
			for word in wordlist:
				hist[word] += 1.0
				global total 
				total += 1

def print_histogram():
	for k,v in hist.items():
		print k, v / total


def main():
	tweet_file = open(sys.argv[1])
	create_histogram(tweet_file)
	print_histogram()


if __name__ == '__main__':
	main()