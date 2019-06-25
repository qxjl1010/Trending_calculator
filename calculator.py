import os
import time
import datetime
from nltk.stem import WordNetLemmatizer
from nltk.stem.porter import PorterStemmer
from nltk.corpus import stopwords
import urllib.request
import requests
import pysher
import random
from pusher import Pusher
import json
from timeit import default_timer as timer
import mysql.connector
import re

SIXHOURS_KEEP_TIME = 21600
TWELVEHOURS_KEEP_TIME = 43200
ONEDAY_KEEP_TIME = 86400
ONEWEEK_KEEP_TIME = 604800
ONEMONTH_KEEP_TIME = 2592000
THREEMONTHS_KEEP_TIME = 2592000 * 3

DECAY_SPEED = 600
SIXHOURS_DECAY_SPEED_TUNE = 0.01
TWELVEHOURS_DECAY_SPEED_TUNE = 0.005
ONEDAY_DECAY_SPEED_TUNE = 0.0025
ONEWEEK_DECAY_SPEED_TUNE = 0.00035
ONEMONTH_DECAY_SPEED_TUNE = 0.00008
THREEMONTHS_DECAY_SPEED_TUNE = 0.000028


HOME_PATH = os.path.dirname( os.path.realpath( __file__ ) )



HASHTAG_PENALTY = 0

lemmatizer = WordNetLemmatizer()
stemmer = PorterStemmer()
stop = set(stopwords.words('english'))

sixhours_headline_list = []
sixhours_time_list = []
sixhours_ID_list = []
sixhours_importance_list = []
twelvehours_headline_list = []
twelvehours_time_list = []
twelvehours_ID_list =[]
twelvehours_importance_list =[]
oneday_headline_list = []
oneday_time_list = []
oneday_ID_list = []
oneday_importance_list = []
oneweek_headline_list = []
oneweek_time_list = []
oneweek_ID_list = []
oneweek_importance_list = []
onemonth_headline_list = []
onemonth_time_list = []
onemonth_ID_list =[]
onemonth_importance_list =[]
threemonths_headline_list = []
threemonths_time_list = []
threemonths_ID_list = []
threemonths_importance_list = []

# For now, importance logic not used
# importance_list = []

sixhours_topic_dict = {}
twelvehours_topic_dict = {}
oneday_topic_dict = {}
oneweek_topic_dict = {}
onemonth_topic_dict = {}
threemonths_topic_dict = {}

sixhours_id_dict = {}
twelvehours_id_dict = {}
oneday_id_dict = {}
oneweek_id_dict = {}
onemonth_id_dict = {}
threemonths_id_dict = {}

# store new headlines
tmp_headline_list = []


# My SQL Credentials--------------------------------------------------------
# mysql_user = 'terminal_beta'
mysql_user = 'root'
# mysql_password = 'Cool**88'
mysql_password = 'Bitcoin2018!'
mysql_database = 'cryptote_db2'
#mysql_host = '35.203.18.4' #Beta
mysql_host = '35.203.23.69' #Prod



cnx = mysql.connector.connect(user = mysql_user, password = mysql_password, host = mysql_host, database = mysql_database )
crsr = cnx.cursor(buffered=True)
mysql_insert_trend = ("INSERT INTO trends "
               "( trend, period, ids) "
               "VALUES (%(trend)s, %(period)s, %(ids)s)")

# -------------------------------------------------------------------

report_list = ["long on", "short on", "worth of", "USD) transferred"]

clean_word_dic = {}

time_format = '%Y-%m-%d %H:%M:%S'

# Now = datetime.datetime.strptime('2018-11-20 20:53:10', time_format)

# channel to push to ----------------------------------------------
channel = "private-trends"
event = "hours"


SLEEP_TIME = 2
PUSH_START_TIME = timer()
UPDATE_START_TIME = timer()
twelvehours_trend_json = ""
oneday_trend_json = ""
oneweek_trend_json = ""
threemonths_trend_json = ""
onemonth_trend_json = ""
sixhours_trend_json = ""

event_dict = {"sixhours": sixhours_trend_json, "twelvehours": twelvehours_trend_json, "oneday": oneday_trend_json, "oneweek": oneweek_trend_json, "onemonth": onemonth_trend_json, "threemonths": threemonths_trend_json}

event_dict_plusID = {"sixhours": sixhours_trend_json, "twelvehours": twelvehours_trend_json, "oneday": oneday_trend_json, "oneweek": oneweek_trend_json, "onemonth": onemonth_trend_json, "threemonths": threemonths_trend_json}


def init_dict():
    Now = datetime.datetime.now()
    # new: read from DB
    # get sixhours
    sixhours_before = Now + datetime.timedelta(hours=-9)
    str_sixhours_before = sixhours_before.strftime(time_format)
    crsr.execute("select text,created_at,id,rating3 from headlines where author != 'Crypto Terminal AI' and author != 'Icobrothers' and ((topic != 'price_action' and topic != 'hashtag' and topic != 'price action') or topic is null) and created_at > '%s'"%str_sixhours_before)
    # crsr.execute("select text,created_at,id from headlines where author != 'Crypto Terminal AI' and topic != 'price_action' and topic != 'price action' and topic != 'hashtag' and created_at > '2019-02-19 00:00:00'")
    
    sixhours_list = crsr.fetchall()
    
    for headline in sixhours_list:
        if "Price Analysis" in headline[0] or "Join us" in headline[0] or "Market Analysis" in headline[0] or headline[3] == 0 or headline[3] == -1 or "buy signal" in headline[0] or "sell signal" in headline[0]:
            continue
        created_at = headline[1]
        t = created_at.strftime(time_format)
        sixhours_headline_list.append(headline[0])
        sixhours_time_list.append(t)
        sixhours_ID_list.append(headline[2])
        sixhours_importance_list.append(headline[3])

    # get twelvehours
    twelvehours_before = Now + datetime.timedelta(hours=-12)
    str_twelvehours_before = twelvehours_before.strftime(time_format)
    crsr.execute("select text,created_at,id,rating3 from headlines where author != 'Crypto Terminal AI' and author != 'Icobrothers' and ((topic != 'price_action' and topic != 'hashtag' and topic != 'price action') or topic is null) and created_at > '%s'"%str_twelvehours_before)
    twelvehours_list = crsr.fetchall()
    for headline in twelvehours_list:
        if "Price Analysis" in headline[0] or "Join us" in headline[0] or "Market Analysis" in headline[0] or headline[3] == 0 or headline[3] == -1 or "buy signal" in headline[0] or "sell signal" in headline[0]:
            continue
        created_at = headline[1]
        t = created_at.strftime(time_format)
        twelvehours_headline_list.append(headline[0])
        twelvehours_time_list.append(t)
        twelvehours_ID_list.append(headline[2])
        twelvehours_importance_list.append(headline[3])
        
    # get oneday
    oneday_before = Now + datetime.timedelta(days=-1)
    str_oneday_before = oneday_before.strftime(time_format)
    crsr.execute("select text,created_at,id,rating3 from headlines where author != 'Crypto Terminal AI' and author != 'Icobrothers' and ((topic != 'price_action' and topic != 'hashtag' and topic != 'price action') or topic is null) and created_at > '%s'"%str_oneday_before)
    oneday_list = crsr.fetchall()
    for headline in oneday_list:
        if "Price Analysis" in headline[0] or "Join us" in headline[0] or "Market Analysis" in headline[0] or headline[3] == 0 or headline[3] == -1 or "buy signal" in headline[0] or "sell signal" in headline[0]:
            continue
        created_at = headline[1]
        t = created_at.strftime(time_format)
        oneday_headline_list.append(headline[0])
        oneday_time_list.append(t)
        oneday_ID_list.append(headline[2])
        oneday_importance_list.append(headline[3])

    # get oneweek
    oneweek_before = Now + datetime.timedelta(days=-7)
    str_oneweek_before = oneweek_before.strftime(time_format)
    crsr.execute("select text,created_at,id,rating3 from headlines where author != 'Crypto Terminal AI' and author != 'Icobrothers' and ((topic != 'price_action' and topic != 'hashtag' and topic != 'price action') or topic is null) and created_at > '%s'"%str_oneweek_before)
    oneweek_list = crsr.fetchall()

    for headline in oneweek_list:
        if "Price Analysis" in headline[0] or "Join us" in headline[0] or "Market Analysis" in headline[0] or headline[3] == 0 or headline[3] == -1 or "buy signal" in headline[0] or "sell signal" in headline[0]:
            continue
        created_at = headline[1]
        t = created_at.strftime(time_format)
        oneweek_headline_list.append(headline[0])
        oneweek_time_list.append(t)
        oneweek_ID_list.append(headline[2])
        oneweek_importance_list.append(headline[3])
    # get onemonth
    onemonth_before = Now + datetime.timedelta(days=-30)

    str_onemonth_before = onemonth_before.strftime(time_format)


    command = "select text,created_at,id,rating3 from headlines where author != 'Crypto Terminal AI' and author != 'Icobrothers' and ((topic != 'price_action' and topic != 'hashtag' and topic != 'price action') or topic is null) and created_at > '" + str_onemonth_before + "' union select text,created_at,id,rating3 from headline_archives where author != 'Crypto Terminal AI' and author != 'Icobrothers' and ((topic != 'price_action' and topic != 'hashtag' and topic != 'price action') or topic is null) and created_at > '" + str_onemonth_before + "'"

    print(command)
    crsr.execute(command)
    onemonth_list = crsr.fetchall()
    for headline in onemonth_list:
        if "Price Analysis" in headline[0] or "Join us" in headline[0] or "Market Analysis" in headline[0] or headline[3] == 0 or headline[3] == -1 or "buy signal" in headline[0] or "sell signal" in headline[0]:
            continue
        created_at = headline[1]
        t = created_at.strftime(time_format)
        onemonth_headline_list.append(headline[0])
        onemonth_time_list.append(t)
        onemonth_ID_list.append(headline[2])
        onemonth_importance_list.append(headline[3])

    # get threemonths
    threemonths_before = Now + datetime.timedelta(days=-90)
    str_threemonths_before = threemonths_before.strftime(time_format)
    crsr.execute("select text,created_at,id,rating3 from headlines where author != 'Crypto Terminal AI' and author != 'Icobrothers' and ((topic != 'price_action' and topic != 'hashtag' and topic != 'price action') or topic is null) and created_at > '" + str_threemonths_before + "' union select text,created_at,id,rating3 from headline_archives where author != 'Crypto Terminal AI' and author != 'Icobrothers' and ((topic != 'price_action' and topic != 'hashtag' and topic != 'price action') or topic is null) and created_at > '" + str_threemonths_before + "'")
    threemonths_list = crsr.fetchall()
    for headline in threemonths_list:
        if "Price Analysis" in headline[0] or "Join us" in headline[0] or "Market Analysis" in headline[0] or headline[3] == 0 or headline[3] == -1 or "buy signal" in headline[0] or "sell signal" in headline[0]:
            continue
        created_at = headline[1]
        t = created_at.strftime(time_format)
        threemonths_headline_list.append(headline[0])
        threemonths_time_list.append(t)
        threemonths_ID_list.append(headline[2])
        threemonths_importance_list.append(headline[3])
        


