Twitter-Healthcare
==================

### tweepy_healthcare_finder.py 

1.) Streams twitter data 
2.) Filters the data based on the keywords in medical_hashtags.json
3.) Organizes the twitter data into the following file structure:
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
        
4.) If a mongod.exe mongoDB instance is open
    streams the each tweet record into a collection called 'twitter_healthcare' in a database called 'twitter' 

### mongo_search_healthcare.py

Some basic pymongo search queries on the data being streamed into the twitter.twitter_healthcare collection.

These queries can be dynamically run on the database collection as it is being streamed in.

1.) location_pipeline: creates a query to find the top locations of tweets in the dataset.
2.) hashtag_pipeline: creates a query to find the top hashtags in the dataset.
3.) project_matches_pipeline: creates a query to return the tweets from a specific location.

4.) aggregate: runs the created queries.

### medical_hashtags.json

json file containing the sets of keywords to filter tweets by

### fields.txt

List of field names to export mongo collection to csv.

### mongoexport create csv.txt

Command line argument to export mongo collection as csv with data/fields names specified in fields.txt
