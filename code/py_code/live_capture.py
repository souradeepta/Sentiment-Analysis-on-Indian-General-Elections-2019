
# start twitter stream
# get data
# extract and tun senti analysis
#   - both text blob and NB
# compose json
#   - cleanse and enhance: see json_loadsql
# push to ES

import sys, traceback

from tweepy import Stream
from tweepy import OAuthHandler

from twitter_stream_handler import twitter_streaming

#consumer key, consumer secret, access token, access secret which is passed to the oauth for tweepy.
consumer_key="Hg9dhbMGPQ3s2z5Jzde5oRwKu"
consumer_secret="iiJUk1zuWhUZdv4RICKuYxAqwVAVQ4MR3mX83RgPgYXcoFVUlF"
access_token="1068606021185282050-ZBPQSAo87KwUztDU8eLoCeTHS3h8zn"
access_secret="Yr7Sl41bmAZS9CRof4LZyHhUxLgUMflvVfepnC2FtpePq"

def start():
    # Twitter Authorization path
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_secret)

    # while True:
    try:
        # create twitter stream, which in turn will start streaming tweeets in JSON format,
        #which we are using to query its metadata and store them separately on to the database
        twitterStream = Stream(auth, twitter_streaming())
        print('stream created...')

        # party keywords  to search for in tweets
        twitterStream.filter(track=["modi","namo","narendramodi","phirekbaarmodisarkar", "bharatiyajanataparty","bjp",\
                                    "nationaldemocraticalliance", "nda",\
                                     "vajpayee", "indiannationalcongress", "gandhi", "rahulgandhi", "soniagandhi","priyankagandhi",\
                                    "rahulgandhiforpm"], languages=["en"])

        # twitterStream.filter(track=["amethi", "incindia", "indiannationalcongress","sonia", "gandhi", "rahulgandhi", "soniagandhi","priyankagandhi",\
        #                             "rahulgandhiforpm"], languages=["en"])
        print('processing...')
    except:
        print("Exception found")
        print("-"*60)
        traceback.print_exc(file=sys.stdout)
        print("-"*60)
        start()


if __name__ == '__main__':
    start()