def headline_cutting(headline):
    is_report = False
    
    for report_word in report_list:
        if report_word in headline:
            is_report = True
            return [], is_report
    keep_list = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z','A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z','0','1','2','3','4','5','6','7','8','9']

    words = headline.split()
    topic_list = []
    word_list = []
    clean_headline = ""
    for word in words:
        if word[0] == '@' or word[0] == '#' or word[0] == '&':
            continue
        c_word = ''
        if 'http' in word:
            continue
        for w in word:
            if w in keep_list:
                c_word += w

        word = c_word.replace(',', '')
        word = word.replace('?', '')
        word = word.replace('.', '')
        word = word.replace("'", '')
        word = word.replace("\"", '')
        word = word.replace('-', '')
        if word != '':
            clean_word = word.lower()
            clean_word = lemmatizer.lemmatize(word)
            # clean_word = stemmer.stem(clean_word)
            if clean_word in stop:
                continue
        else:
            continue
        word_list.append(clean_word)
        clean_headline = clean_headline + clean_word + " "
    # insert 1 word topic:
    for i in range(len(word_list)):
        if word_list[i] not in topic_list:
            topic_list.append(word_list[i])
    
    # insert 2 words topic:
    for i in range(len(word_list) - 1):
        topic = word_list[i] + ' ' + word_list[i+1]
        if topic not in topic_list:
            topic_list.append(topic)


    # don't receive 3 words
    '''    
    # insert 3 words topic:
    for i in range(len(word_list) - 2):
        topic = word_list[i] + ' ' + word_list[i+1] + ' ' + word_list[i+2]
        topic_list.append(topic)
    '''
    
    return topic_list, is_report



