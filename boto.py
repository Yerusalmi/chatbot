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
bad_words = ['kkk','fuck', 'shit', 'bitch', 'asshole', 'douchebag', 'fag', 'dick','idiot','fucker','piece of shit']
user_messages = []
conversation = {'level':0} # Conversation Level
chatty = {}
user_message = ""

@route('/', method='GET')
def index():
    return template("chatbot.html")


@route("/chat", method='POST')
def chat2():
    exists = True
    topic = ''
    user_message = request.POST.get('msg').lower().replace('?', ' ?')
    print user_message


    user_words = user_message.split()
    user_messages.append ( user_message )
    print user_words
    if "?" and "talk" and "about" in user_message or "help" in user_message:
        if "?" and "talk" and "about" in user_message:
            return json.dumps ( {"animation": "confused", "msg": "Well, I can talk about: " + str(topics).strip('[]')})
        if "help" in user_message:
            return json.dumps ( {"animation": "confused", "msg": "Alright, we could talk about: " + str(topics).strip('[]')})

    if check_word(user_words,bad_words):
        return json.dumps ( {"animation": "laughing", "msg": "Language Man!"} )

    if user_message == "reset":
        conversation["level"] = 0
        return json.dumps({"animation": "laughing", "msg": "Okay, lets start over. Pick a topic please. Ex: " + random.choice(topics)})

    if conversation["level"] == 0:
        conversation['level'] += 1
        return json.dumps({"animation":"confused", "msg": "Oh hello " + user_message + "! I'm boto! What would you like to talk about?"})

    if "my name" and "is" in user_words:
        conversation['level'] = 1
        return json.dumps({"animation":"laughing","msg":"Okey, so your name is " + user_message + ", I got it. What would you like to talk about?"})

    if word_checker["answer"] is "waiting":
        if "yes" in user_words:
            word_checker["answer"] = ""
            conversation["level"] = 1
            topic = word_checker["new_subject"]
            chatty['subject'] = word_checker["new_subject"]
            chat2 ()
        else:
            word_checker["answer"] = ""
            conversation["level"] = 1
            word_checker['skip'] = "yes"
            return json.dumps ( {"animation": "laughing","msg": "Okay, lets start over. Pick a topic please. Ex: " + random.choice ( topics )} )

    if conversation["level"] == 1:

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
            return json.dumps({"animation":"inlove", "msg": "Truth be told, I would love to talk about it but I haven't learned anything about " + user_message +". Give me something I know like: "+ random.choice(tech_topics)})



    if check_word(user_words,topics):
        conversation["level"] =1
        return json.dumps({"animation":"laughing","msg":"Do you want to talk about " + word_checker["new_subject"] + "?"})



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
                return json.dumps({"animation": "inlove", "msg": "It's super cloudy in istanbul! What else would you like to talk about?"})
            elif "tel aviv" in user_message:
                conversation["level"] = 1
                return json.dumps({"animation": "inlove", "msg": "It's very sunny and HOT in Tel Aviv! What else would you like to talk about?"})
            elif topic == "vienna":
                conversation["level"] = 1
                return json.dumps({"animation": "inlove", "msg": "It's cold but shinny in Vienna! What else would you like to talk about?"})
            if exists is False:
                return json.dumps({"animation": "inlove", "msg": "oh no!, try again"})

word_checker = {"new_subject":"","answer":"","skip":""}


def check_word(user_input_list, the_array):
    for word in the_array:
        if word in user_input_list:
            word_checker["new_subject"] = word
            word_checker["answer"] = "waiting"
            print word_checker["new_subject"]
            print word_checker["answer"]
            return True
    return False

def topic_changer(answer):
    if answer is "yes":
        return True
    else:
        return False


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
