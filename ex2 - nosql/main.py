from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, PyMongoError


def initialize_db():
    client = MongoClient("mongodb://localhost:27017/")
    db = client['catdb']
    cats_collection = db['cats']

    cats_collection.delete_many({})

    cats = [
        {"name": "barsik", "age": 3, "features": ["ходить в капці", "дає себе гладити", "рудий"]},
        {"name": "murzik", "age": 5, "features": ["спить усюди", "любить іграшки", "чорний"]},
        {"name": "pushok", "age": 1, "features": ["дуже малий", "пухнастий", "білий"]}
    ]
    cats_collection.insert_many(cats)


def get_database():
    try:
        client = MongoClient("mongodb://localhost:27017/")
        return client['catdb']
    except ConnectionFailure:
        print("Помилка підключення до MongoDB.")
        return None


def read_all_cats():
    db = get_database()
    if db is not None:
        try:
            for cat in db.cats.find():
                print(cat)
        except PyMongoError as e:
            print(f"Помилка читання з бази даних: {e}")


def read_cat_by_name(name):
    db = get_database()
    if db is not None:
        try:
            cat = db.cats.find_one({"name": name})
            if cat:
                print(cat)
            else:
                print("Кіт з таким іменем не знайдений.")
        except PyMongoError as e:
            print(f"Помилка читання з бази даних: {e}")


def update_cat_age(name, age):
    db = get_database()
    if db is not None:
        try:
            result = db.cats.update_one({"name": name}, {"$set": {"age": age}})
            if result.modified_count:
                print("Вік кота успішно оновлено.")
            else:
                print("Не вдалося оновити вік кота.")
        except PyMongoError as e:
            print(f"Помилка оновлення даних: {e}")


def add_cat_feature(name, feature):
    db = get_database()
    if db is not None:
        try:
            result = db.cats.update_one({"name": name}, {"$push": {"features": feature}})
            if result.modified_count:
                print("Характеристика кота успішно додана.")
            else:
                print("Не вдалося додати характеристику кота.")
        except PyMongoError as e:
            print(f"Помилка оновлення даних: {e}")


def delete_cat_by_name(name):
    db = get_database()
    if db is not None:
        try:
            result = db.cats.delete_one({"name": name})
            if result.deleted_count:
                print("Кіт успішно видалений.")
            else:
                print("Кота з таким іменем не знайдено.")
        except PyMongoError as e:
            print(f"Помилка видалення з бази даних: {e}")


def delete_all_cats():
    db = get_database()
    if db is not None:
        try:
            result = db.cats.delete_many({})
            print(f"Видалено {result.deleted_count} котів.")
        except PyMongoError as e:
            print(f"Помилка видалення з бази даних: {e}")


if __name__ == '__main__':
    initialize_db()
    read_all_cats()
    read_cat_by_name("barsik")
    update_cat_age("barsik", 4)
    add_cat_feature("barsik", "любить сон")
    delete_cat_by_name("barsik")
    delete_all_cats()