def decay():

    Now = datetime.datetime.now()
    

    # minus logic
    # recalculate dict
    sixhours_decay_speed = (DECAY_SPEED)/SIXHOURS_KEEP_TIME
    delete_list = []
    for key in sixhours_topic_dict:
        sixhours_topic_dict[key] = sixhours_topic_dict[key] * (1 - sixhours_decay_speed)
        sixhours_topic_dict[key] -= SIXHOURS_DECAY_SPEED_TUNE
        if sixhours_topic_dict[key] <= 0:
            delete_list.append(key)

    for l in delete_list: 
        sixhours_topic_dict.pop(l)
        sixhours_id_dict.pop(l)
    # clean lists
    delete_time_list = []
    for t in sixhours_time_list:
        if (((Now - datetime.datetime.strptime(t, time_format)).seconds) + ((Now - datetime.datetime.strptime(t, time_format)).days * 86400)) >= SIXHOURS_KEEP_TIME:
            delete_time_list.append(t)

    for t in delete_time_list:
        pos = sixhours_time_list.index(t)
        headline_id = sixhours_ID_list[pos]
        sixhours_time_list.pop(pos)
        sixhours_ID_list.pop(pos)
        sixhours_headline_list.pop(pos)
        sixhours_importance_list.pop(pos)
        for items in sixhours_id_dict.values():
            if headline_id in items:
                items.remove(headline_id)




    sixhours_trend = sorted(sixhours_topic_dict.items(), key = lambda x:x[1], reverse = True)


    i = 0
    tmp_dict = {}
    tmp_id_dict = {}
    for topic in sixhours_trend:
        if i >= 500:
            break
        if len(tmp_dict) == 0:

            tmp_dict[topic[0]] = topic[1]
            tmp_id_dict[topic[0]] = sixhours_id_dict.get(topic[0])
        else:
            same_id = 0
            is_dup = False
            for exist_key in tmp_id_dict:
                if len(sixhours_id_dict.get(topic[0])) != 0:
                    for id in sixhours_id_dict.get(topic[0]):
                        if id in tmp_id_dict[exist_key]:
                            same_id += 1
                    if same_id/len(sixhours_id_dict.get(topic[0])) >= 0.5:
                        is_dup = True
                        break
                same_id = 0

            if is_dup == False:
                tmp_dict[topic[0]] = topic[1]
                tmp_id_dict[topic[0]] = sixhours_id_dict.get(topic[0])



        i += 1
    sixhours_trend_json = []
    i = 0
    for k in tmp_dict:
        if i >= 15:
            break
        
        subitem = {}
        subitem["text"] = k
        subitem["weight"] = round(tmp_dict[k], 2)
        subitem["ids"] = ','.join(str(e) for e in sixhours_id_dict.get(k))
        if len(subitem["ids"]) < 8:
            continue
        sixhours_trend_json.append(subitem)
        i += 1
    event_dict["sixhours"] = json.dumps(sixhours_trend_json)

    
    sixhours_trend_json = []
    trend_text, ids = extract_id(event_dict["sixhours"])

    data = {'trend': trend_text, 'period': "sixhours", 'ids': ids}


    crsr.execute(mysql_insert_trend, data)
    topic_id = crsr.lastrowid


    subitem = {}
    subitem["objects"] = trend_text
    subitem["period"] = "sixhours"
    subitem["id"] = topic_id
    sixhours_trend_json.append(subitem)
    event_dict_plusID["sixhours"] = json.dumps(sixhours_trend_json)




    # recalculate dict
    twelvehours_decay_speed = (DECAY_SPEED)/TWELVEHOURS_KEEP_TIME
    delete_list = []
    for key in twelvehours_topic_dict:
        twelvehours_topic_dict[key] = twelvehours_topic_dict[key] * (1 - twelvehours_decay_speed)
        twelvehours_topic_dict[key] -= TWELVEHOURS_DECAY_SPEED_TUNE
        if twelvehours_topic_dict[key] <= 0:
            delete_list.append(key)
    for l in delete_list:
        twelvehours_topic_dict.pop(l)
        twelvehours_id_dict.pop(l)
    # clean lists
    delete_time_list = []
    for t in twelvehours_time_list:
        if (((Now - datetime.datetime.strptime(t, time_format)).seconds) + ((Now - datetime.datetime.strptime(t, time_format)).days * 86400)) >= TWELVEHOURS_KEEP_TIME:
            delete_time_list.append(t)
    for t in delete_time_list:
        pos = twelvehours_time_list.index(t)
        headline_id = twelvehours_ID_list[pos]
        twelvehours_time_list.pop(pos)
        twelvehours_ID_list.pop(pos)
        twelvehours_headline_list.pop(pos)
        twelvehours_importance_list.pop(pos)
        for items in twelvehours_id_dict.values():
            if headline_id in items:
                items.remove(headline_id)



    twelvehours_trend = sorted(twelvehours_topic_dict.items(), key = lambda x:x[1], reverse = True)


    i = 0
    tmp_dict = {}
    tmp_id_dict = {}
    for topic in twelvehours_trend:
        if i >= 500:
            break
        if len(tmp_dict) == 0:
            tmp_dict[topic[0]] = topic[1]
            tmp_id_dict[topic[0]] = twelvehours_id_dict.get(topic[0])
        else:
            same_id = 0
            is_dup = False
            for exist_key in tmp_id_dict:
                if len(twelvehours_id_dict.get(topic[0])) != 0:
                    for id in twelvehours_id_dict.get(topic[0]):

                        if id in tmp_id_dict[exist_key]:
                            same_id += 1
                    if same_id/len(twelvehours_id_dict.get(topic[0])) >= 0.5:
                        is_dup = True
                        break
                same_id = 0
            if is_dup == False:
                tmp_dict[topic[0]] = topic[1]
                tmp_id_dict[topic[0]] = twelvehours_id_dict.get(topic[0])


        i += 1



    twelvehours_trend_json = []
    i = 0

    for k in tmp_dict:
        if i >= 15:
            break
        
        subitem = {}
        subitem["text"] = k
        subitem["weight"] = round(tmp_dict[k], 2)
        subitem["ids"] = ','.join(str(e) for e in twelvehours_id_dict.get(k))
        if len(subitem["ids"]) < 8:
            continue
        twelvehours_trend_json.append(subitem)
        i += 1
    event_dict["twelvehours"] = json.dumps(twelvehours_trend_json)


    twelvehours_trend_json = []
    trend_text, ids = extract_id(event_dict["twelvehours"])

    data = {'trend': trend_text, 'period': "twelvehours", 'ids': ids}
    crsr.execute(mysql_insert_trend, data)
    topic_id = crsr.lastrowid


    subitem = {}
    subitem["objects"] = trend_text
    subitem["period"] = "twelvehours"
    subitem["id"] = topic_id
    twelvehours_trend_json.append(subitem)
    event_dict_plusID["twelvehours"] = json.dumps(twelvehours_trend_json)


    # recalculate dict
    oneday_decay_speed = (DECAY_SPEED)/ONEDAY_KEEP_TIME
    delete_list = []
    for key in oneday_topic_dict:
        oneday_topic_dict[key] = oneday_topic_dict[key] * (1 - oneday_decay_speed)
        oneday_topic_dict[key] -= ONEDAY_DECAY_SPEED_TUNE
        if oneday_topic_dict[key] <= 0:
            delete_list.append(key)
    for l in delete_list:
        oneday_topic_dict.pop(l)
        oneday_id_dict.pop(l)

    # clean lists
    delete_time_list = []
    for t in oneday_time_list:
        if (((Now - datetime.datetime.strptime(t, time_format)).seconds) + ((Now - datetime.datetime.strptime(t, time_format)).days * 86400)) >= ONEDAY_KEEP_TIME:
            delete_time_list.append(t)

    for t in delete_time_list:
        pos = oneday_time_list.index(t)
        headline_id = oneday_ID_list[pos]
        oneday_time_list.pop(pos)
        oneday_ID_list.pop(pos)
        oneday_headline_list.pop(pos)
        oneday_importance_list.pop(pos)
        for items in oneday_id_dict.values():
            if headline_id in items:
                items.remove(headline_id)



    oneday_trend = sorted(oneday_topic_dict.items(), key = lambda x:x[1], reverse = True)


    i = 0
    tmp_dict = {}
    tmp_id_dict = {}
    for topic in oneday_trend:
        if i >= 500:
            break
        if len(tmp_dict) == 0:
            tmp_dict[topic[0]] = topic[1]
            tmp_id_dict[topic[0]] = oneday_id_dict.get(topic[0])
        else:
            same_id = 0
            is_dup = False
            for exist_key in tmp_id_dict:
                if len(oneday_id_dict.get(topic[0])) != 0:
                    for id in oneday_id_dict.get(topic[0]):

                        if id in tmp_id_dict[exist_key]:
                            same_id += 1
                    if same_id/len(oneday_id_dict.get(topic[0])) >= 0.5:
                        is_dup = True
                        break
                same_id = 0
            if is_dup == False:
                tmp_dict[topic[0]] = topic[1]
                tmp_id_dict[topic[0]] = oneday_id_dict.get(topic[0])


        i += 1

    oneday_trend_json = []
    i = 0

    for k in tmp_dict:
        if i >= 15:
            break
        
        subitem = {}
        subitem["text"] = k
        subitem["weight"] = round(tmp_dict[k], 2)
        subitem["ids"] = ','.join(str(e) for e in oneday_id_dict.get(k))
        if len(subitem["ids"]) < 8:
            continue
        oneday_trend_json.append(subitem)
        i += 1

    event_dict["oneday"] = json.dumps(oneday_trend_json)


    oneday_trend_json = []
    trend_text, ids = extract_id(event_dict["oneday"])

    data = {'trend': trend_text, 'period': "oneday", 'ids': ids}
    crsr.execute(mysql_insert_trend, data)
    topic_id = crsr.lastrowid


    subitem = {}
    subitem["objects"] = trend_text
    subitem["period"] = "oneday"
    subitem["id"] = topic_id
    oneday_trend_json.append(subitem)
    event_dict_plusID["oneday"] = json.dumps(oneday_trend_json)

    
    # recalculate dict
    oneweek_decay_speed = (DECAY_SPEED)/ONEWEEK_KEEP_TIME
    delete_list = []
    for key in oneweek_topic_dict:
        oneweek_topic_dict[key] = oneweek_topic_dict[key] * (1 - oneweek_decay_speed)
        oneweek_topic_dict[key] -= ONEWEEK_DECAY_SPEED_TUNE
        if oneweek_topic_dict[key] <= 0:
            delete_list.append(key)
    for l in delete_list:
        oneweek_topic_dict.pop(l)
        oneweek_id_dict.pop(l)

    # clean lists
    delete_time_list = []
    for t in oneweek_time_list:
        if (((Now - datetime.datetime.strptime(t, time_format)).seconds) + ((Now - datetime.datetime.strptime(t, time_format)).days * 86400)) >= ONEWEEK_KEEP_TIME:
            delete_time_list.append(t)

    for t in delete_time_list:
        pos = oneweek_time_list.index(t)
        headline_id = oneweek_ID_list[pos]
        oneweek_time_list.pop(pos)
        oneweek_ID_list.pop(pos)
        oneweek_headline_list.pop(pos)
        oneweek_importance_list.pop(pos)
        for items in oneweek_id_dict.values():
            if headline_id in items:
                items.remove(headline_id)




    oneweek_trend = sorted(oneweek_topic_dict.items(), key = lambda x:x[1], reverse = True)


    i = 0
    tmp_dict = {}
    tmp_id_dict = {}
    for topic in oneweek_trend:
        if i >= 500:
            break
        if len(tmp_dict) == 0:
            tmp_dict[topic[0]] = topic[1]
            tmp_id_dict[topic[0]] = oneweek_id_dict.get(topic[0])
        else:
            same_id = 0
            is_dup = False
            for exist_key in tmp_id_dict:
                if len(oneweek_id_dict.get(topic[0])) != 0:
                    for id in oneweek_id_dict.get(topic[0]):

                        if id in tmp_id_dict[exist_key]:
                            same_id += 1
                    if same_id/len(oneweek_id_dict.get(topic[0])) >= 0.5:
                        is_dup = True
                        break
                same_id = 0
            if is_dup == False:
                tmp_dict[topic[0]] = topic[1]
                tmp_id_dict[topic[0]] = oneweek_id_dict.get(topic[0])


        i += 1

    oneweek_trend_json = []
    i = 0

    for k in tmp_dict:
        if i >= 15:
            break
        
        subitem = {}
        subitem["text"] = k
        subitem["weight"] = round(tmp_dict[k], 2)
        subitem["ids"] = ','.join(str(e) for e in oneweek_id_dict.get(k))
        if len(subitem["ids"]) < 8:
            continue
        oneweek_trend_json.append(subitem)
        i += 1

    event_dict["oneweek"] = json.dumps(oneweek_trend_json)


    oneweek_trend_json = []
    trend_text, ids = extract_id(event_dict["oneweek"])

    data = {'trend': trend_text, 'period': "oneweek", 'ids': ids}
    crsr.execute(mysql_insert_trend, data)
    topic_id = crsr.lastrowid


    subitem = {}
    subitem["objects"] = trend_text
    subitem["period"] = "oneweek"
    subitem["id"] = topic_id
    oneweek_trend_json.append(subitem)
    event_dict_plusID["oneweek"] = json.dumps(oneweek_trend_json)

    
    # recalculate dict
    onemonth_decay_speed = (DECAY_SPEED)/ONEMONTH_KEEP_TIME
    delete_list = []
    for key in onemonth_topic_dict:
        onemonth_topic_dict[key] = onemonth_topic_dict[key] * (1 - onemonth_decay_speed)
        onemonth_topic_dict[key] -= ONEMONTH_DECAY_SPEED_TUNE
        if onemonth_topic_dict[key] <= 0:
            delete_list.append(key)
    for l in delete_list:
        onemonth_topic_dict.pop(l)
        onemonth_id_dict.pop(l)

    # clean lists
    delete_time_list = []
    for t in onemonth_time_list:
        if (((Now - datetime.datetime.strptime(t, time_format)).seconds) + ((Now - datetime.datetime.strptime(t, time_format)).days * 86400)) >= ONEMONTH_KEEP_TIME:
            delete_time_list.append(t)

    for t in delete_time_list:
        pos = onemonth_time_list.index(t)
        headline_id = onemonth_ID_list[pos]
        onemonth_time_list.pop(pos)
        onemonth_ID_list.pop(pos)
        onemonth_headline_list.pop(pos)
        onemonth_importance_list.pop(pos)       
        for items in onemonth_id_dict.values():
            if headline_id in items:
                items.remove(headline_id)

    onemonth_trend = sorted(onemonth_topic_dict.items(), key = lambda x:x[1], reverse = True)


    i = 0
    tmp_dict = {}
    tmp_id_dict = {}
    for topic in onemonth_trend:
        if i >= 500:
            break
        if len(tmp_dict) == 0:
            tmp_dict[topic[0]] = topic[1]
            tmp_id_dict[topic[0]] = onemonth_id_dict.get(topic[0])
        else:
            same_id = 0
            is_dup = False
            for exist_key in tmp_id_dict:
                if len(onemonth_id_dict.get(topic[0])) != 0:
                    for id in onemonth_id_dict.get(topic[0]):

                        if id in tmp_id_dict[exist_key]:
                            same_id += 1
                    if same_id/len(onemonth_id_dict.get(topic[0])) >= 0.5:
                        is_dup = True
                        break
                same_id = 0
            if is_dup == False:
                tmp_dict[topic[0]] = topic[1]
                tmp_id_dict[topic[0]] = onemonth_id_dict.get(topic[0])


        i += 1

    onemonth_trend_json = []
    i = 0

    for k in tmp_dict:
        if i >= 15:
            break
        
        subitem = {}
        subitem["text"] = k
        subitem["weight"] = round(tmp_dict[k], 2)
        subitem["ids"] = ','.join(str(e) for e in onemonth_id_dict.get(k))
        if len(subitem["ids"]) < 8:
            continue
        onemonth_trend_json.append(subitem)
        i += 1

    event_dict["onemonth"] = json.dumps(onemonth_trend_json)
    

    onemonth_trend_json = []
    trend_text, ids = extract_id(event_dict["onemonth"])

    data = {'trend': trend_text, 'period': "onemonth", 'ids': ids}
    crsr.execute(mysql_insert_trend, data)
    topic_id = crsr.lastrowid


    subitem = {}
    subitem["objects"] = trend_text
    subitem["period"] = "onemonth"
    subitem["id"] = topic_id
    onemonth_trend_json.append(subitem)
    event_dict_plusID["onemonth"] = json.dumps(onemonth_trend_json)


    # recalculate dict
    threemonths_decay_speed = (DECAY_SPEED)/THREEMONTHS_KEEP_TIME
    delete_list = []
    for key in threemonths_topic_dict:
        threemonths_topic_dict[key] = threemonths_topic_dict[key] * (1 - threemonths_decay_speed)
        threemonths_topic_dict[key] -= THREEMONTHS_DECAY_SPEED_TUNE
        if threemonths_topic_dict[key] <= 0:
            delete_list.append(key)
    for l in delete_list:
        threemonths_topic_dict.pop(l)
        threemonths_id_dict.pop(l)

    # clean lists
    delete_time_list = []
    for t in threemonths_time_list:
        if (((Now - datetime.datetime.strptime(t, time_format)).seconds) + ((Now - datetime.datetime.strptime(t, time_format)).days * 86400)) >= THREEMONTHS_KEEP_TIME:
            delete_time_list.append(t)

    for t in delete_time_list:
        pos = threemonths_time_list.index(t)
        headline_id = threemonths_ID_list[pos]
        threemonths_time_list.pop(pos)
        threemonths_ID_list.pop(pos)
        threemonths_headline_list.pop(pos)
        threemonths_importance_list.pop(pos)                    
        for items in threemonths_id_dict.values():
            if headline_id in items:
                items.remove(headline_id)


    threemonths_trend = sorted(threemonths_topic_dict.items(), key = lambda x:x[1], reverse = True)


    i = 0
    tmp_dict = {}
    tmp_id_dict = {}
    for topic in threemonths_trend:
        if i >= 500:
            break
        if len(tmp_dict) == 0:
            tmp_dict[topic[0]] = topic[1]
            tmp_id_dict[topic[0]] = threemonths_id_dict.get(topic[0])
        else:
            same_id = 0
            is_dup = False
            for exist_key in tmp_id_dict:
                if len(threemonths_id_dict.get(topic[0])) != 0:
                    for id in threemonths_id_dict.get(topic[0]):

                        if id in tmp_id_dict[exist_key]:
                            same_id += 1
                    if same_id/len(threemonths_id_dict.get(topic[0])) >= 0.5:
                        is_dup = True
                        break
                same_id = 0
            if is_dup == False:
                tmp_dict[topic[0]] = topic[1]
                tmp_id_dict[topic[0]] = threemonths_id_dict.get(topic[0])


        i += 1

    threemonths_trend_json = []
    i = 0

    for k in tmp_dict:
        if i >= 15:
            break
        
        subitem = {}
        subitem["text"] = k
        subitem["weight"] = round(tmp_dict[k], 2)
        subitem["ids"] = ','.join(str(e) for e in threemonths_id_dict.get(k))
        if len(subitem["ids"]) < 8:
            continue
        threemonths_trend_json.append(subitem)
        i += 1

    event_dict["threemonths"] = json.dumps(threemonths_trend_json)


    threemonths_trend_json = []
    trend_text, ids = extract_id(event_dict["threemonths"])

    data = {'trend': trend_text, 'period': "threemonths", 'ids': ids}
    crsr.execute(mysql_insert_trend, data)
    topic_id = crsr.lastrowid


    subitem = {}
    subitem["objects"] = trend_text
    subitem["period"] = "threemonths"
    subitem["id"] = topic_id
    threemonths_trend_json.append(subitem)
    event_dict_plusID["threemonths"] = json.dumps(threemonths_trend_json)

    cnx.commit()

    insert_new()
        
        




    

