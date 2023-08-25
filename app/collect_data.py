import pandas as pd
import requests as res
import time
import re
from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/")
db = client["project4"]
collection = db["test"]

def list_product_id():
    df = pd.read_csv("./categories_with_relationship.csv")
    list_cates_cl = df["LEAF_CAT_ID"]
    convert_list_cates_cl = list_cates_cl.apply(lambda x: re.sub(r'[^\d.]', '', str(x)))
    list_cates = convert_list_cates_cl.to_list()
    return list_cates

def craw_product(name_file):
    print("RUNNING process {}".format(name_file))
    count = 0
    check = 0
    with open("./{}.txt".format(name_file)) as file:
        for line in file:
            count += 1
            check = 1
            product_id = str(line)
            if check == 1:
                url_res = 'https://tiki.vn/api/v2/products/{}'.format(product_id)
                header_res = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36'}
                sent_request = res.get(url=url_res, headers=header_res)
                if sent_request.status_code == 200:
                    try:
                        data = sent_request.json()
                    except:
                        time.sleep(10)
                        with open("log_error.txt", 'a') as file_er:
                            file_er.write(str(product_id).strip("\n"))
                            file_er.write("\n")
                            file_er.close()
                            continue
                    with open("product_id_running_{}.txt".format(name_file), 'w') as file_er:
                        file_er.write(str(product_id) + " | " + name_file)
                        file_er.close()
                    x = collection.insert_one(data)
                else:
                    with open("log_error.txt", 'a') as file_er:
                        file_er.write(str(product_id).strip("\n") + "--404")
                        file_er.write("\n")
                        file_er.close()
                        continue
                if count % 100 == 0:
                    print('COUNT: {} | {}'.format(count,name_file))


craw_product("product_id_4")



