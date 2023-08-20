from connect_mongodb import collection,client
from bs4 import BeautifulSoup
import re
import csv

def find_origin():
    pipe_line = [
        {
            "$match": {
                "specifications.name": "Content",
            },
        },
        {
            "$match": {
                "specifications.attributes.code": "origin",
            },
        },
        {
            "$project":
                {
                    "specifications": 1,
                },
        },
    ]
    result = collection.aggregate(pipeline=pipe_line)
    data = {}
    for i in result:
        origin = None
        for j in i['specifications']:
            if j.get('name') == 'Content':
                for x in j['attributes']:
                    if x.get('code') == 'origin':
                        origin = x.get('value')
        if origin:
            if data.get(origin):
                data[origin] += 1
            else:
                data[origin] = 1
    clear_data = {}
    for k, v in data.items():
        if "/" not in k and "," not in k:
            clear_data[k] = v
    for k, v in data.items():
        if "/" in k or "," in k:
            for kk, vv in clear_data.items():
                if kk in k:
                    clear_data[kk] += data[k]

    sorted_data = dict(sorted(clear_data.items(), key=lambda item: item[1], reverse=True))
    top_20 = {k: sorted_data[k] for k in list(sorted_data)[:20]}
    print(top_20)

def top_10_sold_out():
    pipe_line = [
        {
            "$sort": {
                "all_time_quantity_sold": -1,
            },
        },
        {
            "$limit": 10,
        },
    ]

    result = collection.aggregate(pipeline=pipe_line)
    print("TOP 10 PRODUCT QUANTITY SOLD:")
    print("-----------------------------")
    for k, i in enumerate(result):
        print("TOP {}: {}".format(k+1, i['name']))
    client.close()

def top_10_rating():
    pipe_line = [
        {
            "$sort":
                {
                    "rating_average": -1,
                    "price": 1,
                },
        },
        {
            "$limit": 10,
        },
    ]
    result = collection.aggregate(pipeline=pipe_line)
    print("TOP 10 PRODUCT HAVE HIGHEST RATING AND LOWEST PRICE:")
    print("----------------------------------------------------")
    for k, i in enumerate(result):
        print("TOP {}: {}".format(k+1, i['name']))
    client.close()

def count_description():
    result = collection.find({
        "description": {
            "$regex": "thành phần",
            "$options": "i"
        }
    })
    # result = collection.find({"id": 225067228})
    result = list(result)
    check = 0
    for k, i in enumerate(result):
        print(len(result)-check)
        check += 1
        description = i['description']
        soup = BeautifulSoup(description, 'html.parser')
        tags_with_content = soup.find_all(lambda tag: 'thành phần' in tag.text.lower())
        data_tp = []
        for j in tags_with_content:
            if len(j.text) < 14:
                data = j.find_next().text
            else:
                data = j.text
            if len(data) > 14:
                data_tp.append(str(data).replace("\n", " "))
        if len(data_tp) == 1:
            with open("product_tp_fail.txt", "a") as file:
                file.write(str(i['id']).strip("\n"))
                file.write("\n")
        else:
            string_data = ''
            for z in data_tp:
                string_data = string_data + (z) + ", "
            string_data[:-2]
            final_data = [i['id'],string_data]
            with open('data_tp.csv', 'a', encoding='utf-8', newline='') as csvfile:
                csvwriter = csv.writer(csvfile)
                csvwriter.writerow(final_data)
        # print(data_tp)
        # print(final_data)
        # if check == 5:
        #     break

if __name__ == "__main__":
    # top_10_sold_out()
    # top_10_rating()
    # find_origin()
    count_description()