def insert_new():
    
    global tmp_headline_list
    for new_head in tmp_headline_list:
        
        args_str = new_head
        headline_start = args_str.index("\"text\":\"") + 8
        headline_end = args_str.index("\",\"content\"")
        new_headline = args_str[headline_start: headline_end]
        if ("\"topic\":null") in args_str:
            new_topic = "null"
        else:
            topic_start = args_str.index("\"topic\":\"") + 9
            topic_end = args_str.index("\",\"duplicate\"")
            new_topic = args_str[topic_start: topic_end]
        ID_start = args_str.index("\"id\":") + 5
        ID_end = args_str.index(",\"author\"")
        new_ID = args_str[ID_start: ID_end]
        # weight low to hashtag headlines
        is_hashtag = False
        if new_topic == 'hashtag':
            is_hashtag = True
        if new_topic == 'price_action':
            continue
        # importance_start = args_str.index("\"importance\":\"") + 14
        # importamce_end = args_str.index("\",\"link\"")
        # importance = args_str[importance_start: importamce_end]
        new_headline_importance = 1
        # change importance

        # new_headline = input('headline?')
        new_headline_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # insert new topic
        topic_list, is_report = headline_cutting(new_headline)
        sixhours_headline_list.append(topic_list)
        sixhours_time_list.append(new_headline_time)
        sixhours_ID_list.append(new_ID)


        # maunually set new importance to 3, waiting for Diego's change
        # ====================================================================================================================   
        # ====================================================================================================================   
        sixhours_importance_list.append(3.0)
        twelvehours_importance_list.append(3.0)
        oneday_importance_list.append(3.0)
        oneweek_importance_list.append(3.0)
        onemonth_importance_list.append(3.0)
        threemonths_importance_list.append(3.0)
        # ====================================================================================================================   
        # ====================================================================================================================   
        
        
        
        
        twelvehours_headline_list.append(topic_list)
        twelvehours_time_list.append(new_headline_time)
        twelvehours_ID_list.append(new_ID)
        oneday_headline_list.append(topic_list)
        oneday_time_list.append(new_headline_time)
        oneday_ID_list.append(new_ID)
        oneweek_headline_list.append(topic_list)
        oneweek_time_list.append(new_headline_time)
        oneweek_ID_list.append(new_ID)
        onemonth_headline_list.append(topic_list)
        onemonth_time_list.append(new_headline_time)
        onemonth_ID_list.append(new_ID)
        threemonths_headline_list.append(topic_list)
        threemonths_time_list.append(new_headline_time)
        threemonths_ID_list.append(new_ID)

        # importance_list.append(new_headline_importance)

        # from Dec.7 not decay here
        # decay("")
        if is_report == False:
            for i in range(len(topic_list)):
                words = topic_list[i].split()
                if len(words) == 1:
                    enhance_weight = 1
                    continue
                elif len(words) == 2:
                    enhance_weight = 1
                else:
                    enhance_weight = 1
                    continue
                # Add new topic in dictionary
                if sixhours_topic_dict.get(topic_list[i]) == None:
                    if is_hashtag == True:
                        sixhours_topic_dict[topic_list[i]] = new_headline_importance * enhance_weight * HASHTAG_PENALTY
                    else:
                        sixhours_topic_dict[topic_list[i]] = new_headline_importance * enhance_weight
                # Add weight
                else:
                    if is_hashtag == True:
                        sixhours_topic_dict[topic_list[i]] = sixhours_topic_dict.get(topic_list[i]) + new_headline_importance * enhance_weight * HASHTAG_PENALTY
                    else:
                        sixhours_topic_dict[topic_list[i]] = sixhours_topic_dict.get(topic_list[i]) + new_headline_importance * enhance_weight 

                # Add new id in dictionary
                if sixhours_id_dict.get(topic_list[i]) == None:
                    l = [new_ID]
                    sixhours_id_dict[topic_list[i]] = l
                else:
                    
                    sixhours_id_dict[topic_list[i]].append(new_ID)
                    





                if twelvehours_topic_dict.get(topic_list[i]) == None:
                    if is_hashtag == True:
                        twelvehours_topic_dict[topic_list[i]] = new_headline_importance * enhance_weight * HASHTAG_PENALTY
                    else:
                        twelvehours_topic_dict[topic_list[i]] = new_headline_importance * enhance_weight
                else:
                    if is_hashtag == True:
                        twelvehours_topic_dict[topic_list[i]] = twelvehours_topic_dict.get(topic_list[i]) + new_headline_importance * enhance_weight * HASHTAG_PENALTY
                    else:
                        twelvehours_topic_dict[topic_list[i]] = twelvehours_topic_dict.get(topic_list[i]) + new_headline_importance * enhance_weight             

                # Add new id in dictionary
                if twelvehours_id_dict.get(topic_list[i]) == None:
                    l = [new_ID]
                    twelvehours_id_dict[topic_list[i]] = l
                else:
                    twelvehours_id_dict[topic_list[i]].append(new_ID)


                if oneday_topic_dict.get(topic_list[i]) == None:
                    if is_hashtag == True:
                        oneday_topic_dict[topic_list[i]] = new_headline_importance * enhance_weight * HASHTAG_PENALTY
                    else:
                        oneday_topic_dict[topic_list[i]] = new_headline_importance * enhance_weight
                else:
                    if is_hashtag == True:
                        oneday_topic_dict[topic_list[i]] = oneday_topic_dict.get(topic_list[i]) + new_headline_importance * enhance_weight * HASHTAG_PENALTY
                    else:
                        oneday_topic_dict[topic_list[i]] = oneday_topic_dict.get(topic_list[i]) + new_headline_importance * enhance_weight

                # Add new id in dictionary
                if oneday_id_dict.get(topic_list[i]) == None:
                    l = [new_ID]
                    oneday_id_dict[topic_list[i]] = l
                else:
                    oneday_id_dict[topic_list[i]].append(new_ID)


                if oneweek_topic_dict.get(topic_list[i]) == None:
                    if is_hashtag == True:
                        oneweek_topic_dict[topic_list[i]] = new_headline_importance * enhance_weight * HASHTAG_PENALTY
                    else:
                        oneweek_topic_dict[topic_list[i]] = new_headline_importance * enhance_weight
                else:
                    if is_hashtag == True:
                        oneweek_topic_dict[topic_list[i]] = oneweek_topic_dict.get(topic_list[i]) + new_headline_importance * enhance_weight * HASHTAG_PENALTY
                    else:
                        oneweek_topic_dict[topic_list[i]] = oneweek_topic_dict.get(topic_list[i]) + new_headline_importance * enhance_weight

                # Add new id in dictionary
                if oneweek_id_dict.get(topic_list[i]) == None:
                    l = [new_ID]
                    oneweek_id_dict[topic_list[i]] = l
                else:
                    oneweek_id_dict[topic_list[i]].append(new_ID)


                if onemonth_topic_dict.get(topic_list[i]) == None:
                    if is_hashtag == True:
                        onemonth_topic_dict[topic_list[i]] = new_headline_importance * enhance_weight * HASHTAG_PENALTY
                    else:
                        onemonth_topic_dict[topic_list[i]] = new_headline_importance * enhance_weight
                else:
                    if is_hashtag == True:
                        onemonth_topic_dict[topic_list[i]] = onemonth_topic_dict.get(topic_list[i]) + new_headline_importance * enhance_weight * HASHTAG_PENALTY
                    else:
                        onemonth_topic_dict[topic_list[i]] = onemonth_topic_dict.get(topic_list[i]) + new_headline_importance * enhance_weight

                # Add new id in dictionary
                if onemonth_id_dict.get(topic_list[i]) == None:
                    l = [new_ID]
                    onemonth_id_dict[topic_list[i]] = l
                else:
                    onemonth_id_dict[topic_list[i]].append(new_ID)



                if threemonths_topic_dict.get(topic_list[i]) == None:
                    if is_hashtag == True:
                        threemonths_topic_dict[topic_list[i]] = new_headline_importance * enhance_weight * HASHTAG_PENALTY
                    else:
                        threemonths_topic_dict[topic_list[i]] = new_headline_importance * enhance_weight
                else:
                    if is_hashtag == True:
                        threemonths_topic_dict[topic_list[i]] = threemonths_topic_dict.get(topic_list[i]) + new_headline_importance * enhance_weight * HASHTAG_PENALTY
                    else:
                        threemonths_topic_dict[topic_list[i]] = threemonths_topic_dict.get(topic_list[i]) + new_headline_importance * enhance_weight

                # Add new id in dictionary
                if threemonths_id_dict.get(topic_list[i]) == None:
                    l = [new_ID]
                    threemonths_id_dict[topic_list[i]] = l
                else:
                    threemonths_id_dict[topic_list[i]].append(new_ID)

        sixhours_trend = sorted(sixhours_topic_dict.items(), key = lambda x:x[1], reverse = True)
        twelvehours_trend = sorted(twelvehours_topic_dict.items(), key = lambda x:x[1], reverse = True)
        oneday_trend = sorted(oneday_topic_dict.items(), key = lambda x:x[1], reverse = True)
        oneweek_trend = sorted(oneweek_topic_dict.items(), key = lambda x:x[1], reverse = True)
        onemonth_trend = sorted(onemonth_topic_dict.items(), key = lambda x:x[1], reverse = True)
        threemonths_trend = sorted(threemonths_topic_dict.items(), key = lambda x:x[1], reverse = True)
        # don't show topics from same headlines
        i = 0
        tmp_dict = {}
        tmp_id_dict = {}
        for topic in sixhours_trend:
            # print("i is:" + str(i))
            if i >= 500:
                break
            
            if len(tmp_dict) == 0:
                tmp_dict[topic[0]] = topic[1]
                tmp_id_dict[topic[0]] = sixhours_id_dict.get(topic[0])
            else:
                same_id = 0
                is_dup = False
                for exist_key in tmp_id_dict:
                    for id in sixhours_id_dict.get(topic[0]):

                        if id in tmp_id_dict[exist_key]:
                            same_id += 1
                    if same_id/len(sixhours_id_dict.get(topic[0])) >= 0.5:
                        is_dup = True
                        break
                    same_id = 0
                if is_dup == False:
                    tmp_dict[topic[0]] = topic[1]
                    tmp_id_dict[topic[0]] = sixhours_id_dict.get(topic[0])

            
            i += 1
        sixhours_trend_json = []
        i = 0
        for k in tmp_dict:
            if i >= 15:
                break
        
            subitem = {}
            subitem["text"] = k
            subitem["weight"] = round(tmp_dict[k], 2)
            subitem["ids"] = ','.join(str(e) for e in sixhours_id_dict.get(k))
            if len(subitem["ids"]) < 8:
                continue
            sixhours_trend_json.append(subitem)
            i += 1
        event_dict["sixhours"] = json.dumps(sixhours_trend_json)
        
        i = 0
        tmp_dict = {}
        tmp_id_dict = {}
        for topic in twelvehours_trend:
            # print("i is: " +str(i))
            if i >= 500:
                break 
            if len(tmp_dict) == 0:

                tmp_dict[topic[0]] = topic[1]
                tmp_id_dict[topic[0]] = twelvehours_id_dict.get(topic[0])
            else:

                same_id = 0
                is_dup = False
                for exist_key in tmp_id_dict:
                    for id in twelvehours_id_dict.get(topic[0]):
                        if id in tmp_id_dict[exist_key]:
                            same_id += 1
                    if same_id/len(twelvehours_id_dict.get(topic[0])) >= 0.5:
                        is_dup = True
                        break
                    same_id = 0

                if is_dup == False:
                    tmp_dict[topic[0]] = topic[1]
                    tmp_id_dict[topic[0]] = twelvehours_id_dict.get(topic[0])
            i += 1

        twelvehours_trend_json = []
        i = 0
        
        for k in tmp_dict:
            if i >= 15:
                break
            subitem = {}
            subitem["text"] = k
            subitem["weight"] = round(tmp_dict[k], 2)
            subitem["ids"] = ','.join(str(e) for e in twelvehours_id_dict.get(k))
            if len(subitem["ids"]) < 8:
                continue
            twelvehours_trend_json.append(subitem)
            i += 1

        event_dict["twelvehours"] = json.dumps(twelvehours_trend_json)
        

        i = 0
        tmp_dict = {}
        tmp_id_dict = {}
        for topic in oneday_trend:
            if i >= 300:
                break
            if len(tmp_dict) == 0:
                tmp_dict[topic[0]] = topic[1]
                tmp_id_dict[topic[0]] = oneday_id_dict.get(topic[0])
            else:
                same_id = 0
                is_dup = False
                for exist_key in tmp_id_dict:
                    for id in oneday_id_dict.get(topic[0]):
                        if id in tmp_id_dict[exist_key]:
                            same_id += 1
                    if same_id/len(oneday_id_dict.get(topic[0])) >= 0.5:
                        is_dup = True
                        break
                    same_id = 0
                if is_dup == False:
                    tmp_dict[topic[0]] = topic[1]
                    tmp_id_dict[topic[0]] = oneday_id_dict.get(topic[0])

            i += 1
    
        oneday_trend_json = []
        i = 0
        for k in tmp_dict:
            if i >= 15:
                break
            subitem = {}
            subitem["text"] = k
            subitem["weight"] = round(tmp_dict[k], 2)
            subitem["ids"] = ','.join(str(e) for e in oneday_id_dict.get(k))
            if len(subitem["ids"]) < 8:
                continue
            oneday_trend_json.append(subitem)
            i += 1

        event_dict["oneday"] = json.dumps(oneday_trend_json)



        i = 0
        tmp_dict = {}
        tmp_id_dict = {}
        for topic in oneweek_trend:
            if i >= 300:
                break
            if len(tmp_dict) == 0:
                tmp_dict[topic[0]] = topic[1]
                tmp_id_dict[topic[0]] = oneweek_id_dict.get(topic[0])
            else:
                same_id = 0
                is_dup = False
                for exist_key in tmp_id_dict:
                    for id in oneweek_id_dict.get(topic[0]):
                        if id in tmp_id_dict[exist_key]:
                            same_id += 1
                    if same_id/len(oneweek_id_dict.get(topic[0])) >= 0.5:
                        is_dup = True
                        break
                    same_id = 0
                if is_dup == False:
                    tmp_dict[topic[0]] = topic[1]
                    tmp_id_dict[topic[0]] = oneweek_id_dict.get(topic[0])

            i += 1

        oneweek_trend_json = []
        i = 0
        for k in tmp_dict:
            if i >= 15:
                break
            subitem = {}
            subitem["text"] = k
            subitem["weight"] = round(tmp_dict[k], 2)
            subitem["ids"] = ','.join(str(e) for e in oneweek_id_dict.get(k))
            if len(subitem["ids"]) < 8:
                continue
            oneweek_trend_json.append(subitem)
            i += 1

        event_dict["oneweek"] = json.dumps(oneweek_trend_json)



        i = 0
        tmp_dict = {}
        tmp_id_dict = {}
        for topic in onemonth_trend:
            if i >= 300:
                break
            if len(tmp_dict) == 0:
                tmp_dict[topic[0]] = topic[1]
                tmp_id_dict[topic[0]] = onemonth_id_dict.get(topic[0])
            else:
                same_id = 0
                is_dup = False
                for exist_key in tmp_id_dict:
                    for id in onemonth_id_dict.get(topic[0]):
                        if id in tmp_id_dict[exist_key]:
                            same_id += 1
                    if same_id/len(onemonth_id_dict.get(topic[0])) >= 0.5:
                        is_dup = True
                        break
                    same_id = 0
                if is_dup == False:
                    tmp_dict[topic[0]] = topic[1]
                    tmp_id_dict[topic[0]] = onemonth_id_dict.get(topic[0])

            i += 1

        onemonth_trend_json = []
        i = 0
        for k in tmp_dict:
            if i >= 15:
                break
            subitem = {}
            subitem["text"] = k
            subitem["weight"] = round(tmp_dict[k], 2)
            subitem["ids"] = ','.join(str(e) for e in onemonth_id_dict.get(k))
            if len(subitem["ids"]) < 8:
                continue
            onemonth_trend_json.append(subitem)
            i += 1

        event_dict["onemonth"] = json.dumps(onemonth_trend_json)



        i = 0
        tmp_dict = {}
        tmp_id_dict = {}
        for topic in threemonths_trend:
            if i >= 300:
                break
            if len(tmp_dict) == 0:
                tmp_dict[topic[0]] = topic[1]
                tmp_id_dict[topic[0]] = threemonths_id_dict.get(topic[0])
            else:
                same_id = 0
                is_dup = False
                for exist_key in tmp_id_dict:
                    for id in threemonths_id_dict.get(topic[0]):
                        if id in tmp_id_dict[exist_key]:
                            same_id += 1
                    if same_id/len(threemonths_id_dict.get(topic[0])) >= 0.5:
                        is_dup = True
                        break
                    same_id = 0
                if is_dup == False:
                    tmp_dict[topic[0]] = topic[1]
                    tmp_id_dict[topic[0]] = threemonths_id_dict.get(topic[0])

            i += 1

        threemonths_trend_json = []
        i = 0
        for k in tmp_dict:
            if i >= 15:
                break
            subitem = {}
            subitem["text"] = k
            subitem["weight"] = round(tmp_dict[k], 2)
            subitem["ids"] = ','.join(str(e) for e in threemonths_id_dict.get(k))
            if len(subitem["ids"]) < 8:
                continue
            threemonths_trend_json.append(subitem)
            i += 1

        event_dict["threemonths"] = json.dumps(threemonths_trend_json)
        
        add_to_mysql()
        
    # add_to_mysql()
    tmp_headline_list = []
        
        
        


