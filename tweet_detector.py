import pytesseract
from PIL import Image
import argparse

import re

import twitter_manager

tweeter_handle_regex = re.compile('(?<=^|(?<=[^a-zA-Z0-9-_\.]))@([A-Za-z]+[A-Za-z0-9]+)')


def get_text_from_image(image_path):
	text = pytesseract.image_to_string(Image.open(image_path))
	# print(text)
	return text


def get_tweet_handles(text):
	tweeter_handles = tweeter_handle_regex.findall(text)
	return tweeter_handles


def get_handle_tweet_pair(chunks):
	pairs = []

	for i in range(len(chunks)):
		handles = tweeter_handle_regex.findall(chunks[i])
		if handles == []:
			handle = None
		else:
			handle = handles[0]
		if handle is not None:
			tweet = chunks[i+1].replace('\n', ' ')
			pairs.append((handle, tweet))

	print(pairs)
	return pairs


def get_chunks(text):
	text = text.strip()
	chunks = text.strip().split('\n\n')
	for chunk in chunks:
		if tweeter_handle_regex.findall(chunk) == []:
			chunks = chunks[1:]
		else:
			break
	return chunks
	

def check_if_fake_tweet(image_path):
	text = get_text_from_image(image_path)
	chunks = get_chunks(text)
	handle_tweet_pairs = get_handle_tweet_pair(chunks)

	for pair in handle_tweet_pairs:
		handle, tweet = pair
		print(u"Searching for \n {}: {}".format(handle, tweet))
		url = twitter_manager.search_tweet(handle, tweet)
		if url is not None:
			print(url)
		else:
			print("NOT FOUND, May wish to Check Manually!")


if __name__ == '__main__':
	ap = argparse.ArgumentParser()
	ap.add_argument("-i", "--image", required=True, help="path to tweet image to be OCR'd")
	args = vars(ap.parse_args())

	image_path = args['image']

	check_if_fake_tweet(image_path)