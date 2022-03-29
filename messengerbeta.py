from flask import Flask, render_template, request
import datetime
import json

app=Flask(__name__)

DB_FILE="./data/db.json"  #Путь к файлу
db = open(DB_FILE, "rb") #Открываем файл
data = json.load(db) #Загрузить все данные
messages = data["messages"] #Из полученных данных берем поле messages

#Функции для сохранения
def save_messages_to_file():
    db = open(DB_FILE, "w") #Открываем для записи
    data= {
        "messages": messages

    }
    json.dump(data, db)

def add_message(text, sender):  # Объявим функцию, которая добавит сообщение в список
    now = datetime.datetime.now() #Текущее время и дату
    new_message = {
        "text": text,
        "sender": sender,
        "time": now.strftime("%H:%M") #Текущий час минуты
    }
    messages.append(new_message)  # Добавляем новое сообщение в список
    save_messages_to_file()

def check_numbers_of_messages():
    if len(messages)>26:
        del messages[0]
    else:
        return

def print_message(message):  # Объявляем функцию, которая будет печатать одно сообщение
    print(f"[{message['sender']}]: {message['text']} / {message['time']} ")

#Главная страница
@app.route("/")
def index_page():
    return"Здравствуйте. Вас приветствует СкиллЧат2022"

#Показать все сообщения в  формате JSON
@app.route("/get_messages")
def get_messages():
    return{"messages": messages}

#Показать форму чата
@app.route("/form")
def form():
    return render_template("form.html")

@app.route("/send_message")
def send_message():
    check_numbers_of_messages()
    name = request.args["name"]
    text = request.args["text"]
    if len(name)<3 or len(name)>100:
        print("Длина имени пользователя недопустима")
    elif len(text)<1 or len(text)>3000:
        print("Длина текста недопустима")
    else:
        add_message(text, name)

    return "OK"

app.run(host="0.0.0.0", port=80)   #Запускаем веб-приложение

#  ПЛАН
#  1. Создали внутреннюю возможность хранить сообщения, добавлять новые и читать чат
#  2. Подключить визуальный интерфейс к этим внутренним возможностями
#     - Превратить наш код в веб-сервер. Flask
#     - Создать интерфейс и подключить его к веб-серверу
