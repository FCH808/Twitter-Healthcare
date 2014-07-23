import tweepy
import pymongo
import pprint
import json
import csv



# Connection to Mongo DB
def get_db(db_name):
    from pymongo import MongoClient
    client = MongoClient('localhost:27017')
    db = client[db_name]
    return db



consumer_key = "my_consumer_key"
consumer_secret = "my_consumer_secret"
access_token = "my_access_token"
access_token_secret = "my_access_token_secret"

class MongoListener(tweepy.StreamListener):
    ''' Handles data received from the stream. '''

    def __init__(self):

        self.counter = 0 # Set a counter for counting the tweets loaded this session.
        print "Counter:", self.counter

    def on_data(self, data):
        #ustr_to_load = unicode(data, 'utf-8')
        decoded = json.loads(data)

        ## If tweets is deleted, ignore the call and continue to next tweet.
        if 'delete' in decoded.keys():
            return True

        ## If call has no user info for some reason, ignore it and continue. Encountered this error before, not sure why.
        if 'user' not in decoded.keys():
            return True

        print '@%s: %s' % (decoded['user']['screen_name'], decoded['text'])
        if decoded['place'] is not None:
            country = decoded['place']['country']
            full_name = decoded['place']['full_name']
            print 'Country: %s,' % country
            print 'Full Name: %s' % full_name
        else:
            country = ""
            full_name = ""
        if decoded['user']['location'] != "":
            print 'Location: %s' % decoded['user']['location']
        if len(decoded['entities']['hashtags']) > 0:
            hashes = []
            for hash in decoded['entities']['hashtags']:
                hashes.append(hash['text'])
                print 'Hashtags: %s' % hash['text']
        else:
            hashes = []


        ## Data structure for tweets to pass into
        my_data = {
            'id': decoded['id'],
            'text': decoded['text'],
            'place': {'country': country,
                      'full_name': full_name},
            'user': {'screen_name': decoded['user']['screen_name'],
                     'location': decoded['user']['location']},
            'entities': {'hashtags': hashes}
        }

        # Print out the full record that is being added in its json format.
        # pprint.pprint(my_data)

        # Load the data with the above file structure into the twitter_healthcare collection in the twitter database in MongoDB.
        db.twitter_healthcare.insert(my_data)

        self.counter += 1 # Add 1 to counter every time tweet is added.
        print "%d added" % self.counter
        if self.counter >= 20000: # Set a max amount to add this session. May be useful to automatically shard data into smaller datasets.
            stream.disconnect()

        print ""

    def on_error(self, status_code):
        print('Returned error status code: ' + str(status_code))
        return True  # To continue listening

    def on_timeout(self):
        print('Timeout...')
        return True  # To continue listening

    # def on_status(self, status):
    #     #
    #     # Prints the text of the tweet
    #     print 'Tweet text: ' + status.text
    #
    #     # There are many options in the status object,
    #     # hashtags can be very easily accessed.
    #     # for hashtag in status.entries['hashtags']:
    #     #     print hashtag['text']
    #     pprint.pprint(status.user.screen_name)
    #     print status.user.location
    #     try:
    #         print status.place.full_name
    #         print status.place.bounding_box
    #     except:
    #         pass
    #     print ""
    #     return True

    ## Two streams of healthcare hashtags borrowed from: https://github.com/pratik008/HealthCare_Twitter_Analysis/tree/master/Archive%201/python_stream_scripts

def make_tracklists(csv_file):

        tracklist = []
        with open(csv_file, 'rb') as d:
            reader = csv.reader(d)
            for row in reader:
                if row[0] == "Raw Data":
                    continue
                tracklist.append(row[0].replace('#', '').strip())
        return tracklist

def split_list(a_list):
    half = len(a_list)/2
    return a_list[:half], a_list[half:]

if __name__ == '__main__':

    db = get_db('twitter')

    listener = MongoListener()
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)

    stream = tweepy.Stream(auth, listener)

    # Read in first column of DiseaseHashtags.csv
    track = make_tracklists('DiseaseHashtags.csv')

    # Original is too large. Split tracklist in half.
    tracklists  = split_list(track)


    for track in tracklists:
        stream.filter(track=track)


# Alternative loop approach.
# # Define my mongoDB database
# db = conn.twitter_results
# # Define my collection where I'll insert my search
# posts = db.posts
#
# # loop through search and insert dictionary into mongoDB
# for tweet in search:
#     # Empty dictionary for storing tweet related data
#     data ={}
#     data['author'] = tweet.author
#     data['coordinates'] = tweet.coordinates
#     data['created_at'] = tweet.created_at
#     data['entities'] = tweet.entities
#     data['in_reply_to_screen_name'] = tweet.in_reply_to_screen_name
#     data['geo'] = tweet.geo
#     data['id'] = tweet.id
#     data['lang'] = tweet.lang
#     data['place'] = tweet.place
#     data['text'] = tweet.text
#     data['user'] = tweet.user
#     data['source'] = tweet.source
#     data['source_url'] = tweet.source_url
#     data['favorite'] = tweet.favorite
#     # Insert process
#     posts.insert(data)
#
# posts.find_one()
