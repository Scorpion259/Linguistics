import os
import time
from pymongo import MongoClient
from progress.bar import IncrementalBar


def tomita():
    # Строка подключения к базе данных
    CONNECTION_STRING = "mongodb+srv://ScorpionVSTU:VsTuBoY@scorpioncluster.kb9vl.mongodb.net/ling?retryWrites=true&w=majority"
    # Подключение к нужной коллекции
    client = MongoClient(CONNECTION_STRING)
    db = client.ling
    collection = db.news
    collection_list = list(collection.find())

    sentence_coll = db.sentence
    clear = lambda: os.system('clear')
    # Инициализация прогресс бара
    bar = IncrementalBar('Countdown', max=len(collection_list))
    for news in collection_list:
        # Запуск парсера, если он не был задействован на данную запись
        if "tomita" not in news:
            clear()
            bar.next()
            time.sleep(0.1)
            print('\n')
            # Запись текста новостей во входной файл парсера
            with open("./tomita/input.txt", "w") as file:
                file.write(news['full_text'])

            os.system("./tomita/tomita-parser ./tomita/config.proto")

            # Откытие файла выходных данных для чтения
            with open("./tomita/output.txt", "r") as file:
                file_output = file.read()
                strings = file_output.split('\n')
                # Формирование выборки нужных данных по строкам
                for i in range(len(strings)):
                    if "Politician" in strings[i]:
                        words = strings[i].split("Politician =")
                        if words[1].find('_'):
                            words = words[1].strip().replace("_", " ")
                        # Запись предложения, в котором нашлась нужная личность
                        sentence = strings[i - 3]
                        # Добавление данных в коллекцию
                        sentence_coll.insert_one({'fact': words, 'sentence': sentence})
                    elif "Attraction" in strings[i]:
                        words = strings[i].split("Attraction =")
                        if words[1].find('_'):
                            words = words[1].strip().replace("_", " ")
                        # Запись предложения, в котором нашлось нужное сооружение
                        sentence = strings[i - 3]
                        # Добавление данных в коллекцию
                        sentence_coll.insert_one({'fact': words, 'sentence': sentence})
    bar.finish()


def main():
    try:
        tomita()
    except Exception as exception:
        print(f"Ошибка {exception}")


if __name__ == "__main__":
    main()