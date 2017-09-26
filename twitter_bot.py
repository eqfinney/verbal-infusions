#
# talks to the Verbal Infusions Twitter account
# Author: Emily Quinn Finney
# draws from https://scotch.io/tutorials/build-a-tweet-bot-with-python
#

import tweepy

def authenticate_bot('vi.keys'):
    """
    Authenticates the Twitter Bot
    :return: nothing, but should write the data from the HTTP request to file
    """
    with open('vi.keys', 'r') as f:
        d = f.readlines()
        api_key = d[1].strip()
        api_secret = d[0].strip()
        access_token = d[2].strip()
        access_secret = d[3].strip()

    authentication = tweepy.OAuthHandler(api_key, api_secret)
    authentication.set_access_token(access_token, access_secret)

    # create a
    access_object = tweepy.API(authentication)

    return


if __name__ == "__main__":
    test_http_request()