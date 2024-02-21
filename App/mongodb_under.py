from pymongo import MongoClient

db_name="sample_mflix"
CONNECTION_STRING = "mongodb+srv://tarkesh2512:6kdCtGM5QP8dwWtK@cluster0.grapx5f.mongodb.net/?retryWrites=true&w=majority"
client = MongoClient(CONNECTION_STRING)
db=client[db_name]
collections = db.list_collection_names()   #list all collections in db
print(f"All collections in db: {db_name} are: \n {collections}")
# Define the map function
map_function = '''
function() {
    // Extract the year from the release_date field and emit it as the key
    var year = this.release_date.getFullYear();
    emit(year, 1);
}
'''

# Define the reduce function
reduce_function = '''
function(key, values) {
    // Sum the values for each key (year)
    return Array.sum(values);
}
'''

# result = db.command('mapReduce', 'movies', map=map_function, reduce=reduce_function, out=0'movies_per_year')

# Print the result
# for doc in db['movies_per_year'].find():
#     print(doc)

# # Perform the map-reduce operation
# result_collection = db.movies.map_reduce(map_function, reduce_function, "movies_per_year")
#
# # Print the result
# for doc in result_collection.find():
#     print(doc)

# comments = db["comments"]   #use specific collection
# movies = db["movies"]
#
# pipeline = [
#     {"$group": {"_id": "$year", "no_of_releases": {"$sum": 1}}},
#     {"$project": {"year": "$_id", "no_of_releases": 1, "_id": 1}},
#     {"$sort":{"_id":1}}
# ]
# result=list(movies.aggregate(pipeline))
# for item in result:
#     print(item)

# pipeline=[
#     {
#         "$group":{
#             "_id":{"$year": "$released"},
#             "count":{"$sum":1}
#         }
#     },
#     {
#         "$sort":{"_id":1}
#     }
# ]

# for x in movies.find({"imdb.rating":{"$in":[3,2]}},{"_id":0,"imdb": 1}):
#     print(f"use of find between {x}")
# pipeline=[
#     {
#         "$group":{
#             "_id":{"$year": "$released"},
#             "count":{"$sum":1}
#         }
#     },
#     {
#         "$sort":{"_id":1}
#     }
# ]

# db.movies.find({"imdb.rating":{"$in":[3,2]}})
# db.movies.find({"imdb.rating":{"$gt":1,"$lt":3}})
# print("is field exists ",db.movies.find_one({"myname":{"$exists":True}}))
# pipeline = [
#     {"$group": {"_id": "$property_type", "no_of_property": {"$sum": 1}}},
#     {"$project": {"property_type": "$_id", "no_of_property": 1, "_id": 0}}
# ]
#
# pipeline=[
#     {
#         "$lookup" : {
#         "from" : "movies",
#         "localField" : "movie_id",
#         "foreignField" : "_id",
#         "as" : "moviedetails"
#         },
#     },
#     {
#     "$limit" : 1
#     }
# ]
#
# result=list(comments.aggregate(pipeline))
# for item in result:
#     print(item)
#

# myquery = comments.find().limit(5)    #first 5 docs
# for x in myquery:
#     print(x)
# print("\n")
# alldocs=comments.find()
# lalldocs=list(alldocs)
# comments_df=pd.DataFrame(lalldocs)
# print("comments_df",comments_df)
#
# myquery = movies.find().limit(5)    #first 5 docs
# for x in myquery:
#     print(x)
# malldocs=movies.find()
# mlalldocs=list(malldocs)
# movies_df=pd.DataFrame(mlalldocs)
# print("movies_df",movies_df)


# pipeline = [
#     {"$group": {"_id": "$property_type", "no_of_property": {"$sum": 1}}},
#     {"$project": {"property_type": "$_id", "no_of_property": 1, "_id": 0}}
# ]


# alldocs=mycol.find()
# lalldocs=list(alldocs)
# df=pd.DataFrame(lalldocs)
# df.to_excel(f"datfrommongodb.xlsx",index=False)
# print(df)
# print("no of keys in one doc",len(mycol.find_one({"_id":"9993190"}).keys()))
# total_documents = mycol.count_documents({})    #to get no of docs in specifed collection
# print("no of docs beofre delete",total_documents)
# print(mycol.find_one(sort=[('_id',-1)]))  #sort doc column by col name i.e "_id" & -1 desc order
# mycol.delete_one({"_id":ObjectId("65c0e0e62ef1db45c6b584e8")})      #to delete perticular doc from collection
# total_documents = mycol.count_documents({})    #to get no of docs in specifed collection
# print("no of docs after delete",total_documents)
# print(mycol.find_one())  #single doc i.e first one
# myquery={"_id":'10006546' }
# myquery={"host_name":{"$gt":"R"}}
# myquery = { "name":{"$regex" : "^R"} }
# myquery = mycol.find().sort("name",1)
# for x in mycol.find(myquery,{ "_id": 0,"name":1 }):  #traversing over docs in col
#   print(x)

# pipeline=[
#     {"$project":{"name":1}},
#     {"$limit":5}
# ]
#
# result=list(mycol.aggregate(pipeline))
# for item in result:
#     print(item)
#
# pipeline=[
#     {"$match":{"property_type":"House"}},
#     {"$count":"totalhouses"}
# ]
#
# result=list(mycol.aggregate(pipeline))
# for item in result:
#     print(item)
#
# pipeline=[
#     {
#         "$lookup": {"from": "listingsAndReviews","localField": "_id","foreignField": "host_id",
#                     "as": "host_details"},
#
#     },
#     {"$project":{"host":1}},
#   {
#     "$limit": 5
#   }
# ]
#
# result=list(mycol.aggregate(pipeline))
# for item in result:
#     print("lookup",item)
#

# pipeline=[
#     {"$group" : { "_id" : "$property_type"}},
#     {"$count":"property_type_wise_count"}
# ]

# fastapi
# mongodb
# automation