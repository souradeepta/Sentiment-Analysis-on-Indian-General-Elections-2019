import json
import re
import time

from tweepy.streaming import StreamListener
from html.parser import HTMLParser
from unidecode import unidecode

from sentiment_analyzer import sentiment, text_blob_sentiment
from tweet_cleanser import prepare_tweet_json
from es_datastore import write_to_es

# Twitter's results just give us back the tweet, but don't tell us which keyword it was found with
# so, we have to use a keyword dictionary to search the tweet and match it back up to the party
party_tags = dict()
#BJP tags
party_tags['modi'] = 'Bharatiya Janata Party'
party_tags['namo'] = 'Bharatiya Janata Party'
party_tags['namo'] = 'Bharatiya Janata Party'
party_tags['phirekbaarmodisarkar'] = 'Bharatiya Janata Party'
party_tags['bharatiyajanataparty']  = 'Bharatiya Janata Party'
party_tags['bjp'] = 'Bharatiya Janata Party'
party_tags['nationaldemocraticalliance'] = 'Bharatiya Janata Party'
party_tags['nda'] = 'Bharatiya Janata Party'
party_tags['vajpayee'] = 'Bharatiya Janata Party'
#congress tags
party_tags['indiannationalcongress'] = 'Indian National Congress'
party_tags['incindia'] = 'Indian National Congress'
party_tags['gandhi'] = 'Indian National Congress'
party_tags['rahulgandhi'] = 'Indian National Congress'
party_tags['soniagandhi'] = 'Indian National Congress'
party_tags['sonia'] = 'Indian National Congress'
party_tags['priyankagandhi'] = 'Indian National Congress'
party_tags['rahulgandhiforpm'] = 'Indian National Congress'
party_tags['inc'] = 'Indian National Congress'
party_tags['congress'] = 'Indian National Congress'
party_tags['amethi'] = 'Indian National Congress'

def clean_tweet(tweet):
    return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet).split())

#build the class used to process tweets to check for feeds
class twitter_streaming(StreamListener):

    def on_data(self, data):
        all_data = json.loads(HTMLParser().unescape(data))
        #https://developer.twitter.com/en/docs/tweets/data-dictionary/overview/tweet-object
        #https://gist.github.com/hrp/900964
        if 'text' in all_data:
            #1
            tweet = all_data['text']
            tweet = unidecode(tweet)
            #2
            tweetID = all_data['id_str']
            #3
            source = all_data['source']
            source = unidecode(source)
            #4
            if all_data['place']:
                country = all_data['place']['country']
                country = unidecode(country)
                #5
                country_code = all_data['place']['country_code']
                country_code = unidecode(country_code)
                #6
                full_name = all_data['place']['full_name']
                full_name = unidecode(full_name)
                #7
                name =  all_data['place']['name']
                name = unidecode(name)
                #8
                place_type = all_data['place']['place_type']
                place_type = unidecode(place_type)
                #9
            else:
                country = country_code = full_name = name = place_type = "0"

            quote_count = all_data['quote_count']
            #10
            reply_count = all_data['reply_count']
            #11
            retweet_count = all_data['retweet_count']
            #12
            favorite_count = all_data['favorite_count']
            #13
            screen_name = all_data['user']['screen_name']
            screen_name = unidecode(screen_name)
            #13
            followers_count = all_data['user']['followers_count']
            #14
            friends_count = all_data['user']['friends_count']
            #15
            verified = all_data['user']['verified']
            #print("verified value is:", verified)
            #type(verified)



            #tweetNoPunctuation = regex.sub('', tweet)
            tweetNoPunctuation = clean_tweet(tweet)
            #we want to make sure while compiling tweets, we do not include the oens that are retweeted
            if not all_data['retweeted'] and not tweet.startswith('RT') and 't.co' not in tweet:
                sentiment_value, confidence = sentiment(tweetNoPunctuation)
                #print(tweet, sentiment_value, confidence) #print output

                #value manipulations
                if (sentiment_value.lower() == "neg"):
                    num_sentiment=0
                else:
                    num_sentiment=1

                blob_senti = text_blob_sentiment(tweetNoPunctuation)

                if (verified == True):
                    verified_bit = 1
                else:
                    verified_bit = 0

                found = False
                party = ""
                for word in tweetNoPunctuation.split(" "):
                    if word.lower() in party_tags.keys():
                        party_name = party_tags[word.lower()]
                        #print("Found keyword: ", word, " belongs to party: ", party_name)
                        found = True
                        break

                if found:
                    created_at = time.strftime('%Y-%m-%d %H:%M:%S')
                    newID = (int)(all_data['id'])
                    #twitter JSON is being parsed with queries below and using sentiment module, we are assigning confidence values
                    # tweetID, party_name, dateTime, tweet, source,country, country_code, full_name, name, place_type,\
                    #  reply_count, retweet_count, favorite_count, result, confidence,num_sentiment
                    tweet_data = (tweetID ,party_name, created_at, tweet,screen_name,followers_count,friends_count,\
                                  verified_bit, source,country, country_code,full_name,name, place_type,\
                                  reply_count, retweet_count, favorite_count, sentiment_value.lower(), confidence, num_sentiment)

                    data_to_dump = prepare_tweet_json([tweetID ,party_name, created_at, tweet,screen_name,
                                        source,country, country_code,full_name, place_type,\
                                  sentiment_value.lower(), num_sentiment, confidence, followers_count, blob_senti])
                    write_to_es(data_to_dump)
                    print(data_to_dump)

                    # Write a row to the CSV file. I use encode UTF-8
                    # csvWriter.writerow([tweetID ,party_name, created_at, tweet,screen_name,followers_count,friends_count,\
                    #                     verified_bit, source,country, country_code,full_name,name, place_type,\
                    #               reply_count, retweet_count, favorite_count, sentiment_value.lower(), confidence, num_sentiment])

                    # c.execute(add_tweet, tweet_data)
                    # conn.commit()
                # else:
                    # print('unrelated tweet found')
            # else:
                # print('retweeted data found')
        # else:
            # print('no text field found')

        #error handling, since tweepy tends to time out with twitter with out any reason closing the connection from their side
        def on_limit(self, track):
            print('Limit hit! Track = %s' % track)
            return True

        def on_error(self, status):
            print(status)

        def on_disconnect(self, notice):
            print(notice)

        return True