#
# talks to the Verbal Infusions Twitter account
# Author: Emily Quinn Finney
#

import tweepy
import create_status as cs


def authenticate_bot(filename):
    """
    Authenticates the Twitter Bot
    :return: nothing, but should write the data from the HTTP request to file
    """
    with open(filename, 'r') as f:
        d = f.readlines()
        api_key = d[0].strip()
        api_secret = d[1].strip()
        access_token = d[2].strip()
        access_secret = d[3].strip()

    authentication = tweepy.OAuthHandler(api_key, api_secret)
    authentication.set_access_token(access_token, access_secret)

    return authentication


if __name__ == "__main__":
    auth = authenticate_bot('vi.keys')
    VerbalInfusions = tweepy.API(auth)
    #import ipdb; ipdb.set_trace()
    VerbalInfusions.update_status(cs.markov_tweet('tea_description.txt'))
