from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import declarative_base
from bs4 import BeautifulSoup
from connect_mongodb import collection,client

def remove_html_tags(html_string):
    soup = BeautifulSoup(html_string, "html.parser")
    plain_text = soup.get_text()
    return plain_text

engine = create_engine("mysql+pymysql://root:@localhost:3306/data_tiki")

Base = declarative_base()

class Products(Base):
    __tablename__ = 'data_products'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100))
    short_des = Column(String(1000))
    des = Column(String(5000))
    url = Column(String(200))
    rating = Column(String(10))
    sold_out = Column(Integer)
    price = Column(Integer)
    cate_id = Column(Integer)
    day_ago_created = Column(String(20))

    def __init__(self, name, short_des, des, url, rating, sold_out, price, cate_id, day_ago_created):
        self.name = name
        self.short_des = short_des
        self.des = des
        self.url = url
        self.rating = rating
        self.sold_out = sold_out
        self.price = price
        self.cate_id = cate_id
        self.day_ago_created = day_ago_created

# Create table
# Base.metadata.create_all(engine)

# Create Session
Session = sessionmaker(bind=engine)
session = Session()

# Add data
tmp = 20000
count_mor = 0

while True:
    result = collection.find({}).skip(tmp).limit(10000)
    stop_w = 0
    for k, i in enumerate(list(result)):
        count_mor += 1
        stop_w += k
        print(count_mor)
        try:
            pro_name = i['name'] if i.get('name') else None
            pro_short_des = i['short_description'] if i.get('short_description') else None
            pro_des = remove_html_tags(i['description']) if i.get('description') else None
            pro_url = i['short_url'] if i.get('short_url') else None
            pro_rating = i['rating_average'] if i.get('rating_average') else None
            pro_sold_out = i['all_time_quantity_sold'] if i.get('all_time_quantity_sold') else None
            pro_price = i['price'] if i.get('price') else None
            pro_cate_id = i['categories']['id'] if i.get('categories') else None
            pro_day_ago_created = i['day_ago_created'] if i.get('day_ago_created') else None

            new_product = Products(name=pro_name, short_des=pro_short_des, des=pro_des, url=pro_url,
                                   rating=pro_rating,
                                   sold_out=pro_sold_out, price=pro_price, cate_id=pro_cate_id,
                                   day_ago_created=pro_day_ago_created)


            session.add(new_product)
            session.commit()

        except Exception as e:
            print(e)
            with open("id_false_write_file.txt", 'a') as file:
                file.write(str(i['id']))
                file.write("\n")
            continue
    if stop_w == 0:
        break
    tmp += 10000
    # break


session.close()