def extract_id(trend):
 
    # extract id
    pos1 = re.compile("ids")
    pos2 = re.compile("}, {")
    id_start = []
    id_end = []

    return_id = []
    for m in pos1.finditer(trend):
        id_start.append(m.end()+4)
    
    for m in pos2.finditer(trend):
        id_end.append(m.start()-1)
    for p1, p2 in zip(id_start, id_end):
        return_id.append(trend[p1:p2])
    # extract text
    pos1 = re.compile("text\": \"")
    pos2 = re.compile(", \"ids")

    text_start = []
    text_end = []

    return_text = []
    for m in pos1.finditer(trend):
        text_start.append(m.end())
    
    for m in pos2.finditer(trend):
        text_end.append(m.end()-6)
    rank = 1
    for p1, p2 in zip(text_start, text_end):
        tmp_rank = str(rank)
        tmp_str = trend[p1-9: p2] + ", \"rank\":" + tmp_rank
        return_text.append(tmp_str)
        rank += 1       

    return '[{' + '},{'.join(return_text) + '}]','[[' + '],['.join(return_id) + ']]'

def add_to_mysql():
        
    for period, trend in event_dict.items():
        trend_text, ids = extract_id(trend)
        if period == "sixhours":
            sixhours_trend_json = []
            data = {'trend': trend_text, 'period': period, 'ids': ids}
            crsr.execute(mysql_insert_trend, data)
            topic_id = crsr.lastrowid
            subitem = {}
            subitem["objects"] = trend_text
            subitem["period"] = period
            subitem["id"] = topic_id
            sixhours_trend_json.append(subitem)
            
            
        elif period == "twelvehours":
            twelvehours_trend_json = []
            data = {'trend': trend_text, 'period': period, 'ids': ids}
            crsr.execute(mysql_insert_trend, data)
            topic_id = crsr.lastrowid
            subitem = {}
            subitem["objects"] = trend_text
            subitem["period"] = period
            subitem["id"] = topic_id
            twelvehours_trend_json.append(subitem)
            
            

        elif period == "oneday":
            oneday_trend_json = []
            data = {'trend': trend_text, 'period': period, 'ids': ids}
            crsr.execute(mysql_insert_trend, data)
            topic_id = crsr.lastrowid
            subitem = {}
            subitem["objects"] = trend_text
            subitem["period"] = period
            subitem["id"] = topic_id
            oneday_trend_json.append(subitem)            
            

        elif period == "oneweek":

            oneweek_trend_json = []
            data = {'trend': trend_text, 'period': period, 'ids': ids}                
            crsr.execute(mysql_insert_trend, data)
            topic_id = crsr.lastrowid
            subitem = {}
            subitem["objects"] = trend_text
            subitem["period"] = period
            subitem["id"] = topic_id
            oneweek_trend_json.append(subitem)
            

        elif period == "onemonth":
            
            onemonth_trend_json = []
            data = {'trend': trend_text, 'period': period, 'ids': ids}                
            crsr.execute(mysql_insert_trend, data)
            topic_id = crsr.lastrowid
            subitem = {}
            subitem["objects"] = trend_text
            subitem["period"] = period
            subitem["id"] = topic_id
            onemonth_trend_json.append(subitem)
            

        elif period == "threemonths":
            
            threemonths_trend_json = []
            data = {'trend': trend_text, 'period': period, 'ids': ids}    
            
            
            crsr.execute(mysql_insert_trend, data)
            topic_id = crsr.lastrowid
            
            subitem = {}
            subitem["objects"] = trend_text
            subitem["period"] = period
            subitem["id"] = topic_id
            threemonths_trend_json.append(subitem)
               
    cnx.commit()
        

