import mysql.connector
import json
import time
import pandas as pd

QUERY_FILTER_BOTS_AND_LOSERS = 'SELECT tweetID, party_name, dateTime, tweet, screen_name, source, country, country_code, full_name, place_type, sentiment, num_sentiment, confidence, followers_count FROM party_sentiment WHERE followers_count >= 1000 AND source NOT LIKE \'%bots%\';'

QUERY_ALL = 'SELECT tweetID, party_name, dateTime, tweet, screen_name, source, country, country_code, full_name, place_type, sentiment, num_sentiment, confidence, followers_count FROM party_sentiment;'

from geopy.geocoders import Nominatim
geolocator = Nominatim(user_agent='crawler_v2')

with open('../dump/location_cache.json', 'r', encoding='utf-8') as location_cache_file:
    location_cache = json.load(location_cache_file)

def shorten_party_name(name):
    return 'BJP' if name == 'Bharatiya Janata Party' else 'INC'

def iso_date(date_time):
    date_time_str = str(date_time)
    return 'T'.join(date_time_str.split(' ')) + '+05:00'

def device_type(source):
    return source.split('>')[1].split('<')[0]

def no_country(country):
    return 'India' if country == '0' else country

def no_country_code(country):
    return 'IN' if country == '0' else country

def city_name(full_name, place_type):
    # parse city from full name; set 0 to New Delhi;
    # also check place_type; if country set to capital city,
    # if admin capital city of the state;
    # all fails then new delhi

    if (full_name == '0'
        or full_name == 'India'
        or place_type != 'city'):
        return 'New Delhi'

    return full_name.split(',')[0]

def geo_location(full_name, retry=5):
    if full_name in location_cache:
        return location_cache[full_name]['address'], location_cache[full_name]['latitude'], location_cache[full_name]['longitude']

    location = None
    if full_name == '0':
        return geo_location('New Delhi, India')
    else:
        try:
            location = geolocator.geocode(full_name)
        except:
            if retry == 0:
                print('service failed for name', full_name)
                return geo_location('New Delhi, India')
            else:
                time.sleep(10)
                print('Retrying...', retry)
                return geo_location(full_name, retry - 1)

    if location is None:
        print('got None for name', full_name)
        return geo_location('New Delhi, India')

    location_cache[full_name] = {
        'address': location.address,
        'latitude': location.latitude,
        'longitude': location.longitude
    }

    return location.address, location.latitude, location.longitude

def sentiment(orig, confidence):
    return 'neu' if confidence < 0.8 else orig

def sentiment_num(senti):
    if senti == 'pos': return 1
    if senti == 'neg': return 0
    return 2

def clean(data):
    addr, latitude, longitude = geo_location(data[8])
    senti = sentiment(data[10], data[12])

    cleansed_data = {
        'tweetID': data[0],
        'party_name': data[1],  # short name(s) ?
        'party_name_short': shorten_party_name(data[1]),  # short name(s) ?
        'date_time': iso_date(data[2]),  # ISO format? timezone? mostly EST
        'tweet': data[3],
        'screen_name': data[4],
        'device_type': device_type(data[5]),  # parse out terms [bot, android, iphone]
        'country': no_country(data[6]), # set 0 to india
        'country_code': no_country_code(data[7]), # set 0 to india
        'city': city_name(data[8], data[9]),
        'place': addr,
        'location': {
            'lat': latitude,
            'lon': longitude
        },
        'sentiment_naivebayes_str': senti,
        'sentiment_naivebayes_num': sentiment_num(senti),
        'confidence': data[12],
        'followers_count': data[13]
    }

    return cleansed_data


def add_blob_senti(df_blob, data):
    try:
        blob_data = df_blob.loc[int(data['tweetID']), :]
        if isinstance(blob_data, pd.DataFrame):
            blob_data = blob_data.iloc[0]
        data['sentiment_textblob_str'] = blob_data['blob_senti']
        data['sentiment_textblob_num'] = sentiment_num(blob_data['blob_senti'])

        # if str(blob_data['blob_senti']) in ['pos', 'neu', 'neg']:
        #     print(type(blob_data))
        #     data['sentiment_textblob_str'] = str(blob_data['blob_senti'])
        #     data['sentiment_textblob_num'] = sentiment_num(str(blob_data['blob_senti']))
        # else:
        #     print(type(blob_data))
        #     print(blob_data.shape[0])
        #     # print(blob_data.iloc[0]['blob_senti'])
        #     data['sentiment_textblob_str'] = data['sentiment_naivebayes_str']
        #     data['sentiment_textblob_num'] = data['sentiment_naivebayes_num']
    except KeyError:
        print('KeyError', data['tweetID'])
        data['sentiment_textblob_str'] = data['sentiment_naivebayes_str']
        data['sentiment_textblob_num'] = data['sentiment_naivebayes_num']

    return data


def loadsql():
    mydb = mysql.connector.connect(
        host='localhost',
        port=13306,
        user='root',
        passwd='tiger',
        database='smdm'
    )

    mycursor = mydb.cursor()
    mycursor.execute(QUERY_ALL)

    # for data in mycursor:
    #     clean(data)

    # return

    df_blob = pd.read_csv('../dump/blob5.csv', delimiter=',', index_col='tweetID', error_bad_lines=False)
    # print(df_blob.loc[1115828065072971777,:])
    # print(df_blob.columns)
    # print(df_blob.loc[df_blob['tweetID'] == 1115828065072971777,:])

    # return

    data_for_dump = []
    for data in mycursor:
        dump = clean(data)
        dump = add_blob_senti(df_blob, dump)
        data_for_dump.append(dump)

    with open('../dump/data_es_3.json', 'w') as data_file:
        json.dump(data_for_dump, data_file)

    with open('../dump/location_cache.json', 'w') as location_cache_file:
        json.dump(location_cache, location_cache_file)

    mycursor.close()
    mydb.close()


if __name__ == '__main__':
    loadsql()