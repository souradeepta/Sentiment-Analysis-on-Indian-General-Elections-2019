
import json

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

def prepare_tweet_json(data):
    """
    tweetID #0,
    party_name #1,
    dateTime #2,
    tweet #3,
    screen_name #4,
    source #5,
    country #6,
    country_code #7,
    full_name #8,
    place_type #9,
    sentiment #10,
    num_sentiment #11,
    confidence #12,
    followers_count, #13
    text_blob_sentiment #14
    """

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
        'followers_count': data[13],
        'sentiment_textblob_str': data[14],
        'sentiment_textblob_num': sentiment_num(data[14])
    }

    return cleansed_data