def add_new(*args, **kwargs):

    args_str = args.__str__()
    
    print("new string!!!!!")
    print(args_str)
    
    lower_args = args_str.lower()
    if "price analysis" not in lower_args and "price changed" not in lower_args and "\"category\":\"news\"" in lower_args and "Join us" not in lower_args and "market analysis" not in lower_args and "buy signal" not in headline[0] and "sell signal" not in headline[0]:
        tmp_headline_list.append(args_str)
        
        

# We can't subscribe until we've connected, so we use a callback handler
# to subscribe when able
def connect_handler(data):
    # print("enter connect_handler")
    # channel = pusher.subscribe('private-prices.BITFINEX_SPOT_BTC_USD')
    # channel.bind('App\\Events\\BroadcastPrices', my_func)
    
    channel_twitter = pusher.subscribe('private-headlines.twitter')
    channel_rss = pusher.subscribe('private-headlines.rss')
    channel_twitter.bind('App\\Events\\BroadcastHeadline', add_new)
    channel_rss.bind('App\\Events\\BroadcastHeadline', add_new)
    # channel = pusher.subscribe('api.news.topics.hashtag')
    # channel.bind('App\\Events\\BroadcastHeadlineAPI', my_func)
    '''
    except Exception as inst:
        with open("error.log", 'a') as outfile:
            print(type(inst))    # the exception instance
            print(inst.args)     # arguments stored in .args
            print(inst)  
            outfile.write(type(inst))
            outfile.write(inst.args)
            outfile.write(inst)
        outfile.close()
    '''


