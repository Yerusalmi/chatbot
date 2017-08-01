"""
This is the template server side for ChatBot
"""
from bottle import route, run, template, static_file, request
import random
import json

topics = ["sports","weather","news","tech",]

sports_topics = ["football", "basketball", "tennis", "golf"]
weather_cities = ["istanbul","tel aviv","vienna"]
news_countries = ["Turkey","Israel","Austria"]
tech_topics = ["computers","mobile","high tech"]
user_messages = []
conversation = {'level':1} # Conversation Level
chatty = {}


@route('/', method='GET')
def index():
    return template("chatbot.html")


@route("/chat", method='POST')
# def check_word(user_input_list,the_array):
#     for word in the_array:
#         if word in user_input_list:
#             return True
#     return False

def chat2():
    exists = True
    topic = ''
    user_message = request.POST.get('msg').lower()
    user_messages.append ( user_message )

    if user_message == "reset":
        conversation["level"] = 1
        return json.dumps({"animation": "laughing", "msg": "Okay, lets start over. Pick a topic please. Ex: " + random.choice(topics)})

    if conversation["level"] == 1:
        user_words = user_message.split()
        for word in user_words:
            if word in topics:
                topic = word
                chatty['subject'] = word
                exists = True
            else:
                exists = False
        if topic == "weather":
            conversation['level'] += 1
            return json.dumps({"animation": "waiting", "msg": "cool, now pick a city. Ex: "+ random.choice(weather_cities)})
        elif topic == "sports":
            conversation['level'] += 1
            return json.dumps({"animation": "waiting", "msg": "cool, now pick a branch. Ex: "+ random.choice(sports_topics)})
        elif topic == "news":
            conversation['level'] += 1
            return json.dumps({"animation": "waiting", "msg": "cool, now pick a country. Ex: "+ random.choice(news_countries)})
        elif topic == "tech":
            conversation['level'] += 1
            return json.dumps({"animation": "waiting", "msg": "cool, now pick a topic. Ex: "+ random.choice(tech_topics)})
        if exists is False:
            return json.dumps({"animation":"inlove", "msg":"oh shit, try again"})

    if conversation["level"] == 2:
        user_words = user_message.split()
        if "tel aviv" in user_message:
            print "yes"
        print user_words
        print conversation['level']
        print chatty['subject']
        if chatty['subject'] == "weather":
            for city in user_words:
                if city in weather_cities:
                    topic = city
                    exists = True
                    print topic
                else:
                    exists = False
            if topic == "istanbul":
                conversation["level"] = 1
                return json.dumps({"animation": "inlove", "msg": "It's super cloudy in istanbul"})
            elif "tel aviv" in user_message:
                conversation["level"] = 1
                return json.dumps({"animation": "inlove", "msg": "It's very sunny and HOT in Tel Aviv"})
            elif topic == "vienna":
                conversation["level"] = 1
                return json.dumps({"animation": "inlove", "msg": "It's cold but shinny in Vienna"})
            if exists is False:
                return json.dumps({"animation": "inlove", "msg": "oh shit, try again"})


@route("/test", method='POST')
def chat():
    user_message = request.POST.get('msg')
    user_messages.append(user_message)
    return json.dumps({"animation": "inlove", "msg": user_message})


@route('/chat', method='GET')
def get_the_messages():
    return json.dumps(user_messages)


@route('/js/<filename:re:.*\.js>', method='GET')
def javascripts(filename):
    return static_file(filename, root='js')


@route('/css/<filename:re:.*\.css>', method='GET')
def stylesheets(filename):
    return static_file(filename, root='css')


@route('/images/<filename:re:.*\.(jpg|png|gif|ico)>', method='GET')
def images(filename):
    return static_file(filename, root='images')


def main():
    run(host='localhost', port=7000)

if __name__ == '__main__':
    main()
