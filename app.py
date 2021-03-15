from random import randint
import feedparser
from flask import Flask, request
from pymessenger.bot import Bot

app = Flask(__name__)
access_token = "EAAD0yY1qYlYBAPDwETtYZCLEI0LvLtcd5uO2n1HdiZCCxZCG8N29CmZAcgZBpxIUC7cblBznc625HPULMOZBOejwtSq501tJukxNZAULvvZCGAR6s2NwsaTOB86ggnAkFBKse5ZC4qfUNNBp1Ck2AYz3k7YRJ7eFRBtGXRGD5CVRJBgZDZD"
verify_token = "TESTOWYTOKENWERYFIKUJACY"
bot = Bot(access_token)
NewsFeed = feedparser.parse("https://news.google.com/news/rss/?hl=pl&amp;ned=PL&amp;gl=PL")


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
                        response_sent_text = get_message()
                        send_message(recipient_id, response_sent_text)
                    if message['message'].get('attachments'): #w przypadku wiadomosci nie tekstowej
                        response_sent_nontext = get_message()
                        send_message(recipient_id, response_sent_nontext)
    return "Message processed"


# WERYFIKACJA TOKENU
# Pobieramy token wyslany przez facebook'a i porownujemy go z tokenem wyslanym przez nas.
# Jezeli sie pokrywaja to zezwalamy na komunikacje, jezeli nie zwracamy blad
def verify_fb_token(token_sent):
    if token_sent == verify_token:
        return request.args.get("hub.challenge")
    return 'Invalid verification token'


# WYBIERANIE RANDOMOWEJ WIADOMOSCI WYSYLANEJ DO UZYTKOWNIKA
def get_message():
    news_number = randint(0, len(NewsFeed.entries))
    news = NewsFeed.entries[news_number]
    sample_response = (news.published + "\n**********\n" + news.title + "\n**********\n" + news.link)
    return sample_response


# FUNKCJA WYSYLAJACA WIADOMOSC
# wysyla do uzytkownika wiadomosc podana w parametrze response
def send_message(recipient_id, response):
    bot.send_text_message(recipient_id, response)
    return "Success"


if __name__ == '__main__':
    app.run()
    