## These are some simple search queries on the mongoDB database.
## It can be queried in real-time as the streaming twitter API is loading more data.

def get_db(db_name):
    from pymongo import MongoClient
    client = MongoClient('localhost:27017')
    db = client[db_name]
    return db


## Find top locations
def location_pipeline():
    pipeline = [{"$group": {"_id": "$place.country",
                            "count": {"$sum": 1}}},
                {"$sort": {"count": -1}},
                {"$limit": 10}]
    return pipeline

## Find top hashtags. Unwind is used to drill into the hashtags nested array, then group all individual hashtags, and count them.
## Leaving out unwind, you can aggregate the groups of hashtags by each user/tweet as an individual entity to be counted instead.
def hashtag_pipeline():
    pipeline = [{"$unwind": "$entities.hashtags"},
                {"$group": {"_id": "$entities.hashtags",
                            "count": {"$sum": 1}}},
                {"$sort": {"count": -1}},
                {"$limit": 10}]
    return pipeline


## Find tweets from US, define what to return in 'project'
def project_matches_pipeline():
    pipeline = [{"$match": {"place.country": "United States"}},
                {"$project": {"country": "$place.country",
                              "screen_name": "$user.screen_name",
                              "tweet": "$text",
                              "hashtags": "$entities.hashtags"}},
                {"$sort": {"hashtags": -1}},
                {"$limit": 1}]

    return pipeline


  ## Here is where the defined pipelines get sent to process.
def aggregate(db, pipeline):
    result = db.twitter_healthcare.aggregate(pipeline)
    return result




if __name__ == '__main__':
    db = get_db('twitter')
    location = location_pipeline()
    result = aggregate(db, location)
    print "Printing the top 10 locations of tweets:"
    import pprint
    pprint.pprint(result)
    print ""

    hashtag = hashtag_pipeline()
    result = aggregate(db, hashtag)
    print "Printing the top 10 hashtags:"
    import pprint
    pprint.pprint(result)
    print ""

    matches = project_matches_pipeline()
    result = aggregate(db, matches)
    print "Printing the matched records:"
    import pprint
    pprint.pprint(result)
    print ""

    #pprint.pprint(result["result"][0])
    #pprint.pprint(db.twitterDB.find_one())
    #print ""

