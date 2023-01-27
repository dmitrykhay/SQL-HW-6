import os
import json
import sqlalchemy
from sqlalchemy.orm import sessionmaker
from models import create_tables, Publisher, Shop, Book, Stock, Sale

os.environ['DSN'] = 'postgresql://postgres:***@localhost:5432/6HWdb'
DSN = os.environ['DSN']

engine = sqlalchemy.create_engine(DSN)
Session = sessionmaker(bind=engine)
session = Session()

create_tables(engine)

with open("tests_data.json", "r") as f:
    data = json.load(f)

for record in data:
    model = {
        "publisher": Publisher,
        "shop": Shop,
        "book": Book,
        "stock": Stock,
        "sale": Sale
    }[record.get("model")]
    session.add(model(id=record.get('pk'), **record.get('fields')))
session.commit()
session.close()

query = session.query(Stock, Book.title, Shop.name, Sale.price, Sale.date_sale)
query = query.join(Sale, Sale.id_stock == Stock.id)
query = query.join(Shop, Stock.id_shop == Shop.id)
query = query.join(Book, Stock.id_book == Book.id)
query = query.join(Publisher, Book.id_publisher == Publisher.id)
ident = input("Введите название или идентификатор издателя: ")
records = query.filter(Publisher.name == ident or Publisher.id == ident).all()
for rec in records:
    print(f'{rec.title} | {rec.name} | {rec.price} | {rec.date_sale}')