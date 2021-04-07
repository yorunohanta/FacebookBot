from random import randint
import feedparser
from flask import Flask, request
from pymessenger.bot import Bot

app = Flask(__name__)
access_token = "EAAD0yY1qYlYBAPDwETtYZCLEI0LvLtcd5uO2n1HdiZCCxZCG8N29CmZAcgZBpxIUC7cblBznc625HPULMOZBOejwtSq501tJukxNZAULvvZCGAR6s2NwsaTOB86ggnAkFBKse5ZC4qfUNNBp1Ck2AYz3k7YRJ7eFRBtGXRGD5CVRJBgZDZD"
verify_token = "TESTOWYTOKENWERYFIKUJACY"
bot = Bot(access_token)
NewsFeedImportant = feedparser.parse("https://news.google.com/news/rss/?hl=pl&amp;gl=PL&amp;ceid=PL%3Apl&amp;oc=11")
NewsFeedWorld = feedparser.parse("https://news.google.com/rss/topics/CAAqJggKIiBDQkFTRWdvSUwyMHZNRGx1YlY4U0FuQnNHZ0pRVENnQVAB?hl=pl&gl=PL&ceid=PL%3Apl&oc=11")
NewsFeedPoland = feedparser.parse("https://news.google.com/rss/topics/CAAqIQgKIhtDQkFTRGdvSUwyMHZNRFZ4YUhjU0FuQnNLQUFQAQ?hl=pl&gl=PL&ceid=PL%3Apl&oc=11")
NewsFeedWroclaw = feedparser.parse("https://news.google.com/rss/topics/CAAqHAgKIhZDQklTQ2pvSWJHOWpZV3hmZGpJb0FBUAE/sections/CAQiTkNCSVNORG9JYkc5allXeGZkakpDRUd4dlkyRnNYM1l5WDNObFkzUnBiMjV5Q2hJSUwyMHZNRGcwTldKNkNnb0lMMjB2TURnME5XSW9BQSowCAAqLAgKIiZDQklTRmpvSWJHOWpZV3hmZGpKNkNnb0lMMjB2TURnME5XSW9BQVABUAE?hl=pl&gl=PL&ceid=PL%3Apl&oc=11")
NewsFeedWarszawa = feedparser.parse("https://news.google.com/rss/topics/CAAqHAgKIhZDQklTQ2pvSWJHOWpZV3hmZGpJb0FBUAE/sections/CAQiTkNCSVNORG9JYkc5allXeGZkakpDRUd4dlkyRnNYM1l5WDNObFkzUnBiMjV5Q2hJSUwyMHZNRGd4YlY5NkNnb0lMMjB2TURneGJWOG9BQSowCAAqLAgKIiZDQklTRmpvSWJHOWpZV3hmZGpKNkNnb0lMMjB2TURneGJWOG9BQVABUAE?hl=pl&gl=PL&ceid=PL%3Apl&oc=11")
NewsFeedSport = feedparser.parse("https://news.google.com/rss/topics/CAAqJggKIiBDQkFTRWdvSUwyMHZNRFp1ZEdvU0FuQnNHZ0pRVENnQVAB?hl=pl&gl=PL&ceid=PL%3Apl&oc=11")
KeyWords = ["Important", "World", "Poland", "Wrocław", "Warszawa", "Sport"]


@app.route('/', methods=['GET', 'POST'])
def receive_message():
    if request.method == "GET": #w pierwszej kolejnosci sprawdzamy czy zapytanie pochodzi z facebook'a
        token_sent = request.args.get("hub.verify_token")
        return verify_fb_token(token_sent)
    else: #jezeli nie funkcja GET to POST, przechodzimy do wysylania wiadomosci
        output = request.get_json() #pobranie wiadomosci wyslanej do bota
        for event in output['entry']:
            messaging = event['messaging']
            for message in messaging:
                if message.get('message'):
                    recipient_id = message['sender']['id'] #messenger ID, abysmy wiedzieli do kogo wyslac wiadomosc
                    if message['message'].get('text'):
                        user_message = message['message'].get('text')
                        if user_message in KeyWords:
                            news_type = NewsTypeSwitch(user_message)
                            response_sent_text = LoadingNews(news_type)
                            send_message(recipient_id, response_sent_text)
                        else:
                            response_sent_text = ("Wpisz: Important, World, Poland, Wrocław, Warszawa lub Sport")
                            send_message(recipient_id, response_sent_text)
                    if message['message'].get('attachments'): #w przypadku wiadomosci nie tekstowej
                        response_sent_nontext = LoadingNews(NewsFeedImportant)
                        send_message(recipient_id, response_sent_nontext)
    return "Message processed"


# WERYFIKACJA TOKENU
# Pobieramy token wyslany przez facebook'a i porownujemy go z tokenem wyslanym przez nas.
# Jezeli sie pokrywaja to zezwalamy na komunikacje, jezeli nie zwracamy blad
def verify_fb_token(token_sent):
    if token_sent == verify_token:
        return request.args.get("hub.challenge")
    return 'Invalid verification token'


def NewsTypeSwitch(argument):
    switcher = {
        "Important": NewsFeedImportant,
        "World": NewsFeedWorld,
        "Poland": NewsFeedPoland,
        "Wrocław": NewsFeedWroclaw,
        "Warszawa": NewsFeedWarszawa,
        "Sport": NewsFeedSport
    }
    return switcher.get(argument)


def LoadingNews(type):
    news_number = randint(0, len(type.entries))
    news = type.entries[news_number]
    response = (news.published + "\n**********\n" + news.title + "\n**********\n" + news.link)
    return response


# FUNKCJA WYSYLAJACA WIADOMOSC
# wysyla do uzytkownika wiadomosc podana w parametrze response
def send_message(recipient_id, response):
    bot.send_text_message(recipient_id, response)
    return "Success"


if __name__ == '__main__':
    app.run()