def one_time_import():
    init_dict()
    Now = datetime.datetime.now()

    for (line, time, ID, importance) in zip(sixhours_headline_list, sixhours_time_list, sixhours_ID_list, sixhours_importance_list):            
        topic_list, is_report = headline_cutting(line)
        if is_report == True:
            continue
        for i in range(len(topic_list)):
            words = topic_list[i].split()
            
            if len(words) == 1:
                enhance_weight = 1
                continue
            '''
            elif len(words) == 2:
                enhance_weight = 1
            else:
                enhance_weight = 1
            '''
            if importance == 3.0:
                enhance_weight = 1
            else:
                enhance_weight = 0.1

            # Add new topic in dictionary
            if sixhours_topic_dict.get(topic_list[i]) == None:
                sixhours_topic_dict[topic_list[i]] = enhance_weight * (1 - (Now - datetime.datetime.strptime(time, time_format)).seconds/21600)
            # Add weight
            else:
                sixhours_topic_dict[topic_list[i]] = sixhours_topic_dict.get(topic_list[i]) + enhance_weight * (1 - (Now - datetime.datetime.strptime(time, time_format)).seconds/21600)

            # Add new id in dictionary
            if sixhours_id_dict.get(topic_list[i]) == None:
                l = [ID]
                sixhours_id_dict[topic_list[i]] = l
            else:
                sixhours_id_dict[topic_list[i]].append(ID)

    for (line, time, ID, importance) in zip(twelvehours_headline_list, twelvehours_time_list, twelvehours_ID_list, twelvehours_importance_list):

        
        topic_list, is_report = headline_cutting(line)
        if is_report == True:
            continue
        for i in range(len(topic_list)):
            words = topic_list[i].split()
            
            if len(words) == 1:
                enhance_weight = 1
                continue
            '''
            elif len(words) == 2:
                enhance_weight = 1
            else:
                enhance_weight = 1
            '''
            if importance == 3.0:
                enhance_weight = 1
            else:
                enhance_weight = 0.1

            # Add new topic in dictionary
            if twelvehours_topic_dict.get(topic_list[i]) == None:
                twelvehours_topic_dict[topic_list[i]] = enhance_weight * (1 - (Now - datetime.datetime.strptime(time, time_format)).seconds/43200)
            # Add weight
            else:
                twelvehours_topic_dict[topic_list[i]] = twelvehours_topic_dict.get(topic_list[i]) + enhance_weight * (1 - (Now - datetime.datetime.strptime(time, time_format)).seconds/43200)

            # Add new id in dictionary
            if twelvehours_id_dict.get(topic_list[i]) == None:
                l = [ID]
                twelvehours_id_dict[topic_list[i]] = l
            else:
                twelvehours_id_dict[topic_list[i]].append(ID)  

    for (line, time, ID, importance) in zip(oneday_headline_list, oneday_time_list, oneday_ID_list, oneday_importance_list):
        
        topic_list, is_report = headline_cutting(line)
        if is_report == True:
            continue
        for i in range(len(topic_list)):
            words = topic_list[i].split()
            
            if len(words) == 1:
                enhance_weight = 1
                continue
            '''
            elif len(words) == 2:
                enhance_weight = 1
            else:
                enhance_weight = 1
            '''
            if importance == 3.0:
                enhance_weight = 1
            else:
                enhance_weight = 0.1

            # Add new topic in dictionary
            if oneday_topic_dict.get(topic_list[i]) == None:
                oneday_topic_dict[topic_list[i]] = enhance_weight * (1 - (Now - datetime.datetime.strptime(time, time_format)).seconds/86400)
            # Add weight
            else:
                oneday_topic_dict[topic_list[i]] = oneday_topic_dict.get(topic_list[i]) + enhance_weight * (1 - (Now - datetime.datetime.strptime(time, time_format)).seconds/86400)

            # Add new id in dictionary
            if oneday_id_dict.get(topic_list[i]) == None:
                l = [ID]
                oneday_id_dict[topic_list[i]] = l
            else:
                oneday_id_dict[topic_list[i]].append(ID)

    for (line, time, ID, importance) in zip(oneweek_headline_list, oneweek_time_list, oneweek_ID_list, oneweek_importance_list):
        
        topic_list, is_report = headline_cutting(line)
        if is_report == True:
            continue
        for i in range(len(topic_list)):
            words = topic_list[i].split()
            
            if len(words) == 1:
                enhance_weight = 1
                continue
            '''
            elif len(words) == 2:
                enhance_weight = 1
            else:
                enhance_weight = 1
            '''
            if importance == 3.0:
                enhance_weight = 1
            else:
                enhance_weight = 0.1

            # Add new topic in dictionary
            if oneweek_topic_dict.get(topic_list[i]) == None:
                oneweek_topic_dict[topic_list[i]] = enhance_weight * (1 - ((Now - datetime.datetime.strptime(time, time_format)).seconds + (Now - datetime.datetime.strptime(time, time_format)).days * 86400)/604800)
            # Add weight
            else:
                oneweek_topic_dict[topic_list[i]] = oneweek_topic_dict.get(topic_list[i]) + enhance_weight * (1 - ((Now - datetime.datetime.strptime(time, time_format)).seconds + (Now - datetime.datetime.strptime(time, time_format)).days * 86400)/604800)

            # Add new id in dictionary
            if oneweek_id_dict.get(topic_list[i]) == None:
                l = [ID]
                oneweek_id_dict[topic_list[i]] = l
            else:
                oneweek_id_dict[topic_list[i]].append(ID)

    for (line, time, ID, importance) in zip(onemonth_headline_list, onemonth_time_list, onemonth_ID_list, onemonth_importance_list):
        topic_list, is_report = headline_cutting(line)
        if is_report == True:
            continue
        for i in range(len(topic_list)):
            words = topic_list[i].split()
            
            if len(words) == 1:
                enhance_weight = 1
                continue
            '''
            elif len(words) == 2:
                enhance_weight = 1
            else:
                enhance_weight = 1
            '''
            if importance == 3.0:
                enhance_weight = 1
            else:
                enhance_weight = 0.1
            
            
            # Add new topic in dictionary
            if onemonth_topic_dict.get(topic_list[i]) == None:
                onemonth_topic_dict[topic_list[i]] = enhance_weight * (1 - ((Now - datetime.datetime.strptime(time, time_format)).seconds + (Now - datetime.datetime.strptime(time, time_format)).days * 86400)/2592000)
            # Add weight
            else:
                onemonth_topic_dict[topic_list[i]] = onemonth_topic_dict.get(topic_list[i]) + enhance_weight * (1 - ((Now - datetime.datetime.strptime(time, time_format)).seconds + (Now - datetime.datetime.strptime(time, time_format)).days * 86400)/2592000)
            
            # Add new id in dictionary
            if onemonth_id_dict.get(topic_list[i]) == None:
                l = [ID]
                onemonth_id_dict[topic_list[i]] = l
            else:
                onemonth_id_dict[topic_list[i]].append(ID)

    
    for (line, time, ID, importance) in zip(threemonths_headline_list, threemonths_time_list, threemonths_ID_list, threemonths_importance_list):

        topic_list, is_report = headline_cutting(line)
        if is_report == True:
            continue
        for i in range(len(topic_list)):
            words = topic_list[i].split()
            
            if len(words) == 1:
                enhance_weight = 1
                continue
            '''
            elif len(words) == 2:
                enhance_weight = 1
            else:
                enhance_weight = 1
            '''
            if importance == 3.0:
                enhance_weight = 1
            else:
                enhance_weight = 0.1
            
            # Add new topic in dictionary
            if threemonths_topic_dict.get(topic_list[i]) == None:
                threemonths_topic_dict[topic_list[i]] = enhance_weight * (1 - ((Now - datetime.datetime.strptime(time, time_format)).seconds + (Now - datetime.datetime.strptime(time, time_format)).days * 86400)/7776000)
            # Add weight
            else:
                threemonths_topic_dict[topic_list[i]] = threemonths_topic_dict.get(topic_list[i]) + enhance_weight * (1 - ((Now - datetime.datetime.strptime(time, time_format)).seconds + (Now - datetime.datetime.strptime(time, time_format)).days * 86400)/7776000)
    
            # Add new id in dictionary
            if threemonths_id_dict.get(topic_list[i]) == None:
                l = [ID]
                threemonths_id_dict[topic_list[i]] = l
            else:
                threemonths_id_dict[topic_list[i]].append(ID)


    sixhours_trend = sorted(sixhours_topic_dict.items(), key = lambda x:x[1], reverse = True)    
    
    sixhours_trend_json = json.dumps(dict(sixhours_trend[0:15]))


    twelvehours_trend = sorted(twelvehours_topic_dict.items(), key = lambda x:x[1], reverse = True)

    twelvehours_trend_json = json.dumps(dict(twelvehours_trend[0:15]))


    oneday_trend = sorted(oneday_topic_dict.items(), key = lambda x:x[1], reverse = True)

    oneday_trend_json = json.dumps(dict(oneday_trend[0:15]))



    oneweek_trend = sorted(oneweek_topic_dict.items(), key = lambda x:x[1], reverse = True)

    oneweek_trend_json = json.dumps(dict(oneweek_trend[0:15]))


    onemonth_trend = sorted(onemonth_topic_dict.items(), key = lambda x:x[1], reverse = True)

    onemonth_trend_json = json.dumps(dict(onemonth_trend[0:15]))
    

    threemonths_trend = sorted(threemonths_topic_dict.items(), key = lambda x:x[1], reverse = True)

    threemonths_trend_json = json.dumps(dict(threemonths_trend[0:15]))


    

    sixhours_trend_json = []
    for k in sixhours_trend[0:15]:
        subitem = {}
        subitem["text"] = k[0]
        subitem["weight"] = round(k[1], 2)
        subitem["ids"] = ','.join(str(e) for e in sixhours_id_dict.get(k[0]))
        if len(subitem["ids"]) < 8:
            continue
        sixhours_trend_json.append(subitem)
        # sixhours_trend_json.append(json.dumps(subitem))

    twelvehours_trend_json = []
    for k in twelvehours_trend[0:15] :
        subitem = {}
        subitem["text"] = k[0]
        subitem["weight"] = round(k[1], 2)
        subitem["ids"] = ','.join(str(e) for e in twelvehours_id_dict.get(k[0]))
        if len(subitem["ids"]) < 8:
            continue
        twelvehours_trend_json.append(subitem)
        # twelvehours_trend_json.append(json.dumps(subitem))

    oneday_trend_json = []
    for k in oneday_trend[0:15] :
        subitem = {}
        subitem["text"] = k[0]
        subitem["weight"] = round(k[1], 2)
        subitem["ids"] = ','.join(str(e) for e in oneday_id_dict.get(k[0]))
        if len(subitem["ids"]) < 8:
            continue
        oneday_trend_json.append(subitem)
        # oneday_trend_json.append(json.dumps(subitem))

    oneweek_trend_json = []
    for k in oneweek_trend[0:15] :
        subitem = {}
        subitem["text"] = k[0]
        subitem["weight"] = round(k[1], 2)
        subitem["ids"] = ','.join(str(e) for e in oneweek_id_dict.get(k[0]))
        if len(subitem["ids"]) < 8:
            continue
        oneweek_trend_json.append(subitem)
        # oneweek_trend_json.append(json.dumps(subitem))
    
    onemonth_trend_json = []
    for k in onemonth_trend[0:15] :
        subitem = {}
        subitem["text"] = k[0]
        subitem["weight"] = round(k[1], 2)
        subitem["ids"] = ','.join(str(e) for e in onemonth_id_dict.get(k[0]))
        if len(subitem["ids"]) < 8:
            continue
        onemonth_trend_json.append(subitem)
        # onemonth_trend_json.append(json.dumps(subitem))

    threemonths_trend_json = []
    for k in threemonths_trend[0:15] :
        subitem = {}
        subitem["text"] = k[0]
        subitem["weight"] = round(k[1], 2)
        subitem["ids"] = ','.join(str(e) for e in threemonths_id_dict.get(k[0]))
        if len(subitem["ids"]) < 8:
            continue
        threemonths_trend_json.append(subitem)
        # threemonths_trend_json.append(json.dumps(subitem))
    event_dict["sixhours"] = json.dumps(sixhours_trend_json)
    event_dict["twelvehours"] = json.dumps(twelvehours_trend_json)
    event_dict["oneday"] = json.dumps(oneday_trend_json)
    event_dict["oneweek"] = json.dumps(oneweek_trend_json)
    event_dict["onemonth"] = json.dumps(onemonth_trend_json)
    event_dict["threemonths"] = json.dumps(threemonths_trend_json)


    add_to_mysql()
    


