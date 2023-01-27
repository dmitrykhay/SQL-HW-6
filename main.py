import sqlalchemy
import os
from sqlalchemy.orm import sessionmaker
from models import create_tables, Publisher, Shop, Book, Stock, Sale

os.environ['DSN'] = 'postgresql://postgres:***@localhost:5432/6HWdb'
DSN = os.environ['DSN']

engine = sqlalchemy.create_engine(DSN)
Session = sessionmaker(bind=engine)

if __name__ == '__main__':
    session = Session()

    create_tables(engine)

    publisher_1 = Publisher(name="OReilly")
    publisher_2 = Publisher(name="Pearson")
    publisher_3 = Publisher(name="Microsoft Press")
    publisher_4 = Publisher(name="No starch press")
    book_1 = Book(title="Programming Python, 4th Edition", id_publisher="1")
    book_2 = Book(title="Learning Python, 4th Edition", id_publisher="1")
    book_3 = Book(title="Natural Language Processing with Python", id_publisher="1")
    book_4 = Book(title="Hacking: The Art of Exploitation", id_publisher="4")
    book_5 = Book(title="Modern Operating Systems", id_publisher="2")
    book_6 = Book(title="Code Complete: Second Edition", id_publisher="3")
    shop_1 = Shop(name="Labirint")
    shop_2 = Shop(name="OZON")
    shop_3 = Shop(name="Amazon")
    stock_1 = Stock(id_shop="1", id_book="1", count="34")
    stock_2 = Stock(id_shop="1", id_book="2", count="30")
    stock_3 = Stock(id_shop="1", id_book="3", count="0")
    stock_4 = Stock(id_shop="2", id_book="5", count="40")
    stock_5 = Stock(id_shop="2", id_book="6", count="50")
    stock_6 = Stock(id_shop="3", id_book="4", count="10")
    stock_7 = Stock(id_shop="3", id_book="6", count="10")
    stock_8 = Stock(id_shop="2", id_book="1", count="10")
    stock_9 = Stock(id_shop="3", id_book="1", count="10")
    sale_1 = Sale(price="50.05", date_sale="2018-10-25T09:45:24.552Z", count="16", id_stock="1")
    sale_2 = Sale(price="50.05", date_sale="2018-10-25T09:51:04.113Z", count="10", id_stock="3")
    sale_3 = Sale(price="10.50", date_sale="2018-10-25T09:52:22.194Z", count="9", id_stock="6")
    sale_4 = Sale(price="16.00", date_sale="2018-10-25T10:59:56.230Z", count="5", id_stock="5")
    sale_5 = Sale(price="16.00", date_sale="2018-10-25T10:59:56.230Z", count="5", id_stock="9")
    sale_6 = Sale(price="16.00", date_sale="2018-10-25T10:59:56.230Z", count="1", id_stock="4")

    session.add_all([publisher_1, publisher_2, publisher_3, publisher_4])
    session.add_all([book_1, book_2, book_3, book_4, book_5, book_6])
    session.add_all([shop_1, shop_2, shop_3])
    session.add_all([stock_1, stock_2, stock_3, stock_4, stock_5, stock_6, stock_7, stock_8, stock_9])
    session.add_all([sale_1, sale_2, sale_3, sale_4, sale_5, sale_6])
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
