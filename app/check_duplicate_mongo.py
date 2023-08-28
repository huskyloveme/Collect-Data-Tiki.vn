from connect_mongodb import collection,client

pipeline = [
    {
        "$group": {
            "_id": "$id",
            "count": {"$sum": 1}
        }
    },
    {
        "$match": {
            "count": {"$gte": 2}
        }
    }
]

result = collection.aggregate(pipeline=pipeline)

distinct_ids = [item["_id"] for item in result]
checkk = len(distinct_ids)

for _id in distinct_ids:
    print(checkk)
    documents_to_delete = collection.find({"id": _id})
    check = 0
    for document in list(documents_to_delete):
        if check > 0:
            collection.delete_one({"_id": document["_id"]})
        else:
            with open("log_id.txt", "a") as file:
                file.write(str(document["id"]).strip("\n"))
                file.write("\n")
        check += 1
    checkk -= 1



client.close()