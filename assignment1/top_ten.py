import sys
import json
import heapq
from collections import defaultdict

hist = defaultdict(int)

TOPN = 10

# Populates histogram dictionary by hashtags of tweets
def create_histogram(fp):
	lines = fp.readlines()
	for line in lines:
		tweet = json.loads(line)
		if 'entities' in tweet:
			if 'hashtags' in tweet['entities']:
				tags = tweet['entities']['hashtags']
				for tag in tags:
					if 'text' in tag:
						hist[tag['text']] += 1

# Prints the top ten hashtag
def print_histogram():
	sorted_keys = sorted(hist.keys(), key=lambda x: hist[x], reverse=True)[:TOPN]
	for key in sorted_keys: print key, float(hist[key])

def main():
	tweet_file = open(sys.argv[1])
	create_histogram(tweet_file)
	print_histogram()

if __name__ == '__main__':
	main()