one_time_import()
pusher = pysher.Pusher("25d8d236bc7237b8c5d6", cluster='us2', secret="826a351f3e62e24152ee", )
# contents = urllib.request.urlopen("https:beta.terminal.io/api/v1/oauth/authenticate").read()
# r = requests.post("https://beta.cryptoterminal.io/api/v1/broadcast/auth?channel_name=headline", headers={"Accept":"application/json", "Authorization":"Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiIsImp0aSI6ImQzZmRjOWU0NGU1N2JlMTZkOTRjN2RhMGFlMjQyNGE2N2UyY2YzNmI3ZTBhMmE4OGRmZTM0ZTg2MTNmMGIxNDFmMzcyNWJhZTljMjgzMzM3In0.eyJhdWQiOiIzIiwianRpIjoiZDNmZGM5ZTQ0ZTU3YmUxNmQ5NGM3ZGEwYWUyNDI0YTY3ZTJjZjM2YjdlMGEyYTg4ZGZlMzRlODYxM2YwYjE0MWYzNzI1YmFlOWMyODMzMzciLCJpYXQiOjE1NDIzMTYzMjIsIm5iZiI6MTU0MjMxNjMyMiwiZXhwIjoxNTczODUyMzIyLCJzdWIiOiI4OCIsInNjb3BlcyI6W119.fAPGi60UQsVtvDQ1Y-K9Nsol7F1bJtdpXuZWYGG3nQ5YtGqVx0GlPLWI0fPKxLPmT6L54CM5458c5LiDSqxzuJj2N4_TZBwQGOec2L09dus5R0Gk_vaIAVLZWNVcJdWql7_3kj2LnffsSGLB7Be-eXXAnxkzztjJPQr3GDtFx-v3Axe3pUoQZIrcKDriY0ureiNre_HJPzLyXzggWkXZa-3Hpd-W_Al93moYMYmn260yuz-epRyQDC3WADGi1Bi_aGea9JUtRxpjUnimMvz2VxiL4Z1NhaoM-OLAPCm6FwesPTUDGOJ_IeaRTGMFXV6W5eybK_BHsN28NVRUDbXlJPfsZNzhovYjYDVHCnXH7b53hq3Zx8gELUGT2POBAMhPNBPFxEjXG20btfflU8x8734lSOkvotzZajnfCUh3atSuskau2olV1nL1GztViOOtGxe3nfH8Xl3TeX6xpUsrG74Lv5MV7OyeYqkHLwVf2Mq4XmWLegWXrE-OE6XUhqELY79wCYXqpqt12P-iqsELXW1r-A0iDdn4RQGCOMIQO4MrUJwyT-4j4FwzWOsFaIhsUKzvhWSKHauH0SYDr8FZHUKr7H66XrThhGU2UDWq9fjfBF9mLLoDC-00NvTjH_ZaN16245K85Mf71qfNcl4GqegRsIa2K2FtT2UC_Ij_t28"})
pusher.connection.bind('pusher:connection_established', connect_handler)
pusher.connect()

push = Pusher("551871", "25d8d236bc7237b8c5d6", "826a351f3e62e24152ee", cluster="us2")

def push_json():
    for key, value in event_dict_plusID.items():
        if value:
                
            print("push:")
            print("=========================================")
            print("value is:")
            print(value)
            print("=========================================")
            
            push.trigger(channel, "App\\Events\\"+key, value[1:-1])
            
        else:
            print("{} is empty ".format(key))
        
    




while 1==1:    

    #two times, 1 for push 1 for update

    PUSH_END_TIME = timer()
    UPDATE_END_TIME = timer()


    if PUSH_END_TIME - PUSH_START_TIME >= 620:
        push_json()
        PUSH_START_TIME = timer()

    
    if UPDATE_END_TIME - UPDATE_START_TIME >= DECAY_SPEED:
        decay()
        UPDATE_START_TIME = timer()
    
    # time.sleep(SLEEP_TIME)
    continue
