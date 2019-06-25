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

TWELVEHOURS_KEEP_TIME = 43200
ONEDAY_KEEP_TIME = 86400
ONEWEEK_KEEP_TIME = 604800
ONEMONTH_KEEP_TIME = 2592000
THREEMONTHS_KEEP_TIME = 2592000 * 3

DECAY_SPEED = 600
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

BTC_twelvehours_headline_list = []
BTC_twelvehours_time_list = []
BTC_twelvehours_ID_list =[]
BTC_twelvehours_importance_list =[]
BTC_oneday_headline_list = []
BTC_oneday_time_list = []
BTC_oneday_ID_list = []
BTC_oneday_importance_list = []
BTC_oneweek_headline_list = []
BTC_oneweek_time_list = []
BTC_oneweek_ID_list = []
BTC_oneweek_importance_list = []
BTC_onemonth_headline_list = []
BTC_onemonth_time_list = []
BTC_onemonth_ID_list =[]
BTC_onemonth_importance_list =[]
BTC_threemonths_headline_list = []
BTC_threemonths_time_list = []
BTC_threemonths_ID_list = []
BTC_threemonths_importance_list = []


ETH_twelvehours_headline_list = []
ETH_twelvehours_time_list = []
ETH_twelvehours_ID_list =[]
ETH_twelvehours_importance_list =[]
ETH_oneday_headline_list = []
ETH_oneday_time_list = []
ETH_oneday_ID_list = []
ETH_oneday_importance_list = []
ETH_oneweek_headline_list = []
ETH_oneweek_time_list = []
ETH_oneweek_ID_list = []
ETH_oneweek_importance_list = []
ETH_onemonth_headline_list = []
ETH_onemonth_time_list = []
ETH_onemonth_ID_list =[]
ETH_onemonth_importance_list =[]
ETH_threemonths_headline_list = []
ETH_threemonths_time_list = []
ETH_threemonths_ID_list = []
ETH_threemonths_importance_list = []


XRP_twelvehours_headline_list = []
XRP_twelvehours_time_list = []
XRP_twelvehours_ID_list =[]
XRP_twelvehours_importance_list =[]
XRP_oneday_headline_list = []
XRP_oneday_time_list = []
XRP_oneday_ID_list = []
XRP_oneday_importance_list = []
XRP_oneweek_headline_list = []
XRP_oneweek_time_list = []
XRP_oneweek_ID_list = []
XRP_oneweek_importance_list = []
XRP_onemonth_headline_list = []
XRP_onemonth_time_list = []
XRP_onemonth_ID_list =[]
XRP_onemonth_importance_list =[]
XRP_threemonths_headline_list = []
XRP_threemonths_time_list = []
XRP_threemonths_ID_list = []
XRP_threemonths_importance_list = []


BCH_twelvehours_headline_list = []
BCH_twelvehours_time_list = []
BCH_twelvehours_ID_list =[]
BCH_twelvehours_importance_list =[]
BCH_oneday_headline_list = []
BCH_oneday_time_list = []
BCH_oneday_ID_list = []
BCH_oneday_importance_list = []
BCH_oneweek_headline_list = []
BCH_oneweek_time_list = []
BCH_oneweek_ID_list = []
BCH_oneweek_importance_list = []
BCH_onemonth_headline_list = []
BCH_onemonth_time_list = []
BCH_onemonth_ID_list =[]
BCH_onemonth_importance_list =[]
BCH_threemonths_headline_list = []
BCH_threemonths_time_list = []
BCH_threemonths_ID_list = []
BCH_threemonths_importance_list = []


LTC_twelvehours_headline_list = []
LTC_twelvehours_time_list = []
LTC_twelvehours_ID_list =[]
LTC_twelvehours_importance_list =[]
LTC_oneday_headline_list = []
LTC_oneday_time_list = []
LTC_oneday_ID_list = []
LTC_oneday_importance_list = []
LTC_oneweek_headline_list = []
LTC_oneweek_time_list = []
LTC_oneweek_ID_list = []
LTC_oneweek_importance_list = []
LTC_onemonth_headline_list = []
LTC_onemonth_time_list = []
LTC_onemonth_ID_list =[]
LTC_onemonth_importance_list =[]
LTC_threemonths_headline_list = []
LTC_threemonths_time_list = []
LTC_threemonths_ID_list = []
LTC_threemonths_importance_list = []

# For now, importance logic not used
# importance_list = []

BTC_twelvehours_topic_dict = {}
BTC_oneday_topic_dict = {}
BTC_oneweek_topic_dict = {}
BTC_onemonth_topic_dict = {}
BTC_threemonths_topic_dict = {}

BTC_twelvehours_id_dict = {}
BTC_oneday_id_dict = {}
BTC_oneweek_id_dict = {}
BTC_onemonth_id_dict = {}
BTC_threemonths_id_dict = {}


ETH_twelvehours_topic_dict = {}
ETH_oneday_topic_dict = {}
ETH_oneweek_topic_dict = {}
ETH_onemonth_topic_dict = {}
ETH_threemonths_topic_dict = {}

ETH_twelvehours_id_dict = {}
ETH_oneday_id_dict = {}
ETH_oneweek_id_dict = {}
ETH_onemonth_id_dict = {}
ETH_threemonths_id_dict = {}


XRP_twelvehours_topic_dict = {}
XRP_oneday_topic_dict = {}
XRP_oneweek_topic_dict = {}
XRP_onemonth_topic_dict = {}
XRP_threemonths_topic_dict = {}

XRP_twelvehours_id_dict = {}
XRP_oneday_id_dict = {}
XRP_oneweek_id_dict = {}
XRP_onemonth_id_dict = {}
XRP_threemonths_id_dict = {}


BCH_twelvehours_topic_dict = {}
BCH_oneday_topic_dict = {}
BCH_oneweek_topic_dict = {}
BCH_onemonth_topic_dict = {}
BCH_threemonths_topic_dict = {}

BCH_twelvehours_id_dict = {}
BCH_oneday_id_dict = {}
BCH_oneweek_id_dict = {}
BCH_onemonth_id_dict = {}
BCH_threemonths_id_dict = {}


LTC_twelvehours_topic_dict = {}
LTC_oneday_topic_dict = {}
LTC_oneweek_topic_dict = {}
LTC_onemonth_topic_dict = {}
LTC_threemonths_topic_dict = {}

LTC_twelvehours_id_dict = {}
LTC_oneday_id_dict = {}
LTC_oneweek_id_dict = {}
LTC_onemonth_id_dict = {}
LTC_threemonths_id_dict = {}

# store new headlines
BTC_tmp_headline_list = []
ETH_tmp_headline_list = []
XRP_tmp_headline_list = []
BCH_tmp_headline_list = []
LTC_tmp_headline_list = []

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
channel_BTC = "private-trends.BTC"
channel_ETH = "private-trends.ETH"
channel_XRP = "private-trends.ETH"
channel_BCH = "private-trends.ETH"
channel_LTC = "private-trends.ETH"
event = "hours"


SLEEP_TIME = 2
PUSH_START_TIME = timer()
UPDATE_START_TIME = timer()
twelvehours_trend_json = ""
oneday_trend_json = ""
oneweek_trend_json = ""
threemonths_trend_json = ""
onemonth_trend_json = ""

BTC_event_dict = {"twelvehours": twelvehours_trend_json, "oneday": oneday_trend_json, "oneweek": oneweek_trend_json, "onemonth": onemonth_trend_json, "threemonths": threemonths_trend_json}

BTC_event_dict_plusID = {"twelvehours": twelvehours_trend_json, "oneday": oneday_trend_json, "oneweek": oneweek_trend_json, "onemonth": onemonth_trend_json, "threemonths": threemonths_trend_json}

ETH_event_dict = {"twelvehours": twelvehours_trend_json, "oneday": oneday_trend_json, "oneweek": oneweek_trend_json, "onemonth": onemonth_trend_json, "threemonths": threemonths_trend_json}

ETH_event_dict_plusID = {"twelvehours": twelvehours_trend_json, "oneday": oneday_trend_json, "oneweek": oneweek_trend_json, "onemonth": onemonth_trend_json, "threemonths": threemonths_trend_json}

XRP_event_dict = {"twelvehours": twelvehours_trend_json, "oneday": oneday_trend_json, "oneweek": oneweek_trend_json, "onemonth": onemonth_trend_json, "threemonths": threemonths_trend_json}

XRP_event_dict_plusID = {"twelvehours": twelvehours_trend_json, "oneday": oneday_trend_json, "oneweek": oneweek_trend_json, "onemonth": onemonth_trend_json, "threemonths": threemonths_trend_json}

BCH_event_dict = {"twelvehours": twelvehours_trend_json, "oneday": oneday_trend_json, "oneweek": oneweek_trend_json, "onemonth": onemonth_trend_json, "threemonths": threemonths_trend_json}

BCH_event_dict_plusID = {"twelvehours": twelvehours_trend_json, "oneday": oneday_trend_json, "oneweek": oneweek_trend_json, "onemonth": onemonth_trend_json, "threemonths": threemonths_trend_json}

LTC_event_dict = {"twelvehours": twelvehours_trend_json, "oneday": oneday_trend_json, "oneweek": oneweek_trend_json, "onemonth": onemonth_trend_json, "threemonths": threemonths_trend_json}

LTC_event_dict_plusID = {"twelvehours": twelvehours_trend_json, "oneday": oneday_trend_json, "oneweek": oneweek_trend_json, "onemonth": onemonth_trend_json, "threemonths": threemonths_trend_json}


def init_dict():
    Now = datetime.datetime.now()
    # new: read from DB
    
    # get twelvehours
    twelvehours_before = Now + datetime.timedelta(hours=-12)
    str_twelvehours_before = twelvehours_before.strftime(time_format)
    crsr.execute("select text,created_at,id,rating3,subtopic from headlines where author != 'Crypto Terminal AI' and author != 'Icobrothers' and ((topic != 'price_action' and topic != 'hashtag' and topic != 'price action') or topic is null) and created_at > '%s'"%str_twelvehours_before)
    twelvehours_list = crsr.fetchall()
    for headline in twelvehours_list:
        if "Price Analysis" in headline[0] or "Join us" in headline[0] or "Market Analysis" in headline[0] or headline[3] == 0 or headline[3] == -1 or "buy signal" in headline[0] or "sell signal" in headline[0]:
            continue
        if headline[4] is not None:
            if "BTC" in headline[4]:
                created_at = headline[1]
                t = created_at.strftime(time_format)
                BTC_twelvehours_headline_list.append(headline[0])
                BTC_twelvehours_time_list.append(t)
                BTC_twelvehours_ID_list.append(headline[2])
                BTC_twelvehours_importance_list.append(headline[3])
            if "ETH" in headline[4]:
                created_at = headline[1]
                t = created_at.strftime(time_format)
                ETH_twelvehours_headline_list.append(headline[0])
                ETH_twelvehours_time_list.append(t)
                ETH_twelvehours_ID_list.append(headline[2])
                ETH_twelvehours_importance_list.append(headline[3])
            if "XRP" in headline[4]:
                created_at = headline[1]
                t = created_at.strftime(time_format)
                XRP_twelvehours_headline_list.append(headline[0])
                XRP_twelvehours_time_list.append(t)
                XRP_twelvehours_ID_list.append(headline[2])
                XRP_twelvehours_importance_list.append(headline[3])
            if "BCH" in headline[4]:
                created_at = headline[1]
                t = created_at.strftime(time_format)
                BCH_twelvehours_headline_list.append(headline[0])
                BCH_twelvehours_time_list.append(t)
                BCH_twelvehours_ID_list.append(headline[2])
                BCH_twelvehours_importance_list.append(headline[3])
            if "LTC" in headline[4]:
                created_at = headline[1]
                t = created_at.strftime(time_format)
                LTC_twelvehours_headline_list.append(headline[0])
                LTC_twelvehours_time_list.append(t)
                LTC_twelvehours_ID_list.append(headline[2])
                LTC_twelvehours_importance_list.append(headline[3])
        
    # get oneday
    oneday_before = Now + datetime.timedelta(days=-1)
    str_oneday_before = oneday_before.strftime(time_format)
    crsr.execute("select text,created_at,id,rating3,subtopic from headlines where author != 'Crypto Terminal AI' and author != 'Icobrothers' and ((topic != 'price_action' and topic != 'hashtag' and topic != 'price action') or topic is null) and created_at > '%s'"%str_oneday_before)
    oneday_list = crsr.fetchall()
    for headline in oneday_list:
        if "Price Analysis" in headline[0] or "Join us" in headline[0] or "Market Analysis" in headline[0] or headline[3] == 0 or headline[3] == -1 or "buy signal" in headline[0] or "sell signal" in headline[0]:
            continue
        if headline[4] is not None:
            if "BTC" in headline[4]:
                created_at = headline[1]
                t = created_at.strftime(time_format)
                BTC_oneday_headline_list.append(headline[0])
                BTC_oneday_time_list.append(t)
                BTC_oneday_ID_list.append(headline[2])
                BTC_oneday_importance_list.append(headline[3])
            if "ETH" in headline[4]:
                created_at = headline[1]
                t = created_at.strftime(time_format)
                ETH_oneday_headline_list.append(headline[0])
                ETH_oneday_time_list.append(t)
                ETH_oneday_ID_list.append(headline[2])
                ETH_oneday_importance_list.append(headline[3])
            if "XRP" in headline[4]:
                created_at = headline[1]
                t = created_at.strftime(time_format)
                XRP_oneday_headline_list.append(headline[0])
                XRP_oneday_time_list.append(t)
                XRP_oneday_ID_list.append(headline[2])
                XRP_oneday_importance_list.append(headline[3])
            if "BCH" in headline[4]:
                created_at = headline[1]
                t = created_at.strftime(time_format)
                BCH_oneday_headline_list.append(headline[0])
                BCH_oneday_time_list.append(t)
                BCH_oneday_ID_list.append(headline[2])
                BCH_oneday_importance_list.append(headline[3])
            if "LTC" in headline[4]:
                created_at = headline[1]
                t = created_at.strftime(time_format)
                LTC_oneday_headline_list.append(headline[0])
                LTC_oneday_time_list.append(t)
                LTC_oneday_ID_list.append(headline[2])
                LTC_oneday_importance_list.append(headline[3])

    # get oneweek
    oneweek_before = Now + datetime.timedelta(days=-7)
    str_oneweek_before = oneweek_before.strftime(time_format)
    crsr.execute("select text,created_at,id,rating3,subtopic from headlines where author != 'Crypto Terminal AI' and author != 'Icobrothers' and ((topic != 'price_action' and topic != 'hashtag' and topic != 'price action') or topic is null) and created_at > '%s'"%str_oneweek_before)
    oneweek_list = crsr.fetchall()

    for headline in oneweek_list:
        if "Price Analysis" in headline[0] or "Join us" in headline[0] or "Market Analysis" in headline[0] or headline[3] == 0 or headline[3] == -1 or "buy signal" in headline[0] or "sell signal" in headline[0]:
            continue
        if headline[4] is not None:
            if "BTC" in headline[4]:
                created_at = headline[1]
                t = created_at.strftime(time_format)
                BTC_oneweek_headline_list.append(headline[0])
                BTC_oneweek_time_list.append(t)
                BTC_oneweek_ID_list.append(headline[2])
                BTC_oneweek_importance_list.append(headline[3])
            if "ETH" in headline[4]:
                created_at = headline[1]
                t = created_at.strftime(time_format)
                ETH_oneweek_headline_list.append(headline[0])
                ETH_oneweek_time_list.append(t)
                ETH_oneweek_ID_list.append(headline[2])
                ETH_oneweek_importance_list.append(headline[3])
            if "XRP" in headline[4]:
                created_at = headline[1]
                t = created_at.strftime(time_format)
                XRP_oneweek_headline_list.append(headline[0])
                XRP_oneweek_time_list.append(t)
                XRP_oneweek_ID_list.append(headline[2])
                XRP_oneweek_importance_list.append(headline[3])
            if "BCH" in headline[4]:
                created_at = headline[1]
                t = created_at.strftime(time_format)
                BCH_oneweek_headline_list.append(headline[0])
                BCH_oneweek_time_list.append(t)
                BCH_oneweek_ID_list.append(headline[2])
                BCH_oneweek_importance_list.append(headline[3])
            if "LTC" in headline[4]:
                created_at = headline[1]
                t = created_at.strftime(time_format)
                LTC_oneweek_headline_list.append(headline[0])
                LTC_oneweek_time_list.append(t)
                LTC_oneweek_ID_list.append(headline[2])
                LTC_oneweek_importance_list.append(headline[3])
    # get onemonth
    onemonth_before = Now + datetime.timedelta(days=-30)

    str_onemonth_before = onemonth_before.strftime(time_format)


    command = "select text,created_at,id,rating3,subtopic from headlines where author != 'Crypto Terminal AI' and author != 'Icobrothers' and ((topic != 'price_action' and topic != 'hashtag' and topic != 'price action') or topic is null) and created_at > '" + str_onemonth_before + "' union select text,created_at,id,rating3,subtopic from headline_archives where author != 'Crypto Terminal AI' and author != 'Icobrothers' and ((topic != 'price_action' and topic != 'hashtag' and topic != 'price action') or topic is null) and created_at > '" + str_onemonth_before + "'"

    print(command)
    crsr.execute(command)
    onemonth_list = crsr.fetchall()
    for headline in onemonth_list:
        if "Price Analysis" in headline[0] or "Join us" in headline[0] or "Market Analysis" in headline[0] or headline[3] == 0 or headline[3] == -1 or "buy signal" in headline[0] or "sell signal" in headline[0]:
            continue
        if headline[4] is not None:
            if "BTC" in headline[4]:
                created_at = headline[1]
                t = created_at.strftime(time_format)
                BTC_onemonth_headline_list.append(headline[0])
                BTC_onemonth_time_list.append(t)
                BTC_onemonth_ID_list.append(headline[2])
                BTC_onemonth_importance_list.append(headline[3])
            if "ETH" in headline[4]:
                created_at = headline[1]
                t = created_at.strftime(time_format)
                ETH_onemonth_headline_list.append(headline[0])
                ETH_onemonth_time_list.append(t)
                ETH_onemonth_ID_list.append(headline[2])
                ETH_onemonth_importance_list.append(headline[3])
            if "XRP" in headline[4]:
                created_at = headline[1]
                t = created_at.strftime(time_format)
                XRP_onemonth_headline_list.append(headline[0])
                XRP_onemonth_time_list.append(t)
                XRP_onemonth_ID_list.append(headline[2])
                XRP_onemonth_importance_list.append(headline[3])
            if "BCH" in headline[4]:
                created_at = headline[1]
                t = created_at.strftime(time_format)
                BCH_onemonth_headline_list.append(headline[0])
                BCH_onemonth_time_list.append(t)
                BCH_onemonth_ID_list.append(headline[2])
                BCH_onemonth_importance_list.append(headline[3])
            if "LTC" in headline[4]:
                created_at = headline[1]
                t = created_at.strftime(time_format)
                LTC_onemonth_headline_list.append(headline[0])
                LTC_onemonth_time_list.append(t)
                LTC_onemonth_ID_list.append(headline[2])
                LTC_onemonth_importance_list.append(headline[3])

    # get threemonths
    threemonths_before = Now + datetime.timedelta(days=-90)
    str_threemonths_before = threemonths_before.strftime(time_format)
    crsr.execute("select text,created_at,id,rating3,subtopic from headlines where author != 'Crypto Terminal AI' and author != 'Icobrothers' and ((topic != 'price_action' and topic != 'hashtag' and topic != 'price action') or topic is null) and created_at > '" + str_threemonths_before + "' union select text,created_at,id,rating3,subtopic from headline_archives where author != 'Crypto Terminal AI' and author != 'Icobrothers' and ((topic != 'price_action' and topic != 'hashtag' and topic != 'price action') or topic is null) and created_at > '" + str_threemonths_before + "'")
    threemonths_list = crsr.fetchall()
    for headline in threemonths_list:
        if "Price Analysis" in headline[0] or "Join us" in headline[0] or "Market Analysis" in headline[0] or headline[3] == 0 or headline[3] == -1 or "buy signal" in headline[0] or "sell signal" in headline[0]:
            continue
        if headline[4] is not None:
            if "BTC" in headline[4]:
                created_at = headline[1]
                t = created_at.strftime(time_format)
                BTC_threemonths_headline_list.append(headline[0])
                BTC_threemonths_time_list.append(t)
                BTC_threemonths_ID_list.append(headline[2])
                BTC_threemonths_importance_list.append(headline[3])
            if "ETH" in headline[4]:
                created_at = headline[1]
                t = created_at.strftime(time_format)
                ETH_threemonths_headline_list.append(headline[0])
                ETH_threemonths_time_list.append(t)
                ETH_threemonths_ID_list.append(headline[2])
                ETH_threemonths_importance_list.append(headline[3])
            if "XRP" in headline[4]:
                created_at = headline[1]
                t = created_at.strftime(time_format)
                XRP_threemonths_headline_list.append(headline[0])
                XRP_threemonths_time_list.append(t)
                XRP_threemonths_ID_list.append(headline[2])
                XRP_threemonths_importance_list.append(headline[3])
            if "BCH" in headline[4]:
                created_at = headline[1]
                t = created_at.strftime(time_format)
                BCH_threemonths_headline_list.append(headline[0])
                BCH_threemonths_time_list.append(t)
                BCH_threemonths_ID_list.append(headline[2])
                BCH_threemonths_importance_list.append(headline[3])
            if "LTC" in headline[4]:
                created_at = headline[1]
                t = created_at.strftime(time_format)
                LTC_threemonths_headline_list.append(headline[0])
                LTC_threemonths_time_list.append(t)
                LTC_threemonths_ID_list.append(headline[2])
                LTC_threemonths_importance_list.append(headline[3])
        


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
    twelvehours_decay_speed = (DECAY_SPEED)/TWELVEHOURS_KEEP_TIME
    delete_list = []
    for key in BTC_twelvehours_topic_dict:
        BTC_twelvehours_topic_dict[key] = BTC_twelvehours_topic_dict[key] * (1 - twelvehours_decay_speed)
        BTC_twelvehours_topic_dict[key] -= TWELVEHOURS_DECAY_SPEED_TUNE
        if BTC_twelvehours_topic_dict[key] <= 0:
            delete_list.append(key)
    for l in delete_list:
        BTC_twelvehours_topic_dict.pop(l)
        BTC_twelvehours_id_dict.pop(l)
    # clean lists
    delete_time_list = []
    for t in BTC_twelvehours_time_list:
        if (((Now - datetime.datetime.strptime(t, time_format)).seconds) + ((Now - datetime.datetime.strptime(t, time_format)).days * 86400)) >= TWELVEHOURS_KEEP_TIME:
            delete_time_list.append(t)
    for t in delete_time_list:
        pos = BTC_twelvehours_time_list.index(t)
        headline_id = BTC_twelvehours_ID_list[pos]
        BTC_twelvehours_time_list.pop(pos)
        BTC_twelvehours_ID_list.pop(pos)
        BTC_twelvehours_headline_list.pop(pos)
        BTC_twelvehours_importance_list.pop(pos)
        for items in BTC_twelvehours_id_dict.values():
            if headline_id in items:
                items.remove(headline_id)



    twelvehours_trend = sorted(BTC_twelvehours_topic_dict.items(), key = lambda x:x[1], reverse = True)


    i = 0
    tmp_dict = {}
    tmp_id_dict = {}
    for topic in twelvehours_trend:
        if i >= 500:
            break
        if len(tmp_dict) == 0:
            tmp_dict[topic[0]] = topic[1]
            tmp_id_dict[topic[0]] = BTC_twelvehours_id_dict.get(topic[0])
        else:
            same_id = 0
            is_dup = False
            for exist_key in tmp_id_dict:
                if len(BTC_twelvehours_id_dict.get(topic[0])) != 0:
                    for id in BTC_twelvehours_id_dict.get(topic[0]):

                        if id in tmp_id_dict[exist_key]:
                            same_id += 1
                    if same_id/len(BTC_twelvehours_id_dict.get(topic[0])) >= 0.5:
                        is_dup = True
                        break
                same_id = 0
            if is_dup == False:
                tmp_dict[topic[0]] = topic[1]
                tmp_id_dict[topic[0]] = BTC_twelvehours_id_dict.get(topic[0])


        i += 1



    twelvehours_trend_json = []
    i = 0

    for k in tmp_dict:
        if i >= 15:
            break
        
        subitem = {}
        subitem["text"] = k
        subitem["weight"] = round(tmp_dict[k], 2)
        subitem["ids"] = ','.join(str(e) for e in BTC_twelvehours_id_dict.get(k))
        if len(subitem["ids"]) < 8:
            continue
        twelvehours_trend_json.append(subitem)
        i += 1
    BTC_event_dict["twelvehours"] = json.dumps(twelvehours_trend_json)


    twelvehours_trend_json = []
    trend_text, ids = extract_id(BTC_event_dict["twelvehours"])

    data = {'trend': trend_text, 'period': "twelvehours", 'ids': ids}
    crsr.execute(mysql_insert_trend, data)
    topic_id = crsr.lastrowid


    subitem = {}
    subitem["objects"] = trend_text
    subitem["period"] = "twelvehours"
    subitem["id"] = topic_id
    twelvehours_trend_json.append(subitem)
    BTC_event_dict_plusID["twelvehours"] = json.dumps(twelvehours_trend_json)


    delete_list = []
    for key in ETH_twelvehours_topic_dict:
        ETH_twelvehours_topic_dict[key] = ETH_twelvehours_topic_dict[key] * (1 - twelvehours_decay_speed)
        ETH_twelvehours_topic_dict[key] -= TWELVEHOURS_DECAY_SPEED_TUNE
        if ETH_twelvehours_topic_dict[key] <= 0:
            delete_list.append(key)
    for l in delete_list:
        ETH_twelvehours_topic_dict.pop(l)
        ETH_twelvehours_id_dict.pop(l)
    # clean lists
    delete_time_list = []
    for t in ETH_twelvehours_time_list:
        if (((Now - datetime.datetime.strptime(t, time_format)).seconds) + ((Now - datetime.datetime.strptime(t, time_format)).days * 86400)) >= TWELVEHOURS_KEEP_TIME:
            delete_time_list.append(t)
    for t in delete_time_list:
        pos = ETH_twelvehours_time_list.index(t)
        headline_id = ETH_twelvehours_ID_list[pos]
        ETH_twelvehours_time_list.pop(pos)
        ETH_twelvehours_ID_list.pop(pos)
        ETH_twelvehours_headline_list.pop(pos)
        ETH_twelvehours_importance_list.pop(pos)
        for items in ETH_twelvehours_id_dict.values():
            if headline_id in items:
                items.remove(headline_id)



    twelvehours_trend = sorted(ETH_twelvehours_topic_dict.items(), key = lambda x:x[1], reverse = True)


    i = 0
    tmp_dict = {}
    tmp_id_dict = {}
    for topic in twelvehours_trend:
        if i >= 500:
            break
        if len(tmp_dict) == 0:
            tmp_dict[topic[0]] = topic[1]
            tmp_id_dict[topic[0]] = ETH_twelvehours_id_dict.get(topic[0])
        else:
            same_id = 0
            is_dup = False
            for exist_key in tmp_id_dict:
                if len(ETH_twelvehours_id_dict.get(topic[0])) != 0:
                    for id in ETH_twelvehours_id_dict.get(topic[0]):

                        if id in tmp_id_dict[exist_key]:
                            same_id += 1
                    if same_id/len(ETH_twelvehours_id_dict.get(topic[0])) >= 0.5:
                        is_dup = True
                        break
                same_id = 0
            if is_dup == False:
                tmp_dict[topic[0]] = topic[1]
                tmp_id_dict[topic[0]] = ETH_twelvehours_id_dict.get(topic[0])

        i += 1

    twelvehours_trend_json = []
    i = 0

    for k in tmp_dict:
        if i >= 15:
            break
        
        subitem = {}
        subitem["text"] = k
        subitem["weight"] = round(tmp_dict[k], 2)
        subitem["ids"] = ','.join(str(e) for e in ETH_twelvehours_id_dict.get(k))
        if len(subitem["ids"]) < 8:
            continue
        twelvehours_trend_json.append(subitem)
        i += 1
    ETH_event_dict["twelvehours"] = json.dumps(twelvehours_trend_json)


    twelvehours_trend_json = []
    trend_text, ids = extract_id(ETH_event_dict["twelvehours"])

    data = {'trend': trend_text, 'period': "twelvehours", 'ids': ids}
    crsr.execute(mysql_insert_trend, data)
    topic_id = crsr.lastrowid

    subitem = {}
    subitem["objects"] = trend_text
    subitem["period"] = "twelvehours"
    subitem["id"] = topic_id
    twelvehours_trend_json.append(subitem)
    ETH_event_dict_plusID["twelvehours"] = json.dumps(twelvehours_trend_json)



    # recalculate dict
    oneday_decay_speed = (DECAY_SPEED)/ONEDAY_KEEP_TIME
    delete_list = []
    for key in BTC_oneday_topic_dict:
        BTC_oneday_topic_dict[key] = BTC_oneday_topic_dict[key] * (1 - oneday_decay_speed)
        BTC_oneday_topic_dict[key] -= ONEDAY_DECAY_SPEED_TUNE
        if BTC_oneday_topic_dict[key] <= 0:
            delete_list.append(key)
    for l in delete_list:
        BTC_oneday_topic_dict.pop(l)
        BTC_oneday_id_dict.pop(l)

    # clean lists
    delete_time_list = []
    for t in BTC_oneday_time_list:
        if (((Now - datetime.datetime.strptime(t, time_format)).seconds) + ((Now - datetime.datetime.strptime(t, time_format)).days * 86400)) >= ONEDAY_KEEP_TIME:
            delete_time_list.append(t)

    for t in delete_time_list:
        pos = BTC_oneday_time_list.index(t)
        headline_id = BTC_oneday_ID_list[pos]
        BTC_oneday_time_list.pop(pos)
        BTC_oneday_ID_list.pop(pos)
        BTC_oneday_headline_list.pop(pos)
        BTC_oneday_importance_list.pop(pos)
        for items in BTC_oneday_id_dict.values():
            if headline_id in items:
                items.remove(headline_id)



    oneday_trend = sorted(BTC_oneday_topic_dict.items(), key = lambda x:x[1], reverse = True)


    i = 0
    tmp_dict = {}
    tmp_id_dict = {}
    for topic in oneday_trend:
        if i >= 500:
            break
        if len(tmp_dict) == 0:
            tmp_dict[topic[0]] = topic[1]
            tmp_id_dict[topic[0]] = BTC_oneday_id_dict.get(topic[0])
        else:
            same_id = 0
            is_dup = False
            for exist_key in tmp_id_dict:
                if len(BTC_oneday_id_dict.get(topic[0])) != 0:
                    for id in BTC_oneday_id_dict.get(topic[0]):

                        if id in tmp_id_dict[exist_key]:
                            same_id += 1
                    if same_id/len(BTC_oneday_id_dict.get(topic[0])) >= 0.5:
                        is_dup = True
                        break
                same_id = 0
            if is_dup == False:
                tmp_dict[topic[0]] = topic[1]
                tmp_id_dict[topic[0]] = BTC_oneday_id_dict.get(topic[0])


        i += 1

    oneday_trend_json = []
    i = 0

    for k in tmp_dict:
        if i >= 15:
            break
        
        subitem = {}
        subitem["text"] = k
        subitem["weight"] = round(tmp_dict[k], 2)
        subitem["ids"] = ','.join(str(e) for e in BTC_oneday_id_dict.get(k))
        if len(subitem["ids"]) < 8:
            continue
        oneday_trend_json.append(subitem)
        i += 1

    BTC_event_dict["oneday"] = json.dumps(oneday_trend_json)


    oneday_trend_json = []
    trend_text, ids = extract_id(BTC_event_dict["oneday"])

    data = {'trend': trend_text, 'period': "oneday", 'ids': ids}
    crsr.execute(mysql_insert_trend, data)
    topic_id = crsr.lastrowid


    subitem = {}
    subitem["objects"] = trend_text
    subitem["period"] = "oneday"
    subitem["id"] = topic_id
    oneday_trend_json.append(subitem)
    BTC_event_dict_plusID["oneday"] = json.dumps(oneday_trend_json)



    delete_list = []
    for key in ETH_oneday_topic_dict:
        ETH_oneday_topic_dict[key] = ETH_oneday_topic_dict[key] * (1 - oneday_decay_speed)
        ETH_oneday_topic_dict[key] -= ONEDAY_DECAY_SPEED_TUNE
        if ETH_oneday_topic_dict[key] <= 0:
            delete_list.append(key)
    for l in delete_list:
        ETH_oneday_topic_dict.pop(l)
        ETH_oneday_id_dict.pop(l)

    # clean lists
    delete_time_list = []
    for t in ETH_oneday_time_list:
        if (((Now - datetime.datetime.strptime(t, time_format)).seconds) + ((Now - datetime.datetime.strptime(t, time_format)).days * 86400)) >= ONEDAY_KEEP_TIME:
            delete_time_list.append(t)

    for t in delete_time_list:
        pos = ETH_oneday_time_list.index(t)
        headline_id = ETH_oneday_ID_list[pos]
        ETH_oneday_time_list.pop(pos)
        ETH_oneday_ID_list.pop(pos)
        ETH_oneday_headline_list.pop(pos)
        ETH_oneday_importance_list.pop(pos)
        for items in ETH_oneday_id_dict.values():
            if headline_id in items:
                items.remove(headline_id)


    oneday_trend = sorted(ETH_oneday_topic_dict.items(), key = lambda x:x[1], reverse = True)

    i = 0
    tmp_dict = {}
    tmp_id_dict = {}
    for topic in oneday_trend:
        if i >= 500:
            break
        if len(tmp_dict) == 0:
            tmp_dict[topic[0]] = topic[1]
            tmp_id_dict[topic[0]] = ETH_oneday_id_dict.get(topic[0])
        else:
            same_id = 0
            is_dup = False
            for exist_key in tmp_id_dict:
                if len(ETH_oneday_id_dict.get(topic[0])) != 0:
                    for id in ETH_oneday_id_dict.get(topic[0]):

                        if id in tmp_id_dict[exist_key]:
                            same_id += 1
                    if same_id/len(ETH_oneday_id_dict.get(topic[0])) >= 0.5:
                        is_dup = True
                        break
                same_id = 0
            if is_dup == False:
                tmp_dict[topic[0]] = topic[1]
                tmp_id_dict[topic[0]] = ETH_oneday_id_dict.get(topic[0])


        i += 1

    oneday_trend_json = []
    i = 0

    for k in tmp_dict:
        if i >= 15:
            break
        
        subitem = {}
        subitem["text"] = k
        subitem["weight"] = round(tmp_dict[k], 2)
        subitem["ids"] = ','.join(str(e) for e in ETH_oneday_id_dict.get(k))
        if len(subitem["ids"]) < 8:
            continue
        oneday_trend_json.append(subitem)
        i += 1

    ETH_event_dict["oneday"] = json.dumps(oneday_trend_json)


    oneday_trend_json = []
    trend_text, ids = extract_id(ETH_event_dict["oneday"])

    data = {'trend': trend_text, 'period': "oneday", 'ids': ids}
    crsr.execute(mysql_insert_trend, data)
    topic_id = crsr.lastrowid


    subitem = {}
    subitem["objects"] = trend_text
    subitem["period"] = "oneday"
    subitem["id"] = topic_id
    oneday_trend_json.append(subitem)
    ETH_event_dict_plusID["oneday"] = json.dumps(oneday_trend_json)



    
    # recalculate dict
    oneweek_decay_speed = (DECAY_SPEED)/ONEWEEK_KEEP_TIME
    delete_list = []
    for key in BTC_oneweek_topic_dict:
        BTC_oneweek_topic_dict[key] = BTC_oneweek_topic_dict[key] * (1 - oneweek_decay_speed)
        BTC_oneweek_topic_dict[key] -= ONEWEEK_DECAY_SPEED_TUNE
        if BTC_oneweek_topic_dict[key] <= 0:
            delete_list.append(key)
    for l in delete_list:
        BTC_oneweek_topic_dict.pop(l)
        BTC_oneweek_id_dict.pop(l)

    # clean lists
    delete_time_list = []
    for t in BTC_oneweek_time_list:
        if (((Now - datetime.datetime.strptime(t, time_format)).seconds) + ((Now - datetime.datetime.strptime(t, time_format)).days * 86400)) >= ONEWEEK_KEEP_TIME:
            delete_time_list.append(t)

    for t in delete_time_list:
        pos = BTC_oneweek_time_list.index(t)
        headline_id = BTC_oneweek_ID_list[pos]
        BTC_oneweek_time_list.pop(pos)
        BTC_oneweek_ID_list.pop(pos)
        BTC_oneweek_headline_list.pop(pos)
        BTC_oneweek_importance_list.pop(pos)
        for items in BTC_oneweek_id_dict.values():
            if headline_id in items:
                items.remove(headline_id)




    oneweek_trend = sorted(BTC_oneweek_topic_dict.items(), key = lambda x:x[1], reverse = True)


    i = 0
    tmp_dict = {}
    tmp_id_dict = {}
    for topic in oneweek_trend:
        if i >= 500:
            break
        if len(tmp_dict) == 0:
            tmp_dict[topic[0]] = topic[1]
            tmp_id_dict[topic[0]] = BTC_oneweek_id_dict.get(topic[0])
        else:
            same_id = 0
            is_dup = False
            for exist_key in tmp_id_dict:
                if len(BTC_oneweek_id_dict.get(topic[0])) != 0:
                    for id in BTC_oneweek_id_dict.get(topic[0]):

                        if id in tmp_id_dict[exist_key]:
                            same_id += 1
                    if same_id/len(BTC_oneweek_id_dict.get(topic[0])) >= 0.5:
                        is_dup = True
                        break
                same_id = 0
            if is_dup == False:
                tmp_dict[topic[0]] = topic[1]
                tmp_id_dict[topic[0]] = BTC_oneweek_id_dict.get(topic[0])


        i += 1

    oneweek_trend_json = []
    i = 0

    for k in tmp_dict:
        if i >= 15:
            break
        
        subitem = {}
        subitem["text"] = k
        subitem["weight"] = round(tmp_dict[k], 2)
        subitem["ids"] = ','.join(str(e) for e in BTC_oneweek_id_dict.get(k))
        if len(subitem["ids"]) < 8:
            continue
        oneweek_trend_json.append(subitem)
        i += 1

    BTC_event_dict["oneweek"] = json.dumps(oneweek_trend_json)


    oneweek_trend_json = []
    trend_text, ids = extract_id(BTC_event_dict["oneweek"])

    data = {'trend': trend_text, 'period': "oneweek", 'ids': ids}
    crsr.execute(mysql_insert_trend, data)
    topic_id = crsr.lastrowid


    subitem = {}
    subitem["objects"] = trend_text
    subitem["period"] = "oneweek"
    subitem["id"] = topic_id
    oneweek_trend_json.append(subitem)
    BTC_event_dict_plusID["oneweek"] = json.dumps(oneweek_trend_json)



    delete_list = []
    for key in ETH_oneweek_topic_dict:
        ETH_oneweek_topic_dict[key] = ETH_oneweek_topic_dict[key] * (1 - oneweek_decay_speed)
        ETH_oneweek_topic_dict[key] -= ONEWEEK_DECAY_SPEED_TUNE
        if ETH_oneweek_topic_dict[key] <= 0:
            delete_list.append(key)
    for l in delete_list:
        ETH_oneweek_topic_dict.pop(l)
        ETH_oneweek_id_dict.pop(l)

    # clean lists
    delete_time_list = []
    for t in ETH_oneweek_time_list:
        if (((Now - datetime.datetime.strptime(t, time_format)).seconds) + ((Now - datetime.datetime.strptime(t, time_format)).days * 86400)) >= ONEWEEK_KEEP_TIME:
            delete_time_list.append(t)

    for t in delete_time_list:
        pos = ETH_oneweek_time_list.index(t)
        headline_id = ETH_oneweek_ID_list[pos]
        ETH_oneweek_time_list.pop(pos)
        ETH_oneweek_ID_list.pop(pos)
        ETH_oneweek_headline_list.pop(pos)
        ETH_oneweek_importance_list.pop(pos)
        for items in ETH_oneweek_id_dict.values():
            if headline_id in items:
                items.remove(headline_id)




    oneweek_trend = sorted(ETH_oneweek_topic_dict.items(), key = lambda x:x[1], reverse = True)


    i = 0
    tmp_dict = {}
    tmp_id_dict = {}
    for topic in oneweek_trend:
        if i >= 500:
            break
        if len(tmp_dict) == 0:
            tmp_dict[topic[0]] = topic[1]
            tmp_id_dict[topic[0]] = ETH_oneweek_id_dict.get(topic[0])
        else:
            same_id = 0
            is_dup = False
            for exist_key in tmp_id_dict:
                if len(ETH_oneweek_id_dict.get(topic[0])) != 0:
                    for id in ETH_oneweek_id_dict.get(topic[0]):

                        if id in tmp_id_dict[exist_key]:
                            same_id += 1
                    if same_id/len(ETH_oneweek_id_dict.get(topic[0])) >= 0.5:
                        is_dup = True
                        break
                same_id = 0
            if is_dup == False:
                tmp_dict[topic[0]] = topic[1]
                tmp_id_dict[topic[0]] = ETH_oneweek_id_dict.get(topic[0])


        i += 1

    oneweek_trend_json = []
    i = 0

    for k in tmp_dict:
        if i >= 15:
            break
        
        subitem = {}
        subitem["text"] = k
        subitem["weight"] = round(tmp_dict[k], 2)
        subitem["ids"] = ','.join(str(e) for e in ETH_oneweek_id_dict.get(k))
        if len(subitem["ids"]) < 8:
            continue
        oneweek_trend_json.append(subitem)
        i += 1

    ETH_event_dict["oneweek"] = json.dumps(oneweek_trend_json)


    oneweek_trend_json = []
    trend_text, ids = extract_id(ETH_event_dict["oneweek"])

    data = {'trend': trend_text, 'period': "oneweek", 'ids': ids}
    crsr.execute(mysql_insert_trend, data)
    topic_id = crsr.lastrowid


    subitem = {}
    subitem["objects"] = trend_text
    subitem["period"] = "oneweek"
    subitem["id"] = topic_id
    oneweek_trend_json.append(subitem)
    ETH_event_dict_plusID["oneweek"] = json.dumps(oneweek_trend_json)




    # recalculate dict
    onemonth_decay_speed = (DECAY_SPEED)/ONEMONTH_KEEP_TIME
    delete_list = []
    for key in BTC_onemonth_topic_dict:
        BTC_onemonth_topic_dict[key] = BTC_onemonth_topic_dict[key] * (1 - onemonth_decay_speed)
        BTC_onemonth_topic_dict[key] -= ONEMONTH_DECAY_SPEED_TUNE
        if BTC_onemonth_topic_dict[key] <= 0:
            delete_list.append(key)
    for l in delete_list:
        BTC_onemonth_topic_dict.pop(l)
        BTC_onemonth_id_dict.pop(l)

    # clean lists
    delete_time_list = []
    for t in BTC_onemonth_time_list:
        if (((Now - datetime.datetime.strptime(t, time_format)).seconds) + ((Now - datetime.datetime.strptime(t, time_format)).days * 86400)) >= ONEMONTH_KEEP_TIME:
            delete_time_list.append(t)

    for t in delete_time_list:
        pos = BTC_onemonth_time_list.index(t)
        headline_id = BTC_onemonth_ID_list[pos]
        BTC_onemonth_time_list.pop(pos)
        BTC_onemonth_ID_list.pop(pos)
        BTC_onemonth_headline_list.pop(pos)
        BTC_onemonth_importance_list.pop(pos)       
        for items in BTC_onemonth_id_dict.values():
            if headline_id in items:
                items.remove(headline_id)

    onemonth_trend = sorted(BTC_onemonth_topic_dict.items(), key = lambda x:x[1], reverse = True)


    i = 0
    tmp_dict = {}
    tmp_id_dict = {}
    for topic in onemonth_trend:
        if i >= 500:
            break
        if len(tmp_dict) == 0:
            tmp_dict[topic[0]] = topic[1]
            tmp_id_dict[topic[0]] = BTC_onemonth_id_dict.get(topic[0])
        else:
            same_id = 0
            is_dup = False
            for exist_key in tmp_id_dict:
                if len(BTC_onemonth_id_dict.get(topic[0])) != 0:
                    for id in BTC_onemonth_id_dict.get(topic[0]):

                        if id in tmp_id_dict[exist_key]:
                            same_id += 1
                    if same_id/len(BTC_onemonth_id_dict.get(topic[0])) >= 0.5:
                        is_dup = True
                        break
                same_id = 0
            if is_dup == False:
                tmp_dict[topic[0]] = topic[1]
                tmp_id_dict[topic[0]] = BTC_onemonth_id_dict.get(topic[0])


        i += 1

    onemonth_trend_json = []
    i = 0

    for k in tmp_dict:
        if i >= 15:
            break
        
        subitem = {}
        subitem["text"] = k
        subitem["weight"] = round(tmp_dict[k], 2)
        subitem["ids"] = ','.join(str(e) for e in BTC_onemonth_id_dict.get(k))
        if len(subitem["ids"]) < 8:
            continue
        onemonth_trend_json.append(subitem)
        i += 1

    BTC_event_dict["onemonth"] = json.dumps(onemonth_trend_json)
    

    onemonth_trend_json = []
    trend_text, ids = extract_id(BTC_event_dict["onemonth"])

    data = {'trend': trend_text, 'period': "onemonth", 'ids': ids}
    crsr.execute(mysql_insert_trend, data)
    topic_id = crsr.lastrowid


    subitem = {}
    subitem["objects"] = trend_text
    subitem["period"] = "onemonth"
    subitem["id"] = topic_id
    onemonth_trend_json.append(subitem)
    BTC_event_dict_plusID["onemonth"] = json.dumps(onemonth_trend_json)




    delete_list = []
    for key in ETH_onemonth_topic_dict:
        ETH_onemonth_topic_dict[key] = ETH_onemonth_topic_dict[key] * (1 - onemonth_decay_speed)
        ETH_onemonth_topic_dict[key] -= ONEMONTH_DECAY_SPEED_TUNE
        if ETH_onemonth_topic_dict[key] <= 0:
            delete_list.append(key)
    for l in delete_list:
        ETH_onemonth_topic_dict.pop(l)
        ETH_onemonth_id_dict.pop(l)

    # clean lists
    delete_time_list = []
    for t in ETH_onemonth_time_list:
        if (((Now - datetime.datetime.strptime(t, time_format)).seconds) + ((Now - datetime.datetime.strptime(t, time_format)).days * 86400)) >= ONEMONTH_KEEP_TIME:
            delete_time_list.append(t)

    for t in delete_time_list:
        pos = ETH_onemonth_time_list.index(t)
        headline_id = ETH_onemonth_ID_list[pos]
        ETH_onemonth_time_list.pop(pos)
        ETH_onemonth_ID_list.pop(pos)
        ETH_onemonth_headline_list.pop(pos)
        ETH_onemonth_importance_list.pop(pos)       
        for items in ETH_onemonth_id_dict.values():
            if headline_id in items:
                items.remove(headline_id)

    onemonth_trend = sorted(ETH_onemonth_topic_dict.items(), key = lambda x:x[1], reverse = True)


    i = 0
    tmp_dict = {}
    tmp_id_dict = {}
    for topic in onemonth_trend:
        if i >= 500:
            break
        if len(tmp_dict) == 0:
            tmp_dict[topic[0]] = topic[1]
            tmp_id_dict[topic[0]] = ETH_onemonth_id_dict.get(topic[0])
        else:
            same_id = 0
            is_dup = False
            for exist_key in tmp_id_dict:
                if len(ETH_onemonth_id_dict.get(topic[0])) != 0:
                    for id in ETH_onemonth_id_dict.get(topic[0]):

                        if id in tmp_id_dict[exist_key]:
                            same_id += 1
                    if same_id/len(ETH_onemonth_id_dict.get(topic[0])) >= 0.5:
                        is_dup = True
                        break
                same_id = 0
            if is_dup == False:
                tmp_dict[topic[0]] = topic[1]
                tmp_id_dict[topic[0]] = ETH_onemonth_id_dict.get(topic[0])


        i += 1

    onemonth_trend_json = []
    i = 0

    for k in tmp_dict:
        if i >= 15:
            break
        
        subitem = {}
        subitem["text"] = k
        subitem["weight"] = round(tmp_dict[k], 2)
        subitem["ids"] = ','.join(str(e) for e in ETH_onemonth_id_dict.get(k))
        if len(subitem["ids"]) < 8:
            continue
        onemonth_trend_json.append(subitem)
        i += 1

    ETH_event_dict["onemonth"] = json.dumps(onemonth_trend_json)
    

    onemonth_trend_json = []
    trend_text, ids = extract_id(ETH_event_dict["onemonth"])

    data = {'trend': trend_text, 'period': "onemonth", 'ids': ids}
    crsr.execute(mysql_insert_trend, data)
    topic_id = crsr.lastrowid


    subitem = {}
    subitem["objects"] = trend_text
    subitem["period"] = "onemonth"
    subitem["id"] = topic_id
    onemonth_trend_json.append(subitem)
    ETH_event_dict_plusID["onemonth"] = json.dumps(onemonth_trend_json)




    # recalculate dict
    threemonths_decay_speed = (DECAY_SPEED)/THREEMONTHS_KEEP_TIME
    delete_list = []
    for key in BTC_threemonths_topic_dict:
        BTC_threemonths_topic_dict[key] = BTC_threemonths_topic_dict[key] * (1 - threemonths_decay_speed)
        BTC_threemonths_topic_dict[key] -= THREEMONTHS_DECAY_SPEED_TUNE
        if BTC_threemonths_topic_dict[key] <= 0:
            delete_list.append(key)
    for l in delete_list:
        BTC_threemonths_topic_dict.pop(l)
        BTC_threemonths_id_dict.pop(l)

    # clean lists
    delete_time_list = []
    for t in BTC_threemonths_time_list:
        if (((Now - datetime.datetime.strptime(t, time_format)).seconds) + ((Now - datetime.datetime.strptime(t, time_format)).days * 86400)) >= THREEMONTHS_KEEP_TIME:
            delete_time_list.append(t)

    for t in delete_time_list:
        pos = BTC_threemonths_time_list.index(t)
        headline_id = BTC_threemonths_ID_list[pos]
        BTC_threemonths_time_list.pop(pos)
        BTC_threemonths_ID_list.pop(pos)
        BTC_threemonths_headline_list.pop(pos)
        BTC_threemonths_importance_list.pop(pos)                    
        for items in BTC_threemonths_id_dict.values():
            if headline_id in items:
                items.remove(headline_id)


    threemonths_trend = sorted(BTC_threemonths_topic_dict.items(), key = lambda x:x[1], reverse = True)


    i = 0
    tmp_dict = {}
    tmp_id_dict = {}
    for topic in threemonths_trend:
        if i >= 500:
            break
        if len(tmp_dict) == 0:
            tmp_dict[topic[0]] = topic[1]
            tmp_id_dict[topic[0]] = BTC_threemonths_id_dict.get(topic[0])
        else:
            same_id = 0
            is_dup = False
            for exist_key in tmp_id_dict:
                if len(BTC_threemonths_id_dict.get(topic[0])) != 0:
                    for id in BTC_threemonths_id_dict.get(topic[0]):

                        if id in tmp_id_dict[exist_key]:
                            same_id += 1
                    if same_id/len(BTC_threemonths_id_dict.get(topic[0])) >= 0.5:
                        is_dup = True
                        break
                same_id = 0
            if is_dup == False:
                tmp_dict[topic[0]] = topic[1]
                tmp_id_dict[topic[0]] = BTC_threemonths_id_dict.get(topic[0])


        i += 1

    threemonths_trend_json = []
    i = 0

    for k in tmp_dict:
        if i >= 15:
            break
        
        subitem = {}
        subitem["text"] = k
        subitem["weight"] = round(tmp_dict[k], 2)
        subitem["ids"] = ','.join(str(e) for e in BTC_threemonths_id_dict.get(k))
        if len(subitem["ids"]) < 8:
            continue
        threemonths_trend_json.append(subitem)
        i += 1

    BTC_event_dict["threemonths"] = json.dumps(threemonths_trend_json)


    threemonths_trend_json = []
    trend_text, ids = extract_id(BTC_event_dict["threemonths"])

    data = {'trend': trend_text, 'period': "threemonths", 'ids': ids}
    crsr.execute(mysql_insert_trend, data)
    topic_id = crsr.lastrowid


    subitem = {}
    subitem["objects"] = trend_text
    subitem["period"] = "threemonths"
    subitem["id"] = topic_id
    threemonths_trend_json.append(subitem)
    BTC_event_dict_plusID["threemonths"] = json.dumps(threemonths_trend_json)




    delete_list = []
    for key in ETH_threemonths_topic_dict:
        ETH_threemonths_topic_dict[key] = ETH_threemonths_topic_dict[key] * (1 - threemonths_decay_speed)
        ETH_threemonths_topic_dict[key] -= THREEMONTHS_DECAY_SPEED_TUNE
        if ETH_threemonths_topic_dict[key] <= 0:
            delete_list.append(key)
    for l in delete_list:
        ETH_threemonths_topic_dict.pop(l)
        ETH_threemonths_id_dict.pop(l)

    # clean lists
    delete_time_list = []
    for t in ETH_threemonths_time_list:
        if (((Now - datetime.datetime.strptime(t, time_format)).seconds) + ((Now - datetime.datetime.strptime(t, time_format)).days * 86400)) >= THREEMONTHS_KEEP_TIME:
            delete_time_list.append(t)

    for t in delete_time_list:
        pos = ETH_threemonths_time_list.index(t)
        headline_id = ETH_threemonths_ID_list[pos]
        ETH_threemonths_time_list.pop(pos)
        ETH_threemonths_ID_list.pop(pos)
        ETH_threemonths_headline_list.pop(pos)
        ETH_threemonths_importance_list.pop(pos)                    
        for items in ETH_threemonths_id_dict.values():
            if headline_id in items:
                items.remove(headline_id)


    threemonths_trend = sorted(ETH_threemonths_topic_dict.items(), key = lambda x:x[1], reverse = True)


    i = 0
    tmp_dict = {}
    tmp_id_dict = {}
    for topic in threemonths_trend:
        if i >= 500:
            break
        if len(tmp_dict) == 0:
            tmp_dict[topic[0]] = topic[1]
            tmp_id_dict[topic[0]] = ETH_threemonths_id_dict.get(topic[0])
        else:
            same_id = 0
            is_dup = False
            for exist_key in tmp_id_dict:
                if len(ETH_threemonths_id_dict.get(topic[0])) != 0:
                    for id in ETH_threemonths_id_dict.get(topic[0]):

                        if id in tmp_id_dict[exist_key]:
                            same_id += 1
                    if same_id/len(ETH_threemonths_id_dict.get(topic[0])) >= 0.5:
                        is_dup = True
                        break
                same_id = 0
            if is_dup == False:
                tmp_dict[topic[0]] = topic[1]
                tmp_id_dict[topic[0]] = ETH_threemonths_id_dict.get(topic[0])


        i += 1

    threemonths_trend_json = []
    i = 0

    for k in tmp_dict:
        if i >= 15:
            break
        
        subitem = {}
        subitem["text"] = k
        subitem["weight"] = round(tmp_dict[k], 2)
        subitem["ids"] = ','.join(str(e) for e in ETH_threemonths_id_dict.get(k))
        if len(subitem["ids"]) < 8:
            continue
        threemonths_trend_json.append(subitem)
        i += 1

    ETH_event_dict["threemonths"] = json.dumps(threemonths_trend_json)


    threemonths_trend_json = []
    trend_text, ids = extract_id(ETH_event_dict["threemonths"])

    data = {'trend': trend_text, 'period': "threemonths", 'ids': ids}
    crsr.execute(mysql_insert_trend, data)
    topic_id = crsr.lastrowid


    subitem = {}
    subitem["objects"] = trend_text
    subitem["period"] = "threemonths"
    subitem["id"] = topic_id
    threemonths_trend_json.append(subitem)
    ETH_event_dict_plusID["threemonths"] = json.dumps(threemonths_trend_json)


    
    # recalculate dict
    delete_list = []
    for key in XRP_twelvehours_topic_dict:
        XRP_twelvehours_topic_dict[key] = XRP_twelvehours_topic_dict[key] * (1 - twelvehours_decay_speed)
        XRP_twelvehours_topic_dict[key] -= TWELVEHOURS_DECAY_SPEED_TUNE
        if XRP_twelvehours_topic_dict[key] <= 0:
            delete_list.append(key)
    for l in delete_list:
        XRP_twelvehours_topic_dict.pop(l)
        XRP_twelvehours_id_dict.pop(l)
    # clean lists
    delete_time_list = []
    for t in XRP_twelvehours_time_list:
        if (((Now - datetime.datetime.strptime(t, time_format)).seconds) + ((Now - datetime.datetime.strptime(t, time_format)).days * 86400)) >= TWELVEHOURS_KEEP_TIME:
            delete_time_list.append(t)
    for t in delete_time_list:
        pos = XRP_twelvehours_time_list.index(t)
        headline_id = XRP_twelvehours_ID_list[pos]
        XRP_twelvehours_time_list.pop(pos)
        XRP_twelvehours_ID_list.pop(pos)
        XRP_twelvehours_headline_list.pop(pos)
        XRP_twelvehours_importance_list.pop(pos)
        for items in XRP_twelvehours_id_dict.values():
            if headline_id in items:
                items.remove(headline_id)



    twelvehours_trend = sorted(XRP_twelvehours_topic_dict.items(), key = lambda x:x[1], reverse = True)


    i = 0
    tmp_dict = {}
    tmp_id_dict = {}
    for topic in twelvehours_trend:
        if i >= 500:
            break
        if len(tmp_dict) == 0:
            tmp_dict[topic[0]] = topic[1]
            tmp_id_dict[topic[0]] = XRP_twelvehours_id_dict.get(topic[0])
        else:
            same_id = 0
            is_dup = False
            for exist_key in tmp_id_dict:
                if len(XRP_twelvehours_id_dict.get(topic[0])) != 0:
                    for id in XRP_twelvehours_id_dict.get(topic[0]):

                        if id in tmp_id_dict[exist_key]:
                            same_id += 1
                    if same_id/len(XRP_twelvehours_id_dict.get(topic[0])) >= 0.5:
                        is_dup = True
                        break
                same_id = 0
            if is_dup == False:
                tmp_dict[topic[0]] = topic[1]
                tmp_id_dict[topic[0]] = XRP_twelvehours_id_dict.get(topic[0])


        i += 1



    twelvehours_trend_json = []
    i = 0

    for k in tmp_dict:
        if i >= 15:
            break
        
        subitem = {}
        subitem["text"] = k
        subitem["weight"] = round(tmp_dict[k], 2)
        subitem["ids"] = ','.join(str(e) for e in XRP_twelvehours_id_dict.get(k))
        if len(subitem["ids"]) < 8:
            continue
        twelvehours_trend_json.append(subitem)
        i += 1
    XRP_event_dict["twelvehours"] = json.dumps(twelvehours_trend_json)


    twelvehours_trend_json = []
    trend_text, ids = extract_id(XRP_event_dict["twelvehours"])

    data = {'trend': trend_text, 'period': "twelvehours", 'ids': ids}
    crsr.execute(mysql_insert_trend, data)
    topic_id = crsr.lastrowid


    subitem = {}
    subitem["objects"] = trend_text
    subitem["period"] = "twelvehours"
    subitem["id"] = topic_id
    twelvehours_trend_json.append(subitem)
    XRP_event_dict_plusID["twelvehours"] = json.dumps(twelvehours_trend_json)




    # recalculate dict
    delete_list = []
    for key in XRP_oneday_topic_dict:
        XRP_oneday_topic_dict[key] = XRP_oneday_topic_dict[key] * (1 - oneday_decay_speed)
        XRP_oneday_topic_dict[key] -= ONEDAY_DECAY_SPEED_TUNE
        if XRP_oneday_topic_dict[key] <= 0:
            delete_list.append(key)
    for l in delete_list:
        XRP_oneday_topic_dict.pop(l)
        XRP_oneday_id_dict.pop(l)

    # clean lists
    delete_time_list = []
    for t in XRP_oneday_time_list:
        if (((Now - datetime.datetime.strptime(t, time_format)).seconds) + ((Now - datetime.datetime.strptime(t, time_format)).days * 86400)) >= ONEDAY_KEEP_TIME:
            delete_time_list.append(t)

    for t in delete_time_list:
        pos = XRP_oneday_time_list.index(t)
        headline_id = XRP_oneday_ID_list[pos]
        XRP_oneday_time_list.pop(pos)
        XRP_oneday_ID_list.pop(pos)
        XRP_oneday_headline_list.pop(pos)
        XRP_oneday_importance_list.pop(pos)
        for items in XRP_oneday_id_dict.values():
            if headline_id in items:
                items.remove(headline_id)



    oneday_trend = sorted(XRP_oneday_topic_dict.items(), key = lambda x:x[1], reverse = True)


    i = 0
    tmp_dict = {}
    tmp_id_dict = {}
    for topic in oneday_trend:
        if i >= 500:
            break
        if len(tmp_dict) == 0:
            tmp_dict[topic[0]] = topic[1]
            tmp_id_dict[topic[0]] = XRP_oneday_id_dict.get(topic[0])
        else:
            same_id = 0
            is_dup = False
            for exist_key in tmp_id_dict:
                if len(XRP_oneday_id_dict.get(topic[0])) != 0:
                    for id in XRP_oneday_id_dict.get(topic[0]):

                        if id in tmp_id_dict[exist_key]:
                            same_id += 1
                    if same_id/len(XRP_oneday_id_dict.get(topic[0])) >= 0.5:
                        is_dup = True
                        break
                same_id = 0
            if is_dup == False:
                tmp_dict[topic[0]] = topic[1]
                tmp_id_dict[topic[0]] = XRP_oneday_id_dict.get(topic[0])


        i += 1

    oneday_trend_json = []
    i = 0

    for k in tmp_dict:
        if i >= 15:
            break
        
        subitem = {}
        subitem["text"] = k
        subitem["weight"] = round(tmp_dict[k], 2)
        subitem["ids"] = ','.join(str(e) for e in XRP_oneday_id_dict.get(k))
        if len(subitem["ids"]) < 8:
            continue
        oneday_trend_json.append(subitem)
        i += 1

    XRP_event_dict["oneday"] = json.dumps(oneday_trend_json)


    oneday_trend_json = []
    trend_text, ids = extract_id(XRP_event_dict["oneday"])

    data = {'trend': trend_text, 'period': "oneday", 'ids': ids}
    crsr.execute(mysql_insert_trend, data)
    topic_id = crsr.lastrowid


    subitem = {}
    subitem["objects"] = trend_text
    subitem["period"] = "oneday"
    subitem["id"] = topic_id
    oneday_trend_json.append(subitem)
    XRP_event_dict_plusID["oneday"] = json.dumps(oneday_trend_json)





    # recalculate dict
    delete_list = []
    for key in XRP_oneweek_topic_dict:
        XRP_oneweek_topic_dict[key] = XRP_oneweek_topic_dict[key] * (1 - oneweek_decay_speed)
        XRP_oneweek_topic_dict[key] -= ONEWEEK_DECAY_SPEED_TUNE
        if XRP_oneweek_topic_dict[key] <= 0:
            delete_list.append(key)
    for l in delete_list:
        XRP_oneweek_topic_dict.pop(l)
        XRP_oneweek_id_dict.pop(l)

    # clean lists
    delete_time_list = []
    for t in XRP_oneweek_time_list:
        if (((Now - datetime.datetime.strptime(t, time_format)).seconds) + ((Now - datetime.datetime.strptime(t, time_format)).days * 86400)) >= ONEWEEK_KEEP_TIME:
            delete_time_list.append(t)

    for t in delete_time_list:
        pos = XRP_oneweek_time_list.index(t)
        headline_id = XRP_oneweek_ID_list[pos]
        XRP_oneweek_time_list.pop(pos)
        XRP_oneweek_ID_list.pop(pos)
        XRP_oneweek_headline_list.pop(pos)
        XRP_oneweek_importance_list.pop(pos)
        for items in XRP_oneweek_id_dict.values():
            if headline_id in items:
                items.remove(headline_id)




    oneweek_trend = sorted(XRP_oneweek_topic_dict.items(), key = lambda x:x[1], reverse = True)


    i = 0
    tmp_dict = {}
    tmp_id_dict = {}
    for topic in oneweek_trend:
        if i >= 500:
            break
        if len(tmp_dict) == 0:
            tmp_dict[topic[0]] = topic[1]
            tmp_id_dict[topic[0]] = XRP_oneweek_id_dict.get(topic[0])
        else:
            same_id = 0
            is_dup = False
            for exist_key in tmp_id_dict:
                if len(XRP_oneweek_id_dict.get(topic[0])) != 0:
                    for id in XRP_oneweek_id_dict.get(topic[0]):

                        if id in tmp_id_dict[exist_key]:
                            same_id += 1
                    if same_id/len(XRP_oneweek_id_dict.get(topic[0])) >= 0.5:
                        is_dup = True
                        break
                same_id = 0
            if is_dup == False:
                tmp_dict[topic[0]] = topic[1]
                tmp_id_dict[topic[0]] = XRP_oneweek_id_dict.get(topic[0])


        i += 1

    oneweek_trend_json = []
    i = 0

    for k in tmp_dict:
        if i >= 15:
            break
        
        subitem = {}
        subitem["text"] = k
        subitem["weight"] = round(tmp_dict[k], 2)
        subitem["ids"] = ','.join(str(e) for e in XRP_oneweek_id_dict.get(k))
        if len(subitem["ids"]) < 8:
            continue
        oneweek_trend_json.append(subitem)
        i += 1

    XRP_event_dict["oneweek"] = json.dumps(oneweek_trend_json)


    oneweek_trend_json = []
    trend_text, ids = extract_id(XRP_event_dict["oneweek"])

    data = {'trend': trend_text, 'period': "oneweek", 'ids': ids}
    crsr.execute(mysql_insert_trend, data)
    topic_id = crsr.lastrowid


    subitem = {}
    subitem["objects"] = trend_text
    subitem["period"] = "oneweek"
    subitem["id"] = topic_id
    oneweek_trend_json.append(subitem)
    XRP_event_dict_plusID["oneweek"] = json.dumps(oneweek_trend_json)




    # recalculate dict
    delete_list = []
    for key in XRP_onemonth_topic_dict:
        XRP_onemonth_topic_dict[key] = XRP_onemonth_topic_dict[key] * (1 - onemonth_decay_speed)
        XRP_onemonth_topic_dict[key] -= ONEMONTH_DECAY_SPEED_TUNE
        if XRP_onemonth_topic_dict[key] <= 0:
            delete_list.append(key)
    for l in delete_list:
        XRP_onemonth_topic_dict.pop(l)
        XRP_onemonth_id_dict.pop(l)

    # clean lists
    delete_time_list = []
    for t in XRP_onemonth_time_list:
        if (((Now - datetime.datetime.strptime(t, time_format)).seconds) + ((Now - datetime.datetime.strptime(t, time_format)).days * 86400)) >= ONEMONTH_KEEP_TIME:
            delete_time_list.append(t)

    for t in delete_time_list:
        pos = XRP_onemonth_time_list.index(t)
        headline_id = XRP_onemonth_ID_list[pos]
        XRP_onemonth_time_list.pop(pos)
        XRP_onemonth_ID_list.pop(pos)
        XRP_onemonth_headline_list.pop(pos)
        XRP_onemonth_importance_list.pop(pos)       
        for items in XRP_onemonth_id_dict.values():
            if headline_id in items:
                items.remove(headline_id)

    onemonth_trend = sorted(XRP_onemonth_topic_dict.items(), key = lambda x:x[1], reverse = True)


    i = 0
    tmp_dict = {}
    tmp_id_dict = {}
    for topic in onemonth_trend:
        if i >= 500:
            break
        if len(tmp_dict) == 0:
            tmp_dict[topic[0]] = topic[1]
            tmp_id_dict[topic[0]] = XRP_onemonth_id_dict.get(topic[0])
        else:
            same_id = 0
            is_dup = False
            for exist_key in tmp_id_dict:
                if len(XRP_onemonth_id_dict.get(topic[0])) != 0:
                    for id in XRP_onemonth_id_dict.get(topic[0]):

                        if id in tmp_id_dict[exist_key]:
                            same_id += 1
                    if same_id/len(XRP_onemonth_id_dict.get(topic[0])) >= 0.5:
                        is_dup = True
                        break
                same_id = 0
            if is_dup == False:
                tmp_dict[topic[0]] = topic[1]
                tmp_id_dict[topic[0]] = XRP_onemonth_id_dict.get(topic[0])


        i += 1

    onemonth_trend_json = []
    i = 0

    for k in tmp_dict:
        if i >= 15:
            break
        
        subitem = {}
        subitem["text"] = k
        subitem["weight"] = round(tmp_dict[k], 2)
        subitem["ids"] = ','.join(str(e) for e in XRP_onemonth_id_dict.get(k))
        if len(subitem["ids"]) < 8:
            continue
        onemonth_trend_json.append(subitem)
        i += 1

    XRP_event_dict["onemonth"] = json.dumps(onemonth_trend_json)
    

    onemonth_trend_json = []
    trend_text, ids = extract_id(XRP_event_dict["onemonth"])

    data = {'trend': trend_text, 'period': "onemonth", 'ids': ids}
    crsr.execute(mysql_insert_trend, data)
    topic_id = crsr.lastrowid


    subitem = {}
    subitem["objects"] = trend_text
    subitem["period"] = "onemonth"
    subitem["id"] = topic_id
    onemonth_trend_json.append(subitem)
    XRP_event_dict_plusID["onemonth"] = json.dumps(onemonth_trend_json)




    # recalculate dict
    delete_list = []
    for key in XRP_threemonths_topic_dict:
        XRP_threemonths_topic_dict[key] = XRP_threemonths_topic_dict[key] * (1 - threemonths_decay_speed)
        XRP_threemonths_topic_dict[key] -= THREEMONTHS_DECAY_SPEED_TUNE
        if XRP_threemonths_topic_dict[key] <= 0:
            delete_list.append(key)
    for l in delete_list:
        XRP_threemonths_topic_dict.pop(l)
        XRP_threemonths_id_dict.pop(l)

    # clean lists
    delete_time_list = []
    for t in XRP_threemonths_time_list:
        if (((Now - datetime.datetime.strptime(t, time_format)).seconds) + ((Now - datetime.datetime.strptime(t, time_format)).days * 86400)) >= THREEMONTHS_KEEP_TIME:
            delete_time_list.append(t)

    for t in delete_time_list:
        pos = XRP_threemonths_time_list.index(t)
        headline_id = XRP_threemonths_ID_list[pos]
        XRP_threemonths_time_list.pop(pos)
        XRP_threemonths_ID_list.pop(pos)
        XRP_threemonths_headline_list.pop(pos)
        XRP_threemonths_importance_list.pop(pos)                    
        for items in XRP_threemonths_id_dict.values():
            if headline_id in items:
                items.remove(headline_id)


    threemonths_trend = sorted(XRP_threemonths_topic_dict.items(), key = lambda x:x[1], reverse = True)


    i = 0
    tmp_dict = {}
    tmp_id_dict = {}
    for topic in threemonths_trend:
        if i >= 500:
            break
        if len(tmp_dict) == 0:
            tmp_dict[topic[0]] = topic[1]
            tmp_id_dict[topic[0]] = XRP_threemonths_id_dict.get(topic[0])
        else:
            same_id = 0
            is_dup = False
            for exist_key in tmp_id_dict:
                if len(XRP_threemonths_id_dict.get(topic[0])) != 0:
                    for id in XRP_threemonths_id_dict.get(topic[0]):

                        if id in tmp_id_dict[exist_key]:
                            same_id += 1
                    if same_id/len(XRP_threemonths_id_dict.get(topic[0])) >= 0.5:
                        is_dup = True
                        break
                same_id = 0
            if is_dup == False:
                tmp_dict[topic[0]] = topic[1]
                tmp_id_dict[topic[0]] = XRP_threemonths_id_dict.get(topic[0])


        i += 1

    threemonths_trend_json = []
    i = 0

    for k in tmp_dict:
        if i >= 15:
            break
        
        subitem = {}
        subitem["text"] = k
        subitem["weight"] = round(tmp_dict[k], 2)
        subitem["ids"] = ','.join(str(e) for e in XRP_threemonths_id_dict.get(k))
        if len(subitem["ids"]) < 8:
            continue
        threemonths_trend_json.append(subitem)
        i += 1

    XRP_event_dict["threemonths"] = json.dumps(threemonths_trend_json)


    threemonths_trend_json = []
    trend_text, ids = extract_id(XRP_event_dict["threemonths"])

    data = {'trend': trend_text, 'period': "threemonths", 'ids': ids}
    crsr.execute(mysql_insert_trend, data)
    topic_id = crsr.lastrowid


    subitem = {}
    subitem["objects"] = trend_text
    subitem["period"] = "threemonths"
    subitem["id"] = topic_id
    threemonths_trend_json.append(subitem)
    XRP_event_dict_plusID["threemonths"] = json.dumps(threemonths_trend_json)






    # recalculate dict
    delete_list = []
    for key in BCH_twelvehours_topic_dict:
        BCH_twelvehours_topic_dict[key] = BCH_twelvehours_topic_dict[key] * (1 - twelvehours_decay_speed)
        BCH_twelvehours_topic_dict[key] -= TWELVEHOURS_DECAY_SPEED_TUNE
        if BCH_twelvehours_topic_dict[key] <= 0:
            delete_list.append(key)
    for l in delete_list:
        BCH_twelvehours_topic_dict.pop(l)
        BCH_twelvehours_id_dict.pop(l)
    # clean lists
    delete_time_list = []
    for t in BCH_twelvehours_time_list:
        if (((Now - datetime.datetime.strptime(t, time_format)).seconds) + ((Now - datetime.datetime.strptime(t, time_format)).days * 86400)) >= TWELVEHOURS_KEEP_TIME:
            delete_time_list.append(t)
    for t in delete_time_list:
        pos = BCH_twelvehours_time_list.index(t)
        headline_id = BCH_twelvehours_ID_list[pos]
        BCH_twelvehours_time_list.pop(pos)
        BCH_twelvehours_ID_list.pop(pos)
        BCH_twelvehours_headline_list.pop(pos)
        BCH_twelvehours_importance_list.pop(pos)
        for items in BCH_twelvehours_id_dict.values():
            if headline_id in items:
                items.remove(headline_id)



    twelvehours_trend = sorted(BCH_twelvehours_topic_dict.items(), key = lambda x:x[1], reverse = True)


    i = 0
    tmp_dict = {}
    tmp_id_dict = {}
    for topic in twelvehours_trend:
        if i >= 500:
            break
        if len(tmp_dict) == 0:
            tmp_dict[topic[0]] = topic[1]
            tmp_id_dict[topic[0]] = BCH_twelvehours_id_dict.get(topic[0])
        else:
            same_id = 0
            is_dup = False
            for exist_key in tmp_id_dict:
                if len(BCH_twelvehours_id_dict.get(topic[0])) != 0:
                    for id in BCH_twelvehours_id_dict.get(topic[0]):

                        if id in tmp_id_dict[exist_key]:
                            same_id += 1
                    if same_id/len(BCH_twelvehours_id_dict.get(topic[0])) >= 0.5:
                        is_dup = True
                        break
                same_id = 0
            if is_dup == False:
                tmp_dict[topic[0]] = topic[1]
                tmp_id_dict[topic[0]] = BCH_twelvehours_id_dict.get(topic[0])


        i += 1



    twelvehours_trend_json = []
    i = 0

    for k in tmp_dict:
        if i >= 15:
            break
        
        subitem = {}
        subitem["text"] = k
        subitem["weight"] = round(tmp_dict[k], 2)
        subitem["ids"] = ','.join(str(e) for e in BCH_twelvehours_id_dict.get(k))
        if len(subitem["ids"]) < 8:
            continue
        twelvehours_trend_json.append(subitem)
        i += 1
    BCH_event_dict["twelvehours"] = json.dumps(twelvehours_trend_json)


    twelvehours_trend_json = []
    trend_text, ids = extract_id(BCH_event_dict["twelvehours"])

    data = {'trend': trend_text, 'period': "twelvehours", 'ids': ids}
    crsr.execute(mysql_insert_trend, data)
    topic_id = crsr.lastrowid


    subitem = {}
    subitem["objects"] = trend_text
    subitem["period"] = "twelvehours"
    subitem["id"] = topic_id
    twelvehours_trend_json.append(subitem)
    BCH_event_dict_plusID["twelvehours"] = json.dumps(twelvehours_trend_json)




    # recalculate dict
    delete_list = []
    for key in BCH_oneday_topic_dict:
        BCH_oneday_topic_dict[key] = BCH_oneday_topic_dict[key] * (1 - oneday_decay_speed)
        BCH_oneday_topic_dict[key] -= ONEDAY_DECAY_SPEED_TUNE
        if BCH_oneday_topic_dict[key] <= 0:
            delete_list.append(key)
    for l in delete_list:
        BCH_oneday_topic_dict.pop(l)
        BCH_oneday_id_dict.pop(l)

    # clean lists
    delete_time_list = []
    for t in BCH_oneday_time_list:
        if (((Now - datetime.datetime.strptime(t, time_format)).seconds) + ((Now - datetime.datetime.strptime(t, time_format)).days * 86400)) >= ONEDAY_KEEP_TIME:
            delete_time_list.append(t)

    for t in delete_time_list:
        pos = BCH_oneday_time_list.index(t)
        headline_id = BCH_oneday_ID_list[pos]
        BCH_oneday_time_list.pop(pos)
        BCH_oneday_ID_list.pop(pos)
        BCH_oneday_headline_list.pop(pos)
        BCH_oneday_importance_list.pop(pos)
        for items in BCH_oneday_id_dict.values():
            if headline_id in items:
                items.remove(headline_id)



    oneday_trend = sorted(BCH_oneday_topic_dict.items(), key = lambda x:x[1], reverse = True)


    i = 0
    tmp_dict = {}
    tmp_id_dict = {}
    for topic in oneday_trend:
        if i >= 500:
            break
        if len(tmp_dict) == 0:
            tmp_dict[topic[0]] = topic[1]
            tmp_id_dict[topic[0]] = BCH_oneday_id_dict.get(topic[0])
        else:
            same_id = 0
            is_dup = False
            for exist_key in tmp_id_dict:
                if len(BCH_oneday_id_dict.get(topic[0])) != 0:
                    for id in BCH_oneday_id_dict.get(topic[0]):

                        if id in tmp_id_dict[exist_key]:
                            same_id += 1
                    if same_id/len(BCH_oneday_id_dict.get(topic[0])) >= 0.5:
                        is_dup = True
                        break
                same_id = 0
            if is_dup == False:
                tmp_dict[topic[0]] = topic[1]
                tmp_id_dict[topic[0]] = BCH_oneday_id_dict.get(topic[0])


        i += 1

    oneday_trend_json = []
    i = 0

    for k in tmp_dict:
        if i >= 15:
            break
        
        subitem = {}
        subitem["text"] = k
        subitem["weight"] = round(tmp_dict[k], 2)
        subitem["ids"] = ','.join(str(e) for e in BCH_oneday_id_dict.get(k))
        if len(subitem["ids"]) < 8:
            continue
        oneday_trend_json.append(subitem)
        i += 1

    BCH_event_dict["oneday"] = json.dumps(oneday_trend_json)


    oneday_trend_json = []
    trend_text, ids = extract_id(BCH_event_dict["oneday"])

    data = {'trend': trend_text, 'period': "oneday", 'ids': ids}
    crsr.execute(mysql_insert_trend, data)
    topic_id = crsr.lastrowid


    subitem = {}
    subitem["objects"] = trend_text
    subitem["period"] = "oneday"
    subitem["id"] = topic_id
    oneday_trend_json.append(subitem)
    BCH_event_dict_plusID["oneday"] = json.dumps(oneday_trend_json)





    # recalculate dict
    delete_list = []
    for key in BCH_oneweek_topic_dict:
        BCH_oneweek_topic_dict[key] = BCH_oneweek_topic_dict[key] * (1 - oneweek_decay_speed)
        BCH_oneweek_topic_dict[key] -= ONEWEEK_DECAY_SPEED_TUNE
        if BCH_oneweek_topic_dict[key] <= 0:
            delete_list.append(key)
    for l in delete_list:
        BCH_oneweek_topic_dict.pop(l)
        BCH_oneweek_id_dict.pop(l)

    # clean lists
    delete_time_list = []
    for t in BCH_oneweek_time_list:
        if (((Now - datetime.datetime.strptime(t, time_format)).seconds) + ((Now - datetime.datetime.strptime(t, time_format)).days * 86400)) >= ONEWEEK_KEEP_TIME:
            delete_time_list.append(t)

    for t in delete_time_list:
        pos = BCH_oneweek_time_list.index(t)
        headline_id = BCH_oneweek_ID_list[pos]
        BCH_oneweek_time_list.pop(pos)
        BCH_oneweek_ID_list.pop(pos)
        BCH_oneweek_headline_list.pop(pos)
        BCH_oneweek_importance_list.pop(pos)
        for items in BCH_oneweek_id_dict.values():
            if headline_id in items:
                items.remove(headline_id)




    oneweek_trend = sorted(BCH_oneweek_topic_dict.items(), key = lambda x:x[1], reverse = True)


    i = 0
    tmp_dict = {}
    tmp_id_dict = {}
    for topic in oneweek_trend:
        if i >= 500:
            break
        if len(tmp_dict) == 0:
            tmp_dict[topic[0]] = topic[1]
            tmp_id_dict[topic[0]] = BCH_oneweek_id_dict.get(topic[0])
        else:
            same_id = 0
            is_dup = False
            for exist_key in tmp_id_dict:
                if len(BCH_oneweek_id_dict.get(topic[0])) != 0:
                    for id in BCH_oneweek_id_dict.get(topic[0]):

                        if id in tmp_id_dict[exist_key]:
                            same_id += 1
                    if same_id/len(BCH_oneweek_id_dict.get(topic[0])) >= 0.5:
                        is_dup = True
                        break
                same_id = 0
            if is_dup == False:
                tmp_dict[topic[0]] = topic[1]
                tmp_id_dict[topic[0]] = BCH_oneweek_id_dict.get(topic[0])


        i += 1

    oneweek_trend_json = []
    i = 0

    for k in tmp_dict:
        if i >= 15:
            break
        
        subitem = {}
        subitem["text"] = k
        subitem["weight"] = round(tmp_dict[k], 2)
        subitem["ids"] = ','.join(str(e) for e in BCH_oneweek_id_dict.get(k))
        if len(subitem["ids"]) < 8:
            continue
        oneweek_trend_json.append(subitem)
        i += 1

    BCH_event_dict["oneweek"] = json.dumps(oneweek_trend_json)


    oneweek_trend_json = []
    trend_text, ids = extract_id(BCH_event_dict["oneweek"])

    data = {'trend': trend_text, 'period': "oneweek", 'ids': ids}
    crsr.execute(mysql_insert_trend, data)
    topic_id = crsr.lastrowid


    subitem = {}
    subitem["objects"] = trend_text
    subitem["period"] = "oneweek"
    subitem["id"] = topic_id
    oneweek_trend_json.append(subitem)
    BCH_event_dict_plusID["oneweek"] = json.dumps(oneweek_trend_json)




    # recalculate dict
    delete_list = []
    for key in BCH_onemonth_topic_dict:
        BCH_onemonth_topic_dict[key] = BCH_onemonth_topic_dict[key] * (1 - onemonth_decay_speed)
        BCH_onemonth_topic_dict[key] -= ONEMONTH_DECAY_SPEED_TUNE
        if BCH_onemonth_topic_dict[key] <= 0:
            delete_list.append(key)
    for l in delete_list:
        BCH_onemonth_topic_dict.pop(l)
        BCH_onemonth_id_dict.pop(l)

    # clean lists
    delete_time_list = []
    for t in BCH_onemonth_time_list:
        if (((Now - datetime.datetime.strptime(t, time_format)).seconds) + ((Now - datetime.datetime.strptime(t, time_format)).days * 86400)) >= ONEMONTH_KEEP_TIME:
            delete_time_list.append(t)

    for t in delete_time_list:
        pos = BCH_onemonth_time_list.index(t)
        headline_id = BCH_onemonth_ID_list[pos]
        BCH_onemonth_time_list.pop(pos)
        BCH_onemonth_ID_list.pop(pos)
        BCH_onemonth_headline_list.pop(pos)
        BCH_onemonth_importance_list.pop(pos)       
        for items in BCH_onemonth_id_dict.values():
            if headline_id in items:
                items.remove(headline_id)

    onemonth_trend = sorted(BCH_onemonth_topic_dict.items(), key = lambda x:x[1], reverse = True)


    i = 0
    tmp_dict = {}
    tmp_id_dict = {}
    for topic in onemonth_trend:
        if i >= 500:
            break
        if len(tmp_dict) == 0:
            tmp_dict[topic[0]] = topic[1]
            tmp_id_dict[topic[0]] = BCH_onemonth_id_dict.get(topic[0])
        else:
            same_id = 0
            is_dup = False
            for exist_key in tmp_id_dict:
                if len(BCH_onemonth_id_dict.get(topic[0])) != 0:
                    for id in BCH_onemonth_id_dict.get(topic[0]):

                        if id in tmp_id_dict[exist_key]:
                            same_id += 1
                    if same_id/len(BCH_onemonth_id_dict.get(topic[0])) >= 0.5:
                        is_dup = True
                        break
                same_id = 0
            if is_dup == False:
                tmp_dict[topic[0]] = topic[1]
                tmp_id_dict[topic[0]] = BCH_onemonth_id_dict.get(topic[0])


        i += 1

    onemonth_trend_json = []
    i = 0

    for k in tmp_dict:
        if i >= 15:
            break
        
        subitem = {}
        subitem["text"] = k
        subitem["weight"] = round(tmp_dict[k], 2)
        subitem["ids"] = ','.join(str(e) for e in BCH_onemonth_id_dict.get(k))
        if len(subitem["ids"]) < 8:
            continue
        onemonth_trend_json.append(subitem)
        i += 1

    BCH_event_dict["onemonth"] = json.dumps(onemonth_trend_json)
    

    onemonth_trend_json = []
    trend_text, ids = extract_id(BCH_event_dict["onemonth"])

    data = {'trend': trend_text, 'period': "onemonth", 'ids': ids}
    crsr.execute(mysql_insert_trend, data)
    topic_id = crsr.lastrowid


    subitem = {}
    subitem["objects"] = trend_text
    subitem["period"] = "onemonth"
    subitem["id"] = topic_id
    onemonth_trend_json.append(subitem)
    BCH_event_dict_plusID["onemonth"] = json.dumps(onemonth_trend_json)




    # recalculate dict
    delete_list = []
    for key in BCH_threemonths_topic_dict:
        BCH_threemonths_topic_dict[key] = BCH_threemonths_topic_dict[key] * (1 - threemonths_decay_speed)
        BCH_threemonths_topic_dict[key] -= THREEMONTHS_DECAY_SPEED_TUNE
        if BCH_threemonths_topic_dict[key] <= 0:
            delete_list.append(key)
    for l in delete_list:
        BCH_threemonths_topic_dict.pop(l)
        BCH_threemonths_id_dict.pop(l)

    # clean lists
    delete_time_list = []
    for t in BCH_threemonths_time_list:
        if (((Now - datetime.datetime.strptime(t, time_format)).seconds) + ((Now - datetime.datetime.strptime(t, time_format)).days * 86400)) >= THREEMONTHS_KEEP_TIME:
            delete_time_list.append(t)

    for t in delete_time_list:
        pos = BCH_threemonths_time_list.index(t)
        headline_id = BCH_threemonths_ID_list[pos]
        BCH_threemonths_time_list.pop(pos)
        BCH_threemonths_ID_list.pop(pos)
        BCH_threemonths_headline_list.pop(pos)
        BCH_threemonths_importance_list.pop(pos)                    
        for items in BCH_threemonths_id_dict.values():
            if headline_id in items:
                items.remove(headline_id)


    threemonths_trend = sorted(BCH_threemonths_topic_dict.items(), key = lambda x:x[1], reverse = True)


    i = 0
    tmp_dict = {}
    tmp_id_dict = {}
    for topic in threemonths_trend:
        if i >= 500:
            break
        if len(tmp_dict) == 0:
            tmp_dict[topic[0]] = topic[1]
            tmp_id_dict[topic[0]] = BCH_threemonths_id_dict.get(topic[0])
        else:
            same_id = 0
            is_dup = False
            for exist_key in tmp_id_dict:
                if len(BCH_threemonths_id_dict.get(topic[0])) != 0:
                    for id in BCH_threemonths_id_dict.get(topic[0]):

                        if id in tmp_id_dict[exist_key]:
                            same_id += 1
                    if same_id/len(BCH_threemonths_id_dict.get(topic[0])) >= 0.5:
                        is_dup = True
                        break
                same_id = 0
            if is_dup == False:
                tmp_dict[topic[0]] = topic[1]
                tmp_id_dict[topic[0]] = BCH_threemonths_id_dict.get(topic[0])


        i += 1

    threemonths_trend_json = []
    i = 0

    for k in tmp_dict:
        if i >= 15:
            break
        
        subitem = {}
        subitem["text"] = k
        subitem["weight"] = round(tmp_dict[k], 2)
        subitem["ids"] = ','.join(str(e) for e in BCH_threemonths_id_dict.get(k))
        if len(subitem["ids"]) < 8:
            continue
        threemonths_trend_json.append(subitem)
        i += 1

    BCH_event_dict["threemonths"] = json.dumps(threemonths_trend_json)


    threemonths_trend_json = []
    trend_text, ids = extract_id(BCH_event_dict["threemonths"])

    data = {'trend': trend_text, 'period': "threemonths", 'ids': ids}
    crsr.execute(mysql_insert_trend, data)
    topic_id = crsr.lastrowid


    subitem = {}
    subitem["objects"] = trend_text
    subitem["period"] = "threemonths"
    subitem["id"] = topic_id
    threemonths_trend_json.append(subitem)
    BCH_event_dict_plusID["threemonths"] = json.dumps(threemonths_trend_json)







    # recalculate dict
    delete_list = []
    for key in LTC_twelvehours_topic_dict:
        LTC_twelvehours_topic_dict[key] = LTC_twelvehours_topic_dict[key] * (1 - twelvehours_decay_speed)
        LTC_twelvehours_topic_dict[key] -= TWELVEHOURS_DECAY_SPEED_TUNE
        if LTC_twelvehours_topic_dict[key] <= 0:
            delete_list.append(key)
    for l in delete_list:
        LTC_twelvehours_topic_dict.pop(l)
        LTC_twelvehours_id_dict.pop(l)
    # clean lists
    delete_time_list = []
    for t in LTC_twelvehours_time_list:
        if (((Now - datetime.datetime.strptime(t, time_format)).seconds) + ((Now - datetime.datetime.strptime(t, time_format)).days * 86400)) >= TWELVEHOURS_KEEP_TIME:
            delete_time_list.append(t)
    for t in delete_time_list:
        pos = LTC_twelvehours_time_list.index(t)
        headline_id = LTC_twelvehours_ID_list[pos]
        LTC_twelvehours_time_list.pop(pos)
        LTC_twelvehours_ID_list.pop(pos)
        LTC_twelvehours_headline_list.pop(pos)
        LTC_twelvehours_importance_list.pop(pos)
        for items in LTC_twelvehours_id_dict.values():
            if headline_id in items:
                items.remove(headline_id)



    twelvehours_trend = sorted(LTC_twelvehours_topic_dict.items(), key = lambda x:x[1], reverse = True)


    i = 0
    tmp_dict = {}
    tmp_id_dict = {}
    for topic in twelvehours_trend:
        if i >= 500:
            break
        if len(tmp_dict) == 0:
            tmp_dict[topic[0]] = topic[1]
            tmp_id_dict[topic[0]] = LTC_twelvehours_id_dict.get(topic[0])
        else:
            same_id = 0
            is_dup = False
            for exist_key in tmp_id_dict:
                if len(LTC_twelvehours_id_dict.get(topic[0])) != 0:
                    for id in LTC_twelvehours_id_dict.get(topic[0]):

                        if id in tmp_id_dict[exist_key]:
                            same_id += 1
                    if same_id/len(LTC_twelvehours_id_dict.get(topic[0])) >= 0.5:
                        is_dup = True
                        break
                same_id = 0
            if is_dup == False:
                tmp_dict[topic[0]] = topic[1]
                tmp_id_dict[topic[0]] = LTC_twelvehours_id_dict.get(topic[0])


        i += 1



    twelvehours_trend_json = []
    i = 0

    for k in tmp_dict:
        if i >= 15:
            break
        
        subitem = {}
        subitem["text"] = k
        subitem["weight"] = round(tmp_dict[k], 2)
        subitem["ids"] = ','.join(str(e) for e in LTC_twelvehours_id_dict.get(k))
        if len(subitem["ids"]) < 8:
            continue
        twelvehours_trend_json.append(subitem)
        i += 1
    LTC_event_dict["twelvehours"] = json.dumps(twelvehours_trend_json)


    twelvehours_trend_json = []
    trend_text, ids = extract_id(LTC_event_dict["twelvehours"])

    data = {'trend': trend_text, 'period': "twelvehours", 'ids': ids}
    crsr.execute(mysql_insert_trend, data)
    topic_id = crsr.lastrowid


    subitem = {}
    subitem["objects"] = trend_text
    subitem["period"] = "twelvehours"
    subitem["id"] = topic_id
    twelvehours_trend_json.append(subitem)
    LTC_event_dict_plusID["twelvehours"] = json.dumps(twelvehours_trend_json)




    # recalculate dict
    delete_list = []
    for key in LTC_oneday_topic_dict:
        LTC_oneday_topic_dict[key] = LTC_oneday_topic_dict[key] * (1 - oneday_decay_speed)
        LTC_oneday_topic_dict[key] -= ONEDAY_DECAY_SPEED_TUNE
        if LTC_oneday_topic_dict[key] <= 0:
            delete_list.append(key)
    for l in delete_list:
        LTC_oneday_topic_dict.pop(l)
        LTC_oneday_id_dict.pop(l)

    # clean lists
    delete_time_list = []
    for t in LTC_oneday_time_list:
        if (((Now - datetime.datetime.strptime(t, time_format)).seconds) + ((Now - datetime.datetime.strptime(t, time_format)).days * 86400)) >= ONEDAY_KEEP_TIME:
            delete_time_list.append(t)

    for t in delete_time_list:
        pos = LTC_oneday_time_list.index(t)
        headline_id = LTC_oneday_ID_list[pos]
        LTC_oneday_time_list.pop(pos)
        LTC_oneday_ID_list.pop(pos)
        LTC_oneday_headline_list.pop(pos)
        LTC_oneday_importance_list.pop(pos)
        for items in LTC_oneday_id_dict.values():
            if headline_id in items:
                items.remove(headline_id)



    oneday_trend = sorted(LTC_oneday_topic_dict.items(), key = lambda x:x[1], reverse = True)


    i = 0
    tmp_dict = {}
    tmp_id_dict = {}
    for topic in oneday_trend:
        if i >= 500:
            break
        if len(tmp_dict) == 0:
            tmp_dict[topic[0]] = topic[1]
            tmp_id_dict[topic[0]] = LTC_oneday_id_dict.get(topic[0])
        else:
            same_id = 0
            is_dup = False
            for exist_key in tmp_id_dict:
                if len(LTC_oneday_id_dict.get(topic[0])) != 0:
                    for id in LTC_oneday_id_dict.get(topic[0]):

                        if id in tmp_id_dict[exist_key]:
                            same_id += 1
                    if same_id/len(LTC_oneday_id_dict.get(topic[0])) >= 0.5:
                        is_dup = True
                        break
                same_id = 0
            if is_dup == False:
                tmp_dict[topic[0]] = topic[1]
                tmp_id_dict[topic[0]] = LTC_oneday_id_dict.get(topic[0])


        i += 1

    oneday_trend_json = []
    i = 0

    for k in tmp_dict:
        if i >= 15:
            break
        
        subitem = {}
        subitem["text"] = k
        subitem["weight"] = round(tmp_dict[k], 2)
        subitem["ids"] = ','.join(str(e) for e in LTC_oneday_id_dict.get(k))
        if len(subitem["ids"]) < 8:
            continue
        oneday_trend_json.append(subitem)
        i += 1

    LTC_event_dict["oneday"] = json.dumps(oneday_trend_json)


    oneday_trend_json = []
    trend_text, ids = extract_id(LTC_event_dict["oneday"])

    data = {'trend': trend_text, 'period': "oneday", 'ids': ids}
    crsr.execute(mysql_insert_trend, data)
    topic_id = crsr.lastrowid


    subitem = {}
    subitem["objects"] = trend_text
    subitem["period"] = "oneday"
    subitem["id"] = topic_id
    oneday_trend_json.append(subitem)
    LTC_event_dict_plusID["oneday"] = json.dumps(oneday_trend_json)





    # recalculate dict
    delete_list = []
    for key in LTC_oneweek_topic_dict:
        LTC_oneweek_topic_dict[key] = LTC_oneweek_topic_dict[key] * (1 - oneweek_decay_speed)
        LTC_oneweek_topic_dict[key] -= ONEWEEK_DECAY_SPEED_TUNE
        if LTC_oneweek_topic_dict[key] <= 0:
            delete_list.append(key)
    for l in delete_list:
        LTC_oneweek_topic_dict.pop(l)
        LTC_oneweek_id_dict.pop(l)

    # clean lists
    delete_time_list = []
    for t in LTC_oneweek_time_list:
        if (((Now - datetime.datetime.strptime(t, time_format)).seconds) + ((Now - datetime.datetime.strptime(t, time_format)).days * 86400)) >= ONEWEEK_KEEP_TIME:
            delete_time_list.append(t)

    for t in delete_time_list:
        pos = LTC_oneweek_time_list.index(t)
        headline_id = LTC_oneweek_ID_list[pos]
        LTC_oneweek_time_list.pop(pos)
        LTC_oneweek_ID_list.pop(pos)
        LTC_oneweek_headline_list.pop(pos)
        LTC_oneweek_importance_list.pop(pos)
        for items in LTC_oneweek_id_dict.values():
            if headline_id in items:
                items.remove(headline_id)




    oneweek_trend = sorted(LTC_oneweek_topic_dict.items(), key = lambda x:x[1], reverse = True)


    i = 0
    tmp_dict = {}
    tmp_id_dict = {}
    for topic in oneweek_trend:
        if i >= 500:
            break
        if len(tmp_dict) == 0:
            tmp_dict[topic[0]] = topic[1]
            tmp_id_dict[topic[0]] = LTC_oneweek_id_dict.get(topic[0])
        else:
            same_id = 0
            is_dup = False
            for exist_key in tmp_id_dict:
                if len(LTC_oneweek_id_dict.get(topic[0])) != 0:
                    for id in LTC_oneweek_id_dict.get(topic[0]):

                        if id in tmp_id_dict[exist_key]:
                            same_id += 1
                    if same_id/len(LTC_oneweek_id_dict.get(topic[0])) >= 0.5:
                        is_dup = True
                        break
                same_id = 0
            if is_dup == False:
                tmp_dict[topic[0]] = topic[1]
                tmp_id_dict[topic[0]] = LTC_oneweek_id_dict.get(topic[0])


        i += 1

    oneweek_trend_json = []
    i = 0

    for k in tmp_dict:
        if i >= 15:
            break
        
        subitem = {}
        subitem["text"] = k
        subitem["weight"] = round(tmp_dict[k], 2)
        subitem["ids"] = ','.join(str(e) for e in LTC_oneweek_id_dict.get(k))
        if len(subitem["ids"]) < 8:
            continue
        oneweek_trend_json.append(subitem)
        i += 1

    LTC_event_dict["oneweek"] = json.dumps(oneweek_trend_json)


    oneweek_trend_json = []
    trend_text, ids = extract_id(LTC_event_dict["oneweek"])

    data = {'trend': trend_text, 'period': "oneweek", 'ids': ids}
    crsr.execute(mysql_insert_trend, data)
    topic_id = crsr.lastrowid


    subitem = {}
    subitem["objects"] = trend_text
    subitem["period"] = "oneweek"
    subitem["id"] = topic_id
    oneweek_trend_json.append(subitem)
    LTC_event_dict_plusID["oneweek"] = json.dumps(oneweek_trend_json)




    # recalculate dict
    delete_list = []
    for key in LTC_onemonth_topic_dict:
        LTC_onemonth_topic_dict[key] = LTC_onemonth_topic_dict[key] * (1 - onemonth_decay_speed)
        LTC_onemonth_topic_dict[key] -= ONEMONTH_DECAY_SPEED_TUNE
        if LTC_onemonth_topic_dict[key] <= 0:
            delete_list.append(key)
    for l in delete_list:
        LTC_onemonth_topic_dict.pop(l)
        LTC_onemonth_id_dict.pop(l)

    # clean lists
    delete_time_list = []
    for t in LTC_onemonth_time_list:
        if (((Now - datetime.datetime.strptime(t, time_format)).seconds) + ((Now - datetime.datetime.strptime(t, time_format)).days * 86400)) >= ONEMONTH_KEEP_TIME:
            delete_time_list.append(t)

    for t in delete_time_list:
        pos = LTC_onemonth_time_list.index(t)
        headline_id = LTC_onemonth_ID_list[pos]
        LTC_onemonth_time_list.pop(pos)
        LTC_onemonth_ID_list.pop(pos)
        LTC_onemonth_headline_list.pop(pos)
        LTC_onemonth_importance_list.pop(pos)       
        for items in LTC_onemonth_id_dict.values():
            if headline_id in items:
                items.remove(headline_id)

    onemonth_trend = sorted(LTC_onemonth_topic_dict.items(), key = lambda x:x[1], reverse = True)


    i = 0
    tmp_dict = {}
    tmp_id_dict = {}
    for topic in onemonth_trend:
        if i >= 500:
            break
        if len(tmp_dict) == 0:
            tmp_dict[topic[0]] = topic[1]
            tmp_id_dict[topic[0]] = LTC_onemonth_id_dict.get(topic[0])
        else:
            same_id = 0
            is_dup = False
            for exist_key in tmp_id_dict:
                if len(LTC_onemonth_id_dict.get(topic[0])) != 0:
                    for id in LTC_onemonth_id_dict.get(topic[0]):

                        if id in tmp_id_dict[exist_key]:
                            same_id += 1
                    if same_id/len(LTC_onemonth_id_dict.get(topic[0])) >= 0.5:
                        is_dup = True
                        break
                same_id = 0
            if is_dup == False:
                tmp_dict[topic[0]] = topic[1]
                tmp_id_dict[topic[0]] = LTC_onemonth_id_dict.get(topic[0])


        i += 1

    onemonth_trend_json = []
    i = 0

    for k in tmp_dict:
        if i >= 15:
            break
        
        subitem = {}
        subitem["text"] = k
        subitem["weight"] = round(tmp_dict[k], 2)
        subitem["ids"] = ','.join(str(e) for e in LTC_onemonth_id_dict.get(k))
        if len(subitem["ids"]) < 8:
            continue
        onemonth_trend_json.append(subitem)
        i += 1

    LTC_event_dict["onemonth"] = json.dumps(onemonth_trend_json)
    

    onemonth_trend_json = []
    trend_text, ids = extract_id(LTC_event_dict["onemonth"])

    data = {'trend': trend_text, 'period': "onemonth", 'ids': ids}
    crsr.execute(mysql_insert_trend, data)
    topic_id = crsr.lastrowid


    subitem = {}
    subitem["objects"] = trend_text
    subitem["period"] = "onemonth"
    subitem["id"] = topic_id
    onemonth_trend_json.append(subitem)
    LTC_event_dict_plusID["onemonth"] = json.dumps(onemonth_trend_json)




    # recalculate dict
    delete_list = []
    for key in LTC_threemonths_topic_dict:
        LTC_threemonths_topic_dict[key] = LTC_threemonths_topic_dict[key] * (1 - threemonths_decay_speed)
        LTC_threemonths_topic_dict[key] -= THREEMONTHS_DECAY_SPEED_TUNE
        if LTC_threemonths_topic_dict[key] <= 0:
            delete_list.append(key)
    for l in delete_list:
        LTC_threemonths_topic_dict.pop(l)
        LTC_threemonths_id_dict.pop(l)

    # clean lists
    delete_time_list = []
    for t in LTC_threemonths_time_list:
        if (((Now - datetime.datetime.strptime(t, time_format)).seconds) + ((Now - datetime.datetime.strptime(t, time_format)).days * 86400)) >= THREEMONTHS_KEEP_TIME:
            delete_time_list.append(t)

    for t in delete_time_list:
        pos = LTC_threemonths_time_list.index(t)
        headline_id = LTC_threemonths_ID_list[pos]
        LTC_threemonths_time_list.pop(pos)
        LTC_threemonths_ID_list.pop(pos)
        LTC_threemonths_headline_list.pop(pos)
        LTC_threemonths_importance_list.pop(pos)                    
        for items in LTC_threemonths_id_dict.values():
            if headline_id in items:
                items.remove(headline_id)


    threemonths_trend = sorted(LTC_threemonths_topic_dict.items(), key = lambda x:x[1], reverse = True)


    i = 0
    tmp_dict = {}
    tmp_id_dict = {}
    for topic in threemonths_trend:
        if i >= 500:
            break
        if len(tmp_dict) == 0:
            tmp_dict[topic[0]] = topic[1]
            tmp_id_dict[topic[0]] = LTC_threemonths_id_dict.get(topic[0])
        else:
            same_id = 0
            is_dup = False
            for exist_key in tmp_id_dict:
                if len(LTC_threemonths_id_dict.get(topic[0])) != 0:
                    for id in LTC_threemonths_id_dict.get(topic[0]):

                        if id in tmp_id_dict[exist_key]:
                            same_id += 1
                    if same_id/len(LTC_threemonths_id_dict.get(topic[0])) >= 0.5:
                        is_dup = True
                        break
                same_id = 0
            if is_dup == False:
                tmp_dict[topic[0]] = topic[1]
                tmp_id_dict[topic[0]] = LTC_threemonths_id_dict.get(topic[0])


        i += 1

    threemonths_trend_json = []
    i = 0

    for k in tmp_dict:
        if i >= 15:
            break
        
        subitem = {}
        subitem["text"] = k
        subitem["weight"] = round(tmp_dict[k], 2)
        subitem["ids"] = ','.join(str(e) for e in LTC_threemonths_id_dict.get(k))
        if len(subitem["ids"]) < 8:
            continue
        threemonths_trend_json.append(subitem)
        i += 1

    LTC_event_dict["threemonths"] = json.dumps(threemonths_trend_json)


    threemonths_trend_json = []
    trend_text, ids = extract_id(LTC_event_dict["threemonths"])

    data = {'trend': trend_text, 'period': "threemonths", 'ids': ids}
    crsr.execute(mysql_insert_trend, data)
    topic_id = crsr.lastrowid


    subitem = {}
    subitem["objects"] = trend_text
    subitem["period"] = "threemonths"
    subitem["id"] = topic_id
    threemonths_trend_json.append(subitem)
    LTC_event_dict_plusID["threemonths"] = json.dumps(threemonths_trend_json)







    cnx.commit()

    insert_new()

    

def insert_new():
    
    global BTC_tmp_headline_list, ETH_tmp_headline_list, XRP_tmp_headline_list, BCH_tmp_headline_list, LTC_tmp_headline_list
    for new_head in BTC_tmp_headline_list:
        
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
        

        # maunually set new importance to 3, waiting for Diego's change
        # ====================================================================================================================   
        # ====================================================================================================================   
        BTC_twelvehours_importance_list.append(3.0)
        BTC_oneday_importance_list.append(3.0)
        BTC_oneweek_importance_list.append(3.0)
        BTC_onemonth_importance_list.append(3.0)
        BTC_threemonths_importance_list.append(3.0)
        # ====================================================================================================================   
        # ====================================================================================================================
        
        BTC_twelvehours_headline_list.append(topic_list)
        BTC_twelvehours_time_list.append(new_headline_time)
        BTC_twelvehours_ID_list.append(new_ID)
        BTC_oneday_headline_list.append(topic_list)
        BTC_oneday_time_list.append(new_headline_time)
        BTC_oneday_ID_list.append(new_ID)
        BTC_oneweek_headline_list.append(topic_list)
        BTC_oneweek_time_list.append(new_headline_time)
        BTC_oneweek_ID_list.append(new_ID)
        BTC_onemonth_headline_list.append(topic_list)
        BTC_onemonth_time_list.append(new_headline_time)
        BTC_onemonth_ID_list.append(new_ID)
        BTC_threemonths_headline_list.append(topic_list)
        BTC_threemonths_time_list.append(new_headline_time)
        BTC_threemonths_ID_list.append(new_ID)

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
                
                if BTC_twelvehours_topic_dict.get(topic_list[i]) == None:
                    if is_hashtag == True:
                        BTC_twelvehours_topic_dict[topic_list[i]] = new_headline_importance * enhance_weight * HASHTAG_PENALTY
                    else:
                        BTC_twelvehours_topic_dict[topic_list[i]] = new_headline_importance * enhance_weight
                else:
                    if is_hashtag == True:
                        BTC_twelvehours_topic_dict[topic_list[i]] = BTC_twelvehours_topic_dict.get(topic_list[i]) + new_headline_importance * enhance_weight * HASHTAG_PENALTY
                    else:
                        BTC_twelvehours_topic_dict[topic_list[i]] = BTC_twelvehours_topic_dict.get(topic_list[i]) + new_headline_importance * enhance_weight             

                # Add new id in dictionary
                if BTC_twelvehours_id_dict.get(topic_list[i]) == None:
                    l = [new_ID]
                    BTC_twelvehours_id_dict[topic_list[i]] = l
                else:
                    BTC_twelvehours_id_dict[topic_list[i]].append(new_ID)


                if BTC_oneday_topic_dict.get(topic_list[i]) == None:
                    if is_hashtag == True:
                        BTC_oneday_topic_dict[topic_list[i]] = new_headline_importance * enhance_weight * HASHTAG_PENALTY
                    else:
                        BTC_oneday_topic_dict[topic_list[i]] = new_headline_importance * enhance_weight
                else:
                    if is_hashtag == True:
                        BTC_oneday_topic_dict[topic_list[i]] = BTC_oneday_topic_dict.get(topic_list[i]) + new_headline_importance * enhance_weight * HASHTAG_PENALTY
                    else:
                        BTC_oneday_topic_dict[topic_list[i]] = BTC_oneday_topic_dict.get(topic_list[i]) + new_headline_importance * enhance_weight

                # Add new id in dictionary
                if BTC_oneday_id_dict.get(topic_list[i]) == None:
                    l = [new_ID]
                    BTC_oneday_id_dict[topic_list[i]] = l
                else:
                    BTC_oneday_id_dict[topic_list[i]].append(new_ID)


                if BTC_oneweek_topic_dict.get(topic_list[i]) == None:
                    if is_hashtag == True:
                        BTC_oneweek_topic_dict[topic_list[i]] = new_headline_importance * enhance_weight * HASHTAG_PENALTY
                    else:
                        BTC_oneweek_topic_dict[topic_list[i]] = new_headline_importance * enhance_weight
                else:
                    if is_hashtag == True:
                        BTC_oneweek_topic_dict[topic_list[i]] = BTC_oneweek_topic_dict.get(topic_list[i]) + new_headline_importance * enhance_weight * HASHTAG_PENALTY
                    else:
                        BTC_oneweek_topic_dict[topic_list[i]] = BTC_oneweek_topic_dict.get(topic_list[i]) + new_headline_importance * enhance_weight

                # Add new id in dictionary
                if BTC_oneweek_id_dict.get(topic_list[i]) == None:
                    l = [new_ID]
                    BTC_oneweek_id_dict[topic_list[i]] = l
                else:
                    BTC_oneweek_id_dict[topic_list[i]].append(new_ID)


                if BTC_onemonth_topic_dict.get(topic_list[i]) == None:
                    if is_hashtag == True:
                        BTC_onemonth_topic_dict[topic_list[i]] = new_headline_importance * enhance_weight * HASHTAG_PENALTY
                    else:
                        BTC_onemonth_topic_dict[topic_list[i]] = new_headline_importance * enhance_weight
                else:
                    if is_hashtag == True:
                        BTC_onemonth_topic_dict[topic_list[i]] = BTC_onemonth_topic_dict.get(topic_list[i]) + new_headline_importance * enhance_weight * HASHTAG_PENALTY
                    else:
                        BTC_onemonth_topic_dict[topic_list[i]] = BTC_onemonth_topic_dict.get(topic_list[i]) + new_headline_importance * enhance_weight

                # Add new id in dictionary
                if BTC_onemonth_id_dict.get(topic_list[i]) == None:
                    l = [new_ID]
                    BTC_onemonth_id_dict[topic_list[i]] = l
                else:
                    BTC_onemonth_id_dict[topic_list[i]].append(new_ID)



                if BTC_threemonths_topic_dict.get(topic_list[i]) == None:
                    if is_hashtag == True:
                        BTC_threemonths_topic_dict[topic_list[i]] = new_headline_importance * enhance_weight * HASHTAG_PENALTY
                    else:
                        BTC_threemonths_topic_dict[topic_list[i]] = new_headline_importance * enhance_weight
                else:
                    if is_hashtag == True:
                        BTC_threemonths_topic_dict[topic_list[i]] = BTC_threemonths_topic_dict.get(topic_list[i]) + new_headline_importance * enhance_weight * HASHTAG_PENALTY
                    else:
                        BTC_threemonths_topic_dict[topic_list[i]] = BTC_threemonths_topic_dict.get(topic_list[i]) + new_headline_importance * enhance_weight

                # Add new id in dictionary
                if BTC_threemonths_id_dict.get(topic_list[i]) == None:
                    l = [new_ID]
                    BTC_threemonths_id_dict[topic_list[i]] = l
                else:
                    BTC_threemonths_id_dict[topic_list[i]].append(new_ID)

        twelvehours_trend = sorted(BTC_twelvehours_topic_dict.items(), key = lambda x:x[1], reverse = True)
        oneday_trend = sorted(BTC_oneday_topic_dict.items(), key = lambda x:x[1], reverse = True)
        oneweek_trend = sorted(BTC_oneweek_topic_dict.items(), key = lambda x:x[1], reverse = True)
        onemonth_trend = sorted(BTC_onemonth_topic_dict.items(), key = lambda x:x[1], reverse = True)
        threemonths_trend = sorted(BTC_threemonths_topic_dict.items(), key = lambda x:x[1], reverse = True)
        # don't show topics from same headlines
        i = 0
        tmp_dict = {}
        tmp_id_dict = {}
        
        
        i = 0
        tmp_dict = {}
        tmp_id_dict = {}
        for topic in twelvehours_trend:
            # print("i is: " +str(i))
            if i >= 500:
                break 
            if len(tmp_dict) == 0:

                tmp_dict[topic[0]] = topic[1]
                tmp_id_dict[topic[0]] = BTC_twelvehours_id_dict.get(topic[0])
            else:

                same_id = 0
                is_dup = False
                for exist_key in tmp_id_dict:
                    for id in BTC_twelvehours_id_dict.get(topic[0]):
                        if id in tmp_id_dict[exist_key]:
                            same_id += 1
                    if same_id/len(BTC_twelvehours_id_dict.get(topic[0])) >= 0.5:
                        is_dup = True
                        break
                    same_id = 0

                if is_dup == False:
                    tmp_dict[topic[0]] = topic[1]
                    tmp_id_dict[topic[0]] = BTC_twelvehours_id_dict.get(topic[0])
            i += 1

        twelvehours_trend_json = []
        i = 0
        
        for k in tmp_dict:
            if i >= 15:
                break
            subitem = {}
            subitem["text"] = k
            subitem["weight"] = round(tmp_dict[k], 2)
            subitem["ids"] = ','.join(str(e) for e in BTC_twelvehours_id_dict.get(k))
            if len(subitem["ids"]) < 8:
                continue
            twelvehours_trend_json.append(subitem)
            i += 1

        BTC_event_dict["twelvehours"] = json.dumps(twelvehours_trend_json)
        

        i = 0
        tmp_dict = {}
        tmp_id_dict = {}
        for topic in oneday_trend:
            if i >= 300:
                break
            if len(tmp_dict) == 0:
                tmp_dict[topic[0]] = topic[1]
                tmp_id_dict[topic[0]] = BTC_oneday_id_dict.get(topic[0])
            else:
                same_id = 0
                is_dup = False
                for exist_key in tmp_id_dict:
                    for id in BTC_oneday_id_dict.get(topic[0]):
                        if id in tmp_id_dict[exist_key]:
                            same_id += 1
                    if same_id/len(BTC_oneday_id_dict.get(topic[0])) >= 0.5:
                        is_dup = True
                        break
                    same_id = 0
                if is_dup == False:
                    tmp_dict[topic[0]] = topic[1]
                    tmp_id_dict[topic[0]] = BTC_oneday_id_dict.get(topic[0])

            i += 1
    
        oneday_trend_json = []
        i = 0
        for k in tmp_dict:
            if i >= 15:
                break
            subitem = {}
            subitem["text"] = k
            subitem["weight"] = round(tmp_dict[k], 2)
            subitem["ids"] = ','.join(str(e) for e in BTC_oneday_id_dict.get(k))
            if len(subitem["ids"]) < 8:
                continue
            oneday_trend_json.append(subitem)
            i += 1

        BTC_event_dict["oneday"] = json.dumps(oneday_trend_json)


        i = 0
        tmp_dict = {}
        tmp_id_dict = {}
        for topic in oneweek_trend:
            if i >= 300:
                break
            if len(tmp_dict) == 0:
                tmp_dict[topic[0]] = topic[1]
                tmp_id_dict[topic[0]] = BTC_oneweek_id_dict.get(topic[0])
            else:
                same_id = 0
                is_dup = False
                for exist_key in tmp_id_dict:
                    for id in BTC_oneweek_id_dict.get(topic[0]):
                        if id in tmp_id_dict[exist_key]:
                            same_id += 1
                    if same_id/len(BTC_oneweek_id_dict.get(topic[0])) >= 0.5:
                        is_dup = True
                        break
                    same_id = 0
                if is_dup == False:
                    tmp_dict[topic[0]] = topic[1]
                    tmp_id_dict[topic[0]] = BTC_oneweek_id_dict.get(topic[0])

            i += 1

        oneweek_trend_json = []
        i = 0
        for k in tmp_dict:
            if i >= 15:
                break
            subitem = {}
            subitem["text"] = k
            subitem["weight"] = round(tmp_dict[k], 2)
            subitem["ids"] = ','.join(str(e) for e in BTC_oneweek_id_dict.get(k))
            if len(subitem["ids"]) < 8:
                continue
            oneweek_trend_json.append(subitem)
            i += 1

        BTC_event_dict["oneweek"] = json.dumps(oneweek_trend_json)


        i = 0
        tmp_dict = {}
        tmp_id_dict = {}
        for topic in onemonth_trend:
            if i >= 300:
                break
            if len(tmp_dict) == 0:
                tmp_dict[topic[0]] = topic[1]
                tmp_id_dict[topic[0]] = BTC_onemonth_id_dict.get(topic[0])
            else:
                same_id = 0
                is_dup = False
                for exist_key in tmp_id_dict:
                    for id in BTC_onemonth_id_dict.get(topic[0]):
                        if id in tmp_id_dict[exist_key]:
                            same_id += 1
                    if same_id/len(BTC_onemonth_id_dict.get(topic[0])) >= 0.5:
                        is_dup = True
                        break
                    same_id = 0
                if is_dup == False:
                    tmp_dict[topic[0]] = topic[1]
                    tmp_id_dict[topic[0]] = BTC_onemonth_id_dict.get(topic[0])

            i += 1

        onemonth_trend_json = []
        i = 0
        for k in tmp_dict:
            if i >= 15:
                break
            subitem = {}
            subitem["text"] = k
            subitem["weight"] = round(tmp_dict[k], 2)
            subitem["ids"] = ','.join(str(e) for e in BTC_onemonth_id_dict.get(k))
            if len(subitem["ids"]) < 8:
                continue
            onemonth_trend_json.append(subitem)
            i += 1

        BTC_event_dict["onemonth"] = json.dumps(onemonth_trend_json)


        i = 0
        tmp_dict = {}
        tmp_id_dict = {}
        for topic in threemonths_trend:
            if i >= 300:
                break
            if len(tmp_dict) == 0:
                tmp_dict[topic[0]] = topic[1]
                tmp_id_dict[topic[0]] = BTC_threemonths_id_dict.get(topic[0])
            else:
                same_id = 0
                is_dup = False
                for exist_key in tmp_id_dict:
                    for id in BTC_threemonths_id_dict.get(topic[0]):
                        if id in tmp_id_dict[exist_key]:
                            same_id += 1
                    if same_id/len(BTC_threemonths_id_dict.get(topic[0])) >= 0.5:
                        is_dup = True
                        break
                    same_id = 0
                if is_dup == False:
                    tmp_dict[topic[0]] = topic[1]
                    tmp_id_dict[topic[0]] = BTC_threemonths_id_dict.get(topic[0])

            i += 1

        threemonths_trend_json = []
        i = 0
        for k in tmp_dict:
            if i >= 15:
                break
            subitem = {}
            subitem["text"] = k
            subitem["weight"] = round(tmp_dict[k], 2)
            subitem["ids"] = ','.join(str(e) for e in BTC_threemonths_id_dict.get(k))
            if len(subitem["ids"]) < 8:
                continue
            threemonths_trend_json.append(subitem)
            i += 1

        BTC_event_dict["threemonths"] = json.dumps(threemonths_trend_json)
        
        add_to_mysql()

    for new_head in ETH_tmp_headline_list:
        
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
        

        # maunually set new importance to 3, waiting for Diego's change
        # ====================================================================================================================   
        # ====================================================================================================================   
        ETH_twelvehours_importance_list.append(3.0)
        ETH_oneday_importance_list.append(3.0)
        ETH_oneweek_importance_list.append(3.0)
        ETH_onemonth_importance_list.append(3.0)
        ETH_threemonths_importance_list.append(3.0)
        # ====================================================================================================================   
        # ====================================================================================================================
        
        ETH_twelvehours_headline_list.append(topic_list)
        ETH_twelvehours_time_list.append(new_headline_time)
        ETH_twelvehours_ID_list.append(new_ID)
        ETH_oneday_headline_list.append(topic_list)
        ETH_oneday_time_list.append(new_headline_time)
        ETH_oneday_ID_list.append(new_ID)
        ETH_oneweek_headline_list.append(topic_list)
        ETH_oneweek_time_list.append(new_headline_time)
        ETH_oneweek_ID_list.append(new_ID)
        ETH_onemonth_headline_list.append(topic_list)
        ETH_onemonth_time_list.append(new_headline_time)
        ETH_onemonth_ID_list.append(new_ID)
        ETH_threemonths_headline_list.append(topic_list)
        ETH_threemonths_time_list.append(new_headline_time)
        ETH_threemonths_ID_list.append(new_ID)

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
                


                if ETH_twelvehours_topic_dict.get(topic_list[i]) == None:
                    if is_hashtag == True:
                        ETH_twelvehours_topic_dict[topic_list[i]] = new_headline_importance * enhance_weight * HASHTAG_PENALTY
                    else:
                        ETH_twelvehours_topic_dict[topic_list[i]] = new_headline_importance * enhance_weight
                else:
                    if is_hashtag == True:
                        ETH_twelvehours_topic_dict[topic_list[i]] = ETH_twelvehours_topic_dict.get(topic_list[i]) + new_headline_importance * enhance_weight * HASHTAG_PENALTY
                    else:
                        ETH_twelvehours_topic_dict[topic_list[i]] = ETH_twelvehours_topic_dict.get(topic_list[i]) + new_headline_importance * enhance_weight             

                # Add new id in dictionary
                if ETH_twelvehours_id_dict.get(topic_list[i]) == None:
                    l = [new_ID]
                    ETH_twelvehours_id_dict[topic_list[i]] = l
                else:
                    ETH_twelvehours_id_dict[topic_list[i]].append(new_ID)


                if ETH_oneday_topic_dict.get(topic_list[i]) == None:
                    if is_hashtag == True:
                        ETH_oneday_topic_dict[topic_list[i]] = new_headline_importance * enhance_weight * HASHTAG_PENALTY
                    else:
                        ETH_oneday_topic_dict[topic_list[i]] = new_headline_importance * enhance_weight
                else:
                    if is_hashtag == True:
                        ETH_oneday_topic_dict[topic_list[i]] = ETH_oneday_topic_dict.get(topic_list[i]) + new_headline_importance * enhance_weight * HASHTAG_PENALTY
                    else:
                        ETH_oneday_topic_dict[topic_list[i]] = ETH_oneday_topic_dict.get(topic_list[i]) + new_headline_importance * enhance_weight

                # Add new id in dictionary
                if ETH_oneday_id_dict.get(topic_list[i]) == None:
                    l = [new_ID]
                    ETH_oneday_id_dict[topic_list[i]] = l
                else:
                    ETH_oneday_id_dict[topic_list[i]].append(new_ID)


                if ETH_oneweek_topic_dict.get(topic_list[i]) == None:
                    if is_hashtag == True:
                        ETH_oneweek_topic_dict[topic_list[i]] = new_headline_importance * enhance_weight * HASHTAG_PENALTY
                    else:
                        ETH_oneweek_topic_dict[topic_list[i]] = new_headline_importance * enhance_weight
                else:
                    if is_hashtag == True:
                        ETH_oneweek_topic_dict[topic_list[i]] = ETH_oneweek_topic_dict.get(topic_list[i]) + new_headline_importance * enhance_weight * HASHTAG_PENALTY
                    else:
                        ETH_oneweek_topic_dict[topic_list[i]] = ETH_oneweek_topic_dict.get(topic_list[i]) + new_headline_importance * enhance_weight

                # Add new id in dictionary
                if ETH_oneweek_id_dict.get(topic_list[i]) == None:
                    l = [new_ID]
                    ETH_oneweek_id_dict[topic_list[i]] = l
                else:
                    ETH_oneweek_id_dict[topic_list[i]].append(new_ID)


                if ETH_onemonth_topic_dict.get(topic_list[i]) == None:
                    if is_hashtag == True:
                        ETH_onemonth_topic_dict[topic_list[i]] = new_headline_importance * enhance_weight * HASHTAG_PENALTY
                    else:
                        ETH_onemonth_topic_dict[topic_list[i]] = new_headline_importance * enhance_weight
                else:
                    if is_hashtag == True:
                        ETH_onemonth_topic_dict[topic_list[i]] = ETH_onemonth_topic_dict.get(topic_list[i]) + new_headline_importance * enhance_weight * HASHTAG_PENALTY
                    else:
                        ETH_onemonth_topic_dict[topic_list[i]] = ETH_onemonth_topic_dict.get(topic_list[i]) + new_headline_importance * enhance_weight

                # Add new id in dictionary
                if ETH_onemonth_id_dict.get(topic_list[i]) == None:
                    l = [new_ID]
                    ETH_onemonth_id_dict[topic_list[i]] = l
                else:
                    ETH_onemonth_id_dict[topic_list[i]].append(new_ID)


                if ETH_threemonths_topic_dict.get(topic_list[i]) == None:
                    if is_hashtag == True:
                        ETH_threemonths_topic_dict[topic_list[i]] = new_headline_importance * enhance_weight * HASHTAG_PENALTY
                    else:
                        ETH_threemonths_topic_dict[topic_list[i]] = new_headline_importance * enhance_weight
                else:
                    if is_hashtag == True:
                        ETH_threemonths_topic_dict[topic_list[i]] = ETH_threemonths_topic_dict.get(topic_list[i]) + new_headline_importance * enhance_weight * HASHTAG_PENALTY
                    else:
                        ETH_threemonths_topic_dict[topic_list[i]] = ETH_threemonths_topic_dict.get(topic_list[i]) + new_headline_importance * enhance_weight

                # Add new id in dictionary
                if ETH_threemonths_id_dict.get(topic_list[i]) == None:
                    l = [new_ID]
                    ETH_threemonths_id_dict[topic_list[i]] = l
                else:
                    ETH_threemonths_id_dict[topic_list[i]].append(new_ID)

        twelvehours_trend = sorted(ETH_twelvehours_topic_dict.items(), key = lambda x:x[1], reverse = True)
        oneday_trend = sorted(ETH_oneday_topic_dict.items(), key = lambda x:x[1], reverse = True)
        oneweek_trend = sorted(ETH_oneweek_topic_dict.items(), key = lambda x:x[1], reverse = True)
        onemonth_trend = sorted(ETH_onemonth_topic_dict.items(), key = lambda x:x[1], reverse = True)
        threemonths_trend = sorted(ETH_threemonths_topic_dict.items(), key = lambda x:x[1], reverse = True)
        # don't show topics from same headlines
        i = 0
        tmp_dict = {}
        tmp_id_dict = {}
        
        
        i = 0
        tmp_dict = {}
        tmp_id_dict = {}
        for topic in twelvehours_trend:
            # print("i is: " +str(i))
            if i >= 500:
                break 
            if len(tmp_dict) == 0:

                tmp_dict[topic[0]] = topic[1]
                tmp_id_dict[topic[0]] = ETH_twelvehours_id_dict.get(topic[0])
            else:

                same_id = 0
                is_dup = False
                for exist_key in tmp_id_dict:
                    for id in ETH_twelvehours_id_dict.get(topic[0]):
                        if id in tmp_id_dict[exist_key]:
                            same_id += 1
                    if same_id/len(ETH_twelvehours_id_dict.get(topic[0])) >= 0.5:
                        is_dup = True
                        break
                    same_id = 0

                if is_dup == False:
                    tmp_dict[topic[0]] = topic[1]
                    tmp_id_dict[topic[0]] = ETH_twelvehours_id_dict.get(topic[0])
            i += 1

        twelvehours_trend_json = []
        i = 0
        
        for k in tmp_dict:
            if i >= 15:
                break
            subitem = {}
            subitem["text"] = k
            subitem["weight"] = round(tmp_dict[k], 2)
            subitem["ids"] = ','.join(str(e) for e in ETH_twelvehours_id_dict.get(k))
            if len(subitem["ids"]) < 8:
                continue
            twelvehours_trend_json.append(subitem)
            i += 1

        ETH_event_dict["twelvehours"] = json.dumps(twelvehours_trend_json)
        

        i = 0
        tmp_dict = {}
        tmp_id_dict = {}
        for topic in oneday_trend:
            if i >= 300:
                break
            if len(tmp_dict) == 0:
                tmp_dict[topic[0]] = topic[1]
                tmp_id_dict[topic[0]] = ETH_oneday_id_dict.get(topic[0])
            else:
                same_id = 0
                is_dup = False
                for exist_key in tmp_id_dict:
                    for id in ETH_oneday_id_dict.get(topic[0]):
                        if id in tmp_id_dict[exist_key]:
                            same_id += 1
                    if same_id/len(ETH_oneday_id_dict.get(topic[0])) >= 0.5:
                        is_dup = True
                        break
                    same_id = 0
                if is_dup == False:
                    tmp_dict[topic[0]] = topic[1]
                    tmp_id_dict[topic[0]] = ETH_oneday_id_dict.get(topic[0])

            i += 1
    
        oneday_trend_json = []
        i = 0
        for k in tmp_dict:
            if i >= 15:
                break
            subitem = {}
            subitem["text"] = k
            subitem["weight"] = round(tmp_dict[k], 2)
            subitem["ids"] = ','.join(str(e) for e in ETH_oneday_id_dict.get(k))
            if len(subitem["ids"]) < 8:
                continue
            oneday_trend_json.append(subitem)
            i += 1

        ETH_event_dict["oneday"] = json.dumps(oneday_trend_json)


        i = 0
        tmp_dict = {}
        tmp_id_dict = {}
        for topic in oneweek_trend:
            if i >= 300:
                break
            if len(tmp_dict) == 0:
                tmp_dict[topic[0]] = topic[1]
                tmp_id_dict[topic[0]] = ETH_oneweek_id_dict.get(topic[0])
            else:
                same_id = 0
                is_dup = False
                for exist_key in tmp_id_dict:
                    for id in ETH_oneweek_id_dict.get(topic[0]):
                        if id in tmp_id_dict[exist_key]:
                            same_id += 1
                    if same_id/len(ETH_oneweek_id_dict.get(topic[0])) >= 0.5:
                        is_dup = True
                        break
                    same_id = 0
                if is_dup == False:
                    tmp_dict[topic[0]] = topic[1]
                    tmp_id_dict[topic[0]] = ETH_oneweek_id_dict.get(topic[0])

            i += 1

        oneweek_trend_json = []
        i = 0
        for k in tmp_dict:
            if i >= 15:
                break
            subitem = {}
            subitem["text"] = k
            subitem["weight"] = round(tmp_dict[k], 2)
            subitem["ids"] = ','.join(str(e) for e in ETH_oneweek_id_dict.get(k))
            if len(subitem["ids"]) < 8:
                continue
            oneweek_trend_json.append(subitem)
            i += 1

        ETH_event_dict["oneweek"] = json.dumps(oneweek_trend_json)


        i = 0
        tmp_dict = {}
        tmp_id_dict = {}
        for topic in onemonth_trend:
            if i >= 300:
                break
            if len(tmp_dict) == 0:
                tmp_dict[topic[0]] = topic[1]
                tmp_id_dict[topic[0]] = ETH_onemonth_id_dict.get(topic[0])
            else:
                same_id = 0
                is_dup = False
                for exist_key in tmp_id_dict:
                    for id in ETH_onemonth_id_dict.get(topic[0]):
                        if id in tmp_id_dict[exist_key]:
                            same_id += 1
                    if same_id/len(ETH_onemonth_id_dict.get(topic[0])) >= 0.5:
                        is_dup = True
                        break
                    same_id = 0
                if is_dup == False:
                    tmp_dict[topic[0]] = topic[1]
                    tmp_id_dict[topic[0]] = ETH_onemonth_id_dict.get(topic[0])

            i += 1

        onemonth_trend_json = []
        i = 0
        for k in tmp_dict:
            if i >= 15:
                break
            subitem = {}
            subitem["text"] = k
            subitem["weight"] = round(tmp_dict[k], 2)
            subitem["ids"] = ','.join(str(e) for e in ETH_onemonth_id_dict.get(k))
            if len(subitem["ids"]) < 8:
                continue
            onemonth_trend_json.append(subitem)
            i += 1

        ETH_event_dict["onemonth"] = json.dumps(onemonth_trend_json)
        

        i = 0
        tmp_dict = {}
        tmp_id_dict = {}
        for topic in threemonths_trend:
            if i >= 300:
                break
            if len(tmp_dict) == 0:
                tmp_dict[topic[0]] = topic[1]
                tmp_id_dict[topic[0]] = ETH_threemonths_id_dict.get(topic[0])
            else:
                same_id = 0
                is_dup = False
                for exist_key in tmp_id_dict:
                    for id in ETH_threemonths_id_dict.get(topic[0]):
                        if id in tmp_id_dict[exist_key]:
                            same_id += 1
                    if same_id/len(ETH_threemonths_id_dict.get(topic[0])) >= 0.5:
                        is_dup = True
                        break
                    same_id = 0
                if is_dup == False:
                    tmp_dict[topic[0]] = topic[1]
                    tmp_id_dict[topic[0]] = ETH_threemonths_id_dict.get(topic[0])

            i += 1

        threemonths_trend_json = []
        i = 0
        for k in tmp_dict:
            if i >= 15:
                break
            subitem = {}
            subitem["text"] = k
            subitem["weight"] = round(tmp_dict[k], 2)
            subitem["ids"] = ','.join(str(e) for e in ETH_threemonths_id_dict.get(k))
            if len(subitem["ids"]) < 8:
                continue
            threemonths_trend_json.append(subitem)
            i += 1

        ETH_event_dict["threemonths"] = json.dumps(threemonths_trend_json)
        
        add_to_mysql()
        
    for new_head in XRP_tmp_headline_list:
        
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

        # maunually set new importance to 3, waiting for Diego's change
        # ====================================================================================================================   
        # ====================================================================================================================   
        XRP_twelvehours_importance_list.append(3.0)
        XRP_oneday_importance_list.append(3.0)
        XRP_oneweek_importance_list.append(3.0)
        XRP_onemonth_importance_list.append(3.0)
        XRP_threemonths_importance_list.append(3.0)
        # ====================================================================================================================   
        # ====================================================================================================================
        
        XRP_twelvehours_headline_list.append(topic_list)
        XRP_twelvehours_time_list.append(new_headline_time)
        XRP_twelvehours_ID_list.append(new_ID)
        XRP_oneday_headline_list.append(topic_list)
        XRP_oneday_time_list.append(new_headline_time)
        XRP_oneday_ID_list.append(new_ID)
        XRP_oneweek_headline_list.append(topic_list)
        XRP_oneweek_time_list.append(new_headline_time)
        XRP_oneweek_ID_list.append(new_ID)
        XRP_onemonth_headline_list.append(topic_list)
        XRP_onemonth_time_list.append(new_headline_time)
        XRP_onemonth_ID_list.append(new_ID)
        XRP_threemonths_headline_list.append(topic_list)
        XRP_threemonths_time_list.append(new_headline_time)
        XRP_threemonths_ID_list.append(new_ID)

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
                

                if XRP_twelvehours_topic_dict.get(topic_list[i]) == None:
                    if is_hashtag == True:
                        XRP_twelvehours_topic_dict[topic_list[i]] = new_headline_importance * enhance_weight * HASHTAG_PENALTY
                    else:
                        XRP_twelvehours_topic_dict[topic_list[i]] = new_headline_importance * enhance_weight
                else:
                    if is_hashtag == True:
                        XRP_twelvehours_topic_dict[topic_list[i]] = XRP_twelvehours_topic_dict.get(topic_list[i]) + new_headline_importance * enhance_weight * HASHTAG_PENALTY
                    else:
                        XRP_twelvehours_topic_dict[topic_list[i]] = XRP_twelvehours_topic_dict.get(topic_list[i]) + new_headline_importance * enhance_weight             

                # Add new id in dictionary
                if XRP_twelvehours_id_dict.get(topic_list[i]) == None:
                    l = [new_ID]
                    XRP_twelvehours_id_dict[topic_list[i]] = l
                else:
                    XRP_twelvehours_id_dict[topic_list[i]].append(new_ID)


                if XRP_oneday_topic_dict.get(topic_list[i]) == None:
                    if is_hashtag == True:
                        XRP_oneday_topic_dict[topic_list[i]] = new_headline_importance * enhance_weight * HASHTAG_PENALTY
                    else:
                        XRP_oneday_topic_dict[topic_list[i]] = new_headline_importance * enhance_weight
                else:
                    if is_hashtag == True:
                        XRP_oneday_topic_dict[topic_list[i]] = XRP_oneday_topic_dict.get(topic_list[i]) + new_headline_importance * enhance_weight * HASHTAG_PENALTY
                    else:
                        XRP_oneday_topic_dict[topic_list[i]] = XRP_oneday_topic_dict.get(topic_list[i]) + new_headline_importance * enhance_weight

                # Add new id in dictionary
                if XRP_oneday_id_dict.get(topic_list[i]) == None:
                    l = [new_ID]
                    XRP_oneday_id_dict[topic_list[i]] = l
                else:
                    XRP_oneday_id_dict[topic_list[i]].append(new_ID)


                if XRP_oneweek_topic_dict.get(topic_list[i]) == None:
                    if is_hashtag == True:
                        XRP_oneweek_topic_dict[topic_list[i]] = new_headline_importance * enhance_weight * HASHTAG_PENALTY
                    else:
                        XRP_oneweek_topic_dict[topic_list[i]] = new_headline_importance * enhance_weight
                else:
                    if is_hashtag == True:
                        XRP_oneweek_topic_dict[topic_list[i]] = XRP_oneweek_topic_dict.get(topic_list[i]) + new_headline_importance * enhance_weight * HASHTAG_PENALTY
                    else:
                        XRP_oneweek_topic_dict[topic_list[i]] = XRP_oneweek_topic_dict.get(topic_list[i]) + new_headline_importance * enhance_weight

                # Add new id in dictionary
                if XRP_oneweek_id_dict.get(topic_list[i]) == None:
                    l = [new_ID]
                    XRP_oneweek_id_dict[topic_list[i]] = l
                else:
                    XRP_oneweek_id_dict[topic_list[i]].append(new_ID)


                if XRP_onemonth_topic_dict.get(topic_list[i]) == None:
                    if is_hashtag == True:
                        XRP_onemonth_topic_dict[topic_list[i]] = new_headline_importance * enhance_weight * HASHTAG_PENALTY
                    else:
                        XRP_onemonth_topic_dict[topic_list[i]] = new_headline_importance * enhance_weight
                else:
                    if is_hashtag == True:
                        XRP_onemonth_topic_dict[topic_list[i]] = XRP_onemonth_topic_dict.get(topic_list[i]) + new_headline_importance * enhance_weight * HASHTAG_PENALTY
                    else:
                        XRP_onemonth_topic_dict[topic_list[i]] = XRP_onemonth_topic_dict.get(topic_list[i]) + new_headline_importance * enhance_weight

                # Add new id in dictionary
                if XRP_onemonth_id_dict.get(topic_list[i]) == None:
                    l = [new_ID]
                    XRP_onemonth_id_dict[topic_list[i]] = l
                else:
                    XRP_onemonth_id_dict[topic_list[i]].append(new_ID)



                if XRP_threemonths_topic_dict.get(topic_list[i]) == None:
                    if is_hashtag == True:
                        XRP_threemonths_topic_dict[topic_list[i]] = new_headline_importance * enhance_weight * HASHTAG_PENALTY
                    else:
                        XRP_threemonths_topic_dict[topic_list[i]] = new_headline_importance * enhance_weight
                else:
                    if is_hashtag == True:
                        XRP_threemonths_topic_dict[topic_list[i]] = XRP_threemonths_topic_dict.get(topic_list[i]) + new_headline_importance * enhance_weight * HASHTAG_PENALTY
                    else:
                        XRP_threemonths_topic_dict[topic_list[i]] = XRP_threemonths_topic_dict.get(topic_list[i]) + new_headline_importance * enhance_weight

                # Add new id in dictionary
                if XRP_threemonths_id_dict.get(topic_list[i]) == None:
                    l = [new_ID]
                    XRP_threemonths_id_dict[topic_list[i]] = l
                else:
                    XRP_threemonths_id_dict[topic_list[i]].append(new_ID)

        twelvehours_trend = sorted(XRP_twelvehours_topic_dict.items(), key = lambda x:x[1], reverse = True)
        oneday_trend = sorted(XRP_oneday_topic_dict.items(), key = lambda x:x[1], reverse = True)
        oneweek_trend = sorted(XRP_oneweek_topic_dict.items(), key = lambda x:x[1], reverse = True)
        onemonth_trend = sorted(XRP_onemonth_topic_dict.items(), key = lambda x:x[1], reverse = True)
        threemonths_trend = sorted(XRP_threemonths_topic_dict.items(), key = lambda x:x[1], reverse = True)
        # don't show topics from same headlines
        i = 0
        tmp_dict = {}
        tmp_id_dict = {}
                
        i = 0
        tmp_dict = {}
        tmp_id_dict = {}
        for topic in twelvehours_trend:
            # print("i is: " +str(i))
            if i >= 500:
                break 
            if len(tmp_dict) == 0:

                tmp_dict[topic[0]] = topic[1]
                tmp_id_dict[topic[0]] = XRP_twelvehours_id_dict.get(topic[0])
            else:

                same_id = 0
                is_dup = False
                for exist_key in tmp_id_dict:
                    for id in XRP_twelvehours_id_dict.get(topic[0]):
                        if id in tmp_id_dict[exist_key]:
                            same_id += 1
                    if same_id/len(XRP_twelvehours_id_dict.get(topic[0])) >= 0.5:
                        is_dup = True
                        break
                    same_id = 0

                if is_dup == False:
                    tmp_dict[topic[0]] = topic[1]
                    tmp_id_dict[topic[0]] = XRP_twelvehours_id_dict.get(topic[0])
            i += 1

        twelvehours_trend_json = []
        i = 0
        
        for k in tmp_dict:
            if i >= 15:
                break
            subitem = {}
            subitem["text"] = k
            subitem["weight"] = round(tmp_dict[k], 2)
            subitem["ids"] = ','.join(str(e) for e in XRP_twelvehours_id_dict.get(k))
            if len(subitem["ids"]) < 8:
                continue
            twelvehours_trend_json.append(subitem)
            i += 1

        XRP_event_dict["twelvehours"] = json.dumps(twelvehours_trend_json)
        

        i = 0
        tmp_dict = {}
        tmp_id_dict = {}
        for topic in oneday_trend:
            if i >= 300:
                break
            if len(tmp_dict) == 0:
                tmp_dict[topic[0]] = topic[1]
                tmp_id_dict[topic[0]] = XRP_oneday_id_dict.get(topic[0])
            else:
                same_id = 0
                is_dup = False
                for exist_key in tmp_id_dict:
                    for id in XRP_oneday_id_dict.get(topic[0]):
                        if id in tmp_id_dict[exist_key]:
                            same_id += 1
                    if same_id/len(XRP_oneday_id_dict.get(topic[0])) >= 0.5:
                        is_dup = True
                        break
                    same_id = 0
                if is_dup == False:
                    tmp_dict[topic[0]] = topic[1]
                    tmp_id_dict[topic[0]] = XRP_oneday_id_dict.get(topic[0])

            i += 1
    
        oneday_trend_json = []
        i = 0
        for k in tmp_dict:
            if i >= 15:
                break
            subitem = {}
            subitem["text"] = k
            subitem["weight"] = round(tmp_dict[k], 2)
            subitem["ids"] = ','.join(str(e) for e in XRP_oneday_id_dict.get(k))
            if len(subitem["ids"]) < 8:
                continue
            oneday_trend_json.append(subitem)
            i += 1

        XRP_event_dict["oneday"] = json.dumps(oneday_trend_json)


        i = 0
        tmp_dict = {}
        tmp_id_dict = {}
        for topic in oneweek_trend:
            if i >= 300:
                break
            if len(tmp_dict) == 0:
                tmp_dict[topic[0]] = topic[1]
                tmp_id_dict[topic[0]] = XRP_oneweek_id_dict.get(topic[0])
            else:
                same_id = 0
                is_dup = False
                for exist_key in tmp_id_dict:
                    for id in XRP_oneweek_id_dict.get(topic[0]):
                        if id in tmp_id_dict[exist_key]:
                            same_id += 1
                    if same_id/len(XRP_oneweek_id_dict.get(topic[0])) >= 0.5:
                        is_dup = True
                        break
                    same_id = 0
                if is_dup == False:
                    tmp_dict[topic[0]] = topic[1]
                    tmp_id_dict[topic[0]] = XRP_oneweek_id_dict.get(topic[0])

            i += 1

        oneweek_trend_json = []
        i = 0
        for k in tmp_dict:
            if i >= 15:
                break
            subitem = {}
            subitem["text"] = k
            subitem["weight"] = round(tmp_dict[k], 2)
            subitem["ids"] = ','.join(str(e) for e in XRP_oneweek_id_dict.get(k))
            if len(subitem["ids"]) < 8:
                continue
            oneweek_trend_json.append(subitem)
            i += 1

        XRP_event_dict["oneweek"] = json.dumps(oneweek_trend_json)


        i = 0
        tmp_dict = {}
        tmp_id_dict = {}
        for topic in onemonth_trend:
            if i >= 300:
                break
            if len(tmp_dict) == 0:
                tmp_dict[topic[0]] = topic[1]
                tmp_id_dict[topic[0]] = XRP_onemonth_id_dict.get(topic[0])
            else:
                same_id = 0
                is_dup = False
                for exist_key in tmp_id_dict:
                    for id in XRP_onemonth_id_dict.get(topic[0]):
                        if id in tmp_id_dict[exist_key]:
                            same_id += 1
                    if same_id/len(XRP_onemonth_id_dict.get(topic[0])) >= 0.5:
                        is_dup = True
                        break
                    same_id = 0
                if is_dup == False:
                    tmp_dict[topic[0]] = topic[1]
                    tmp_id_dict[topic[0]] = XRP_onemonth_id_dict.get(topic[0])

            i += 1

        onemonth_trend_json = []
        i = 0
        for k in tmp_dict:
            if i >= 15:
                break
            subitem = {}
            subitem["text"] = k
            subitem["weight"] = round(tmp_dict[k], 2)
            subitem["ids"] = ','.join(str(e) for e in XRP_onemonth_id_dict.get(k))
            if len(subitem["ids"]) < 8:
                continue
            onemonth_trend_json.append(subitem)
            i += 1

        XRP_event_dict["onemonth"] = json.dumps(onemonth_trend_json)


        i = 0
        tmp_dict = {}
        tmp_id_dict = {}
        for topic in threemonths_trend:
            if i >= 300:
                break
            if len(tmp_dict) == 0:
                tmp_dict[topic[0]] = topic[1]
                tmp_id_dict[topic[0]] = XRP_threemonths_id_dict.get(topic[0])
            else:
                same_id = 0
                is_dup = False
                for exist_key in tmp_id_dict:
                    for id in XRP_threemonths_id_dict.get(topic[0]):
                        if id in tmp_id_dict[exist_key]:
                            same_id += 1
                    if same_id/len(XRP_threemonths_id_dict.get(topic[0])) >= 0.5:
                        is_dup = True
                        break
                    same_id = 0
                if is_dup == False:
                    tmp_dict[topic[0]] = topic[1]
                    tmp_id_dict[topic[0]] = XRP_threemonths_id_dict.get(topic[0])

            i += 1

        threemonths_trend_json = []
        i = 0
        for k in tmp_dict:
            if i >= 15:
                break
            subitem = {}
            subitem["text"] = k
            subitem["weight"] = round(tmp_dict[k], 2)
            subitem["ids"] = ','.join(str(e) for e in XRP_threemonths_id_dict.get(k))
            if len(subitem["ids"]) < 8:
                continue
            threemonths_trend_json.append(subitem)
            i += 1

        XRP_event_dict["threemonths"] = json.dumps(threemonths_trend_json)
        
        add_to_mysql()



    
    for new_head in BCH_tmp_headline_list:
        
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

        # maunually set new importance to 3, waiting for Diego's change
        # ====================================================================================================================   
        # ====================================================================================================================   
        BCH_twelvehours_importance_list.append(3.0)
        BCH_oneday_importance_list.append(3.0)
        BCH_oneweek_importance_list.append(3.0)
        BCH_onemonth_importance_list.append(3.0)
        BCH_threemonths_importance_list.append(3.0)
        # ====================================================================================================================   
        # ====================================================================================================================
        
        BCH_twelvehours_headline_list.append(topic_list)
        BCH_twelvehours_time_list.append(new_headline_time)
        BCH_twelvehours_ID_list.append(new_ID)
        BCH_oneday_headline_list.append(topic_list)
        BCH_oneday_time_list.append(new_headline_time)
        BCH_oneday_ID_list.append(new_ID)
        BCH_oneweek_headline_list.append(topic_list)
        BCH_oneweek_time_list.append(new_headline_time)
        BCH_oneweek_ID_list.append(new_ID)
        BCH_onemonth_headline_list.append(topic_list)
        BCH_onemonth_time_list.append(new_headline_time)
        BCH_onemonth_ID_list.append(new_ID)
        BCH_threemonths_headline_list.append(topic_list)
        BCH_threemonths_time_list.append(new_headline_time)
        BCH_threemonths_ID_list.append(new_ID)

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
                

                if BCH_twelvehours_topic_dict.get(topic_list[i]) == None:
                    if is_hashtag == True:
                        BCH_twelvehours_topic_dict[topic_list[i]] = new_headline_importance * enhance_weight * HASHTAG_PENALTY
                    else:
                        BCH_twelvehours_topic_dict[topic_list[i]] = new_headline_importance * enhance_weight
                else:
                    if is_hashtag == True:
                        BCH_twelvehours_topic_dict[topic_list[i]] = BCH_twelvehours_topic_dict.get(topic_list[i]) + new_headline_importance * enhance_weight * HASHTAG_PENALTY
                    else:
                        BCH_twelvehours_topic_dict[topic_list[i]] = BCH_twelvehours_topic_dict.get(topic_list[i]) + new_headline_importance * enhance_weight             

                # Add new id in dictionary
                if BCH_twelvehours_id_dict.get(topic_list[i]) == None:
                    l = [new_ID]
                    BCH_twelvehours_id_dict[topic_list[i]] = l
                else:
                    BCH_twelvehours_id_dict[topic_list[i]].append(new_ID)


                if BCH_oneday_topic_dict.get(topic_list[i]) == None:
                    if is_hashtag == True:
                        BCH_oneday_topic_dict[topic_list[i]] = new_headline_importance * enhance_weight * HASHTAG_PENALTY
                    else:
                        BCH_oneday_topic_dict[topic_list[i]] = new_headline_importance * enhance_weight
                else:
                    if is_hashtag == True:
                        BCH_oneday_topic_dict[topic_list[i]] = BCH_oneday_topic_dict.get(topic_list[i]) + new_headline_importance * enhance_weight * HASHTAG_PENALTY
                    else:
                        BCH_oneday_topic_dict[topic_list[i]] = BCH_oneday_topic_dict.get(topic_list[i]) + new_headline_importance * enhance_weight

                # Add new id in dictionary
                if BCH_oneday_id_dict.get(topic_list[i]) == None:
                    l = [new_ID]
                    BCH_oneday_id_dict[topic_list[i]] = l
                else:
                    BCH_oneday_id_dict[topic_list[i]].append(new_ID)


                if BCH_oneweek_topic_dict.get(topic_list[i]) == None:
                    if is_hashtag == True:
                        BCH_oneweek_topic_dict[topic_list[i]] = new_headline_importance * enhance_weight * HASHTAG_PENALTY
                    else:
                        BCH_oneweek_topic_dict[topic_list[i]] = new_headline_importance * enhance_weight
                else:
                    if is_hashtag == True:
                        BCH_oneweek_topic_dict[topic_list[i]] = BCH_oneweek_topic_dict.get(topic_list[i]) + new_headline_importance * enhance_weight * HASHTAG_PENALTY
                    else:
                        BCH_oneweek_topic_dict[topic_list[i]] = BCH_oneweek_topic_dict.get(topic_list[i]) + new_headline_importance * enhance_weight

                # Add new id in dictionary
                if BCH_oneweek_id_dict.get(topic_list[i]) == None:
                    l = [new_ID]
                    BCH_oneweek_id_dict[topic_list[i]] = l
                else:
                    BCH_oneweek_id_dict[topic_list[i]].append(new_ID)


                if BCH_onemonth_topic_dict.get(topic_list[i]) == None:
                    if is_hashtag == True:
                        BCH_onemonth_topic_dict[topic_list[i]] = new_headline_importance * enhance_weight * HASHTAG_PENALTY
                    else:
                        BCH_onemonth_topic_dict[topic_list[i]] = new_headline_importance * enhance_weight
                else:
                    if is_hashtag == True:
                        BCH_onemonth_topic_dict[topic_list[i]] = BCH_onemonth_topic_dict.get(topic_list[i]) + new_headline_importance * enhance_weight * HASHTAG_PENALTY
                    else:
                        BCH_onemonth_topic_dict[topic_list[i]] = BCH_onemonth_topic_dict.get(topic_list[i]) + new_headline_importance * enhance_weight

                # Add new id in dictionary
                if BCH_onemonth_id_dict.get(topic_list[i]) == None:
                    l = [new_ID]
                    BCH_onemonth_id_dict[topic_list[i]] = l
                else:
                    BCH_onemonth_id_dict[topic_list[i]].append(new_ID)



                if BCH_threemonths_topic_dict.get(topic_list[i]) == None:
                    if is_hashtag == True:
                        BCH_threemonths_topic_dict[topic_list[i]] = new_headline_importance * enhance_weight * HASHTAG_PENALTY
                    else:
                        BCH_threemonths_topic_dict[topic_list[i]] = new_headline_importance * enhance_weight
                else:
                    if is_hashtag == True:
                        BCH_threemonths_topic_dict[topic_list[i]] = BCH_threemonths_topic_dict.get(topic_list[i]) + new_headline_importance * enhance_weight * HASHTAG_PENALTY
                    else:
                        BCH_threemonths_topic_dict[topic_list[i]] = BCH_threemonths_topic_dict.get(topic_list[i]) + new_headline_importance * enhance_weight

                # Add new id in dictionary
                if BCH_threemonths_id_dict.get(topic_list[i]) == None:
                    l = [new_ID]
                    BCH_threemonths_id_dict[topic_list[i]] = l
                else:
                    BCH_threemonths_id_dict[topic_list[i]].append(new_ID)

        twelvehours_trend = sorted(BCH_twelvehours_topic_dict.items(), key = lambda x:x[1], reverse = True)
        oneday_trend = sorted(BCH_oneday_topic_dict.items(), key = lambda x:x[1], reverse = True)
        oneweek_trend = sorted(BCH_oneweek_topic_dict.items(), key = lambda x:x[1], reverse = True)
        onemonth_trend = sorted(BCH_onemonth_topic_dict.items(), key = lambda x:x[1], reverse = True)
        threemonths_trend = sorted(BCH_threemonths_topic_dict.items(), key = lambda x:x[1], reverse = True)
        # don't show topics from same headlines
        i = 0
        tmp_dict = {}
        tmp_id_dict = {}
                
        i = 0
        tmp_dict = {}
        tmp_id_dict = {}
        for topic in twelvehours_trend:
            # print("i is: " +str(i))
            if i >= 500:
                break 
            if len(tmp_dict) == 0:

                tmp_dict[topic[0]] = topic[1]
                tmp_id_dict[topic[0]] = BCH_twelvehours_id_dict.get(topic[0])
            else:

                same_id = 0
                is_dup = False
                for exist_key in tmp_id_dict:
                    for id in BCH_twelvehours_id_dict.get(topic[0]):
                        if id in tmp_id_dict[exist_key]:
                            same_id += 1
                    if same_id/len(BCH_twelvehours_id_dict.get(topic[0])) >= 0.5:
                        is_dup = True
                        break
                    same_id = 0

                if is_dup == False:
                    tmp_dict[topic[0]] = topic[1]
                    tmp_id_dict[topic[0]] = BCH_twelvehours_id_dict.get(topic[0])
            i += 1

        twelvehours_trend_json = []
        i = 0
        
        for k in tmp_dict:
            if i >= 15:
                break
            subitem = {}
            subitem["text"] = k
            subitem["weight"] = round(tmp_dict[k], 2)
            subitem["ids"] = ','.join(str(e) for e in BCH_twelvehours_id_dict.get(k))
            if len(subitem["ids"]) < 8:
                continue
            twelvehours_trend_json.append(subitem)
            i += 1

        BCH_event_dict["twelvehours"] = json.dumps(twelvehours_trend_json)
        

        i = 0
        tmp_dict = {}
        tmp_id_dict = {}
        for topic in oneday_trend:
            if i >= 300:
                break
            if len(tmp_dict) == 0:
                tmp_dict[topic[0]] = topic[1]
                tmp_id_dict[topic[0]] = BCH_oneday_id_dict.get(topic[0])
            else:
                same_id = 0
                is_dup = False
                for exist_key in tmp_id_dict:
                    for id in BCH_oneday_id_dict.get(topic[0]):
                        if id in tmp_id_dict[exist_key]:
                            same_id += 1
                    if same_id/len(BCH_oneday_id_dict.get(topic[0])) >= 0.5:
                        is_dup = True
                        break
                    same_id = 0
                if is_dup == False:
                    tmp_dict[topic[0]] = topic[1]
                    tmp_id_dict[topic[0]] = BCH_oneday_id_dict.get(topic[0])

            i += 1
    
        oneday_trend_json = []
        i = 0
        for k in tmp_dict:
            if i >= 15:
                break
            subitem = {}
            subitem["text"] = k
            subitem["weight"] = round(tmp_dict[k], 2)
            subitem["ids"] = ','.join(str(e) for e in BCH_oneday_id_dict.get(k))
            if len(subitem["ids"]) < 8:
                continue
            oneday_trend_json.append(subitem)
            i += 1

        BCH_event_dict["oneday"] = json.dumps(oneday_trend_json)


        i = 0
        tmp_dict = {}
        tmp_id_dict = {}
        for topic in oneweek_trend:
            if i >= 300:
                break
            if len(tmp_dict) == 0:
                tmp_dict[topic[0]] = topic[1]
                tmp_id_dict[topic[0]] = BCH_oneweek_id_dict.get(topic[0])
            else:
                same_id = 0
                is_dup = False
                for exist_key in tmp_id_dict:
                    for id in BCH_oneweek_id_dict.get(topic[0]):
                        if id in tmp_id_dict[exist_key]:
                            same_id += 1
                    if same_id/len(BCH_oneweek_id_dict.get(topic[0])) >= 0.5:
                        is_dup = True
                        break
                    same_id = 0
                if is_dup == False:
                    tmp_dict[topic[0]] = topic[1]
                    tmp_id_dict[topic[0]] = BCH_oneweek_id_dict.get(topic[0])

            i += 1

        oneweek_trend_json = []
        i = 0
        for k in tmp_dict:
            if i >= 15:
                break
            subitem = {}
            subitem["text"] = k
            subitem["weight"] = round(tmp_dict[k], 2)
            subitem["ids"] = ','.join(str(e) for e in BCH_oneweek_id_dict.get(k))
            if len(subitem["ids"]) < 8:
                continue
            oneweek_trend_json.append(subitem)
            i += 1

        BCH_event_dict["oneweek"] = json.dumps(oneweek_trend_json)


        i = 0
        tmp_dict = {}
        tmp_id_dict = {}
        for topic in onemonth_trend:
            if i >= 300:
                break
            if len(tmp_dict) == 0:
                tmp_dict[topic[0]] = topic[1]
                tmp_id_dict[topic[0]] = BCH_onemonth_id_dict.get(topic[0])
            else:
                same_id = 0
                is_dup = False
                for exist_key in tmp_id_dict:
                    for id in BCH_onemonth_id_dict.get(topic[0]):
                        if id in tmp_id_dict[exist_key]:
                            same_id += 1
                    if same_id/len(BCH_onemonth_id_dict.get(topic[0])) >= 0.5:
                        is_dup = True
                        break
                    same_id = 0
                if is_dup == False:
                    tmp_dict[topic[0]] = topic[1]
                    tmp_id_dict[topic[0]] = BCH_onemonth_id_dict.get(topic[0])

            i += 1

        onemonth_trend_json = []
        i = 0
        for k in tmp_dict:
            if i >= 15:
                break
            subitem = {}
            subitem["text"] = k
            subitem["weight"] = round(tmp_dict[k], 2)
            subitem["ids"] = ','.join(str(e) for e in BCH_onemonth_id_dict.get(k))
            if len(subitem["ids"]) < 8:
                continue
            onemonth_trend_json.append(subitem)
            i += 1

        BCH_event_dict["onemonth"] = json.dumps(onemonth_trend_json)


        i = 0
        tmp_dict = {}
        tmp_id_dict = {}
        for topic in threemonths_trend:
            if i >= 300:
                break
            if len(tmp_dict) == 0:
                tmp_dict[topic[0]] = topic[1]
                tmp_id_dict[topic[0]] = BCH_threemonths_id_dict.get(topic[0])
            else:
                same_id = 0
                is_dup = False
                for exist_key in tmp_id_dict:
                    for id in BCH_threemonths_id_dict.get(topic[0]):
                        if id in tmp_id_dict[exist_key]:
                            same_id += 1
                    if same_id/len(BCH_threemonths_id_dict.get(topic[0])) >= 0.5:
                        is_dup = True
                        break
                    same_id = 0
                if is_dup == False:
                    tmp_dict[topic[0]] = topic[1]
                    tmp_id_dict[topic[0]] = BCH_threemonths_id_dict.get(topic[0])

            i += 1

        threemonths_trend_json = []
        i = 0
        for k in tmp_dict:
            if i >= 15:
                break
            subitem = {}
            subitem["text"] = k
            subitem["weight"] = round(tmp_dict[k], 2)
            subitem["ids"] = ','.join(str(e) for e in BCH_threemonths_id_dict.get(k))
            if len(subitem["ids"]) < 8:
                continue
            threemonths_trend_json.append(subitem)
            i += 1

        BCH_event_dict["threemonths"] = json.dumps(threemonths_trend_json)
        
        add_to_mysql()






    
    for new_head in LTC_tmp_headline_list:
        
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

        # maunually set new importance to 3, waiting for Diego's change
        # ====================================================================================================================   
        # ====================================================================================================================   
        LTC_twelvehours_importance_list.append(3.0)
        LTC_oneday_importance_list.append(3.0)
        LTC_oneweek_importance_list.append(3.0)
        LTC_onemonth_importance_list.append(3.0)
        LTC_threemonths_importance_list.append(3.0)
        # ====================================================================================================================   
        # ====================================================================================================================
        
        LTC_twelvehours_headline_list.append(topic_list)
        LTC_twelvehours_time_list.append(new_headline_time)
        LTC_twelvehours_ID_list.append(new_ID)
        LTC_oneday_headline_list.append(topic_list)
        LTC_oneday_time_list.append(new_headline_time)
        LTC_oneday_ID_list.append(new_ID)
        LTC_oneweek_headline_list.append(topic_list)
        LTC_oneweek_time_list.append(new_headline_time)
        LTC_oneweek_ID_list.append(new_ID)
        LTC_onemonth_headline_list.append(topic_list)
        LTC_onemonth_time_list.append(new_headline_time)
        LTC_onemonth_ID_list.append(new_ID)
        LTC_threemonths_headline_list.append(topic_list)
        LTC_threemonths_time_list.append(new_headline_time)
        LTC_threemonths_ID_list.append(new_ID)

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
                

                if LTC_twelvehours_topic_dict.get(topic_list[i]) == None:
                    if is_hashtag == True:
                        LTC_twelvehours_topic_dict[topic_list[i]] = new_headline_importance * enhance_weight * HASHTAG_PENALTY
                    else:
                        LTC_twelvehours_topic_dict[topic_list[i]] = new_headline_importance * enhance_weight
                else:
                    if is_hashtag == True:
                        LTC_twelvehours_topic_dict[topic_list[i]] = LTC_twelvehours_topic_dict.get(topic_list[i]) + new_headline_importance * enhance_weight * HASHTAG_PENALTY
                    else:
                        LTC_twelvehours_topic_dict[topic_list[i]] = LTC_twelvehours_topic_dict.get(topic_list[i]) + new_headline_importance * enhance_weight             

                # Add new id in dictionary
                if LTC_twelvehours_id_dict.get(topic_list[i]) == None:
                    l = [new_ID]
                    LTC_twelvehours_id_dict[topic_list[i]] = l
                else:
                    LTC_twelvehours_id_dict[topic_list[i]].append(new_ID)


                if LTC_oneday_topic_dict.get(topic_list[i]) == None:
                    if is_hashtag == True:
                        LTC_oneday_topic_dict[topic_list[i]] = new_headline_importance * enhance_weight * HASHTAG_PENALTY
                    else:
                        LTC_oneday_topic_dict[topic_list[i]] = new_headline_importance * enhance_weight
                else:
                    if is_hashtag == True:
                        LTC_oneday_topic_dict[topic_list[i]] = LTC_oneday_topic_dict.get(topic_list[i]) + new_headline_importance * enhance_weight * HASHTAG_PENALTY
                    else:
                        LTC_oneday_topic_dict[topic_list[i]] = LTC_oneday_topic_dict.get(topic_list[i]) + new_headline_importance * enhance_weight

                # Add new id in dictionary
                if LTC_oneday_id_dict.get(topic_list[i]) == None:
                    l = [new_ID]
                    LTC_oneday_id_dict[topic_list[i]] = l
                else:
                    LTC_oneday_id_dict[topic_list[i]].append(new_ID)


                if LTC_oneweek_topic_dict.get(topic_list[i]) == None:
                    if is_hashtag == True:
                        LTC_oneweek_topic_dict[topic_list[i]] = new_headline_importance * enhance_weight * HASHTAG_PENALTY
                    else:
                        LTC_oneweek_topic_dict[topic_list[i]] = new_headline_importance * enhance_weight
                else:
                    if is_hashtag == True:
                        LTC_oneweek_topic_dict[topic_list[i]] = LTC_oneweek_topic_dict.get(topic_list[i]) + new_headline_importance * enhance_weight * HASHTAG_PENALTY
                    else:
                        LTC_oneweek_topic_dict[topic_list[i]] = LTC_oneweek_topic_dict.get(topic_list[i]) + new_headline_importance * enhance_weight

                # Add new id in dictionary
                if LTC_oneweek_id_dict.get(topic_list[i]) == None:
                    l = [new_ID]
                    LTC_oneweek_id_dict[topic_list[i]] = l
                else:
                    LTC_oneweek_id_dict[topic_list[i]].append(new_ID)


                if LTC_onemonth_topic_dict.get(topic_list[i]) == None:
                    if is_hashtag == True:
                        LTC_onemonth_topic_dict[topic_list[i]] = new_headline_importance * enhance_weight * HASHTAG_PENALTY
                    else:
                        LTC_onemonth_topic_dict[topic_list[i]] = new_headline_importance * enhance_weight
                else:
                    if is_hashtag == True:
                        LTC_onemonth_topic_dict[topic_list[i]] = LTC_onemonth_topic_dict.get(topic_list[i]) + new_headline_importance * enhance_weight * HASHTAG_PENALTY
                    else:
                        LTC_onemonth_topic_dict[topic_list[i]] = LTC_onemonth_topic_dict.get(topic_list[i]) + new_headline_importance * enhance_weight

                # Add new id in dictionary
                if LTC_onemonth_id_dict.get(topic_list[i]) == None:
                    l = [new_ID]
                    LTC_onemonth_id_dict[topic_list[i]] = l
                else:
                    LTC_onemonth_id_dict[topic_list[i]].append(new_ID)



                if LTC_threemonths_topic_dict.get(topic_list[i]) == None:
                    if is_hashtag == True:
                        LTC_threemonths_topic_dict[topic_list[i]] = new_headline_importance * enhance_weight * HASHTAG_PENALTY
                    else:
                        LTC_threemonths_topic_dict[topic_list[i]] = new_headline_importance * enhance_weight
                else:
                    if is_hashtag == True:
                        LTC_threemonths_topic_dict[topic_list[i]] = LTC_threemonths_topic_dict.get(topic_list[i]) + new_headline_importance * enhance_weight * HASHTAG_PENALTY
                    else:
                        LTC_threemonths_topic_dict[topic_list[i]] = LTC_threemonths_topic_dict.get(topic_list[i]) + new_headline_importance * enhance_weight

                # Add new id in dictionary
                if LTC_threemonths_id_dict.get(topic_list[i]) == None:
                    l = [new_ID]
                    LTC_threemonths_id_dict[topic_list[i]] = l
                else:
                    LTC_threemonths_id_dict[topic_list[i]].append(new_ID)

        twelvehours_trend = sorted(LTC_twelvehours_topic_dict.items(), key = lambda x:x[1], reverse = True)
        oneday_trend = sorted(LTC_oneday_topic_dict.items(), key = lambda x:x[1], reverse = True)
        oneweek_trend = sorted(LTC_oneweek_topic_dict.items(), key = lambda x:x[1], reverse = True)
        onemonth_trend = sorted(LTC_onemonth_topic_dict.items(), key = lambda x:x[1], reverse = True)
        threemonths_trend = sorted(LTC_threemonths_topic_dict.items(), key = lambda x:x[1], reverse = True)
        # don't show topics from same headlines
        i = 0
        tmp_dict = {}
        tmp_id_dict = {}
                
        i = 0
        tmp_dict = {}
        tmp_id_dict = {}
        for topic in twelvehours_trend:
            # print("i is: " +str(i))
            if i >= 500:
                break 
            if len(tmp_dict) == 0:

                tmp_dict[topic[0]] = topic[1]
                tmp_id_dict[topic[0]] = LTC_twelvehours_id_dict.get(topic[0])
            else:

                same_id = 0
                is_dup = False
                for exist_key in tmp_id_dict:
                    for id in LTC_twelvehours_id_dict.get(topic[0]):
                        if id in tmp_id_dict[exist_key]:
                            same_id += 1
                    if same_id/len(LTC_twelvehours_id_dict.get(topic[0])) >= 0.5:
                        is_dup = True
                        break
                    same_id = 0

                if is_dup == False:
                    tmp_dict[topic[0]] = topic[1]
                    tmp_id_dict[topic[0]] = LTC_twelvehours_id_dict.get(topic[0])
            i += 1

        twelvehours_trend_json = []
        i = 0
        
        for k in tmp_dict:
            if i >= 15:
                break
            subitem = {}
            subitem["text"] = k
            subitem["weight"] = round(tmp_dict[k], 2)
            subitem["ids"] = ','.join(str(e) for e in LTC_twelvehours_id_dict.get(k))
            if len(subitem["ids"]) < 8:
                continue
            twelvehours_trend_json.append(subitem)
            i += 1

        LTC_event_dict["twelvehours"] = json.dumps(twelvehours_trend_json)
        

        i = 0
        tmp_dict = {}
        tmp_id_dict = {}
        for topic in oneday_trend:
            if i >= 300:
                break
            if len(tmp_dict) == 0:
                tmp_dict[topic[0]] = topic[1]
                tmp_id_dict[topic[0]] = LTC_oneday_id_dict.get(topic[0])
            else:
                same_id = 0
                is_dup = False
                for exist_key in tmp_id_dict:
                    for id in LTC_oneday_id_dict.get(topic[0]):
                        if id in tmp_id_dict[exist_key]:
                            same_id += 1
                    if same_id/len(LTC_oneday_id_dict.get(topic[0])) >= 0.5:
                        is_dup = True
                        break
                    same_id = 0
                if is_dup == False:
                    tmp_dict[topic[0]] = topic[1]
                    tmp_id_dict[topic[0]] = LTC_oneday_id_dict.get(topic[0])

            i += 1
    
        oneday_trend_json = []
        i = 0
        for k in tmp_dict:
            if i >= 15:
                break
            subitem = {}
            subitem["text"] = k
            subitem["weight"] = round(tmp_dict[k], 2)
            subitem["ids"] = ','.join(str(e) for e in LTC_oneday_id_dict.get(k))
            if len(subitem["ids"]) < 8:
                continue
            oneday_trend_json.append(subitem)
            i += 1

        LTC_event_dict["oneday"] = json.dumps(oneday_trend_json)


        i = 0
        tmp_dict = {}
        tmp_id_dict = {}
        for topic in oneweek_trend:
            if i >= 300:
                break
            if len(tmp_dict) == 0:
                tmp_dict[topic[0]] = topic[1]
                tmp_id_dict[topic[0]] = LTC_oneweek_id_dict.get(topic[0])
            else:
                same_id = 0
                is_dup = False
                for exist_key in tmp_id_dict:
                    for id in LTC_oneweek_id_dict.get(topic[0]):
                        if id in tmp_id_dict[exist_key]:
                            same_id += 1
                    if same_id/len(LTC_oneweek_id_dict.get(topic[0])) >= 0.5:
                        is_dup = True
                        break
                    same_id = 0
                if is_dup == False:
                    tmp_dict[topic[0]] = topic[1]
                    tmp_id_dict[topic[0]] = LTC_oneweek_id_dict.get(topic[0])

            i += 1

        oneweek_trend_json = []
        i = 0
        for k in tmp_dict:
            if i >= 15:
                break
            subitem = {}
            subitem["text"] = k
            subitem["weight"] = round(tmp_dict[k], 2)
            subitem["ids"] = ','.join(str(e) for e in LTC_oneweek_id_dict.get(k))
            if len(subitem["ids"]) < 8:
                continue
            oneweek_trend_json.append(subitem)
            i += 1

        LTC_event_dict["oneweek"] = json.dumps(oneweek_trend_json)


        i = 0
        tmp_dict = {}
        tmp_id_dict = {}
        for topic in onemonth_trend:
            if i >= 300:
                break
            if len(tmp_dict) == 0:
                tmp_dict[topic[0]] = topic[1]
                tmp_id_dict[topic[0]] = LTC_onemonth_id_dict.get(topic[0])
            else:
                same_id = 0
                is_dup = False
                for exist_key in tmp_id_dict:
                    for id in LTC_onemonth_id_dict.get(topic[0]):
                        if id in tmp_id_dict[exist_key]:
                            same_id += 1
                    if same_id/len(LTC_onemonth_id_dict.get(topic[0])) >= 0.5:
                        is_dup = True
                        break
                    same_id = 0
                if is_dup == False:
                    tmp_dict[topic[0]] = topic[1]
                    tmp_id_dict[topic[0]] = LTC_onemonth_id_dict.get(topic[0])

            i += 1

        onemonth_trend_json = []
        i = 0
        for k in tmp_dict:
            if i >= 15:
                break
            subitem = {}
            subitem["text"] = k
            subitem["weight"] = round(tmp_dict[k], 2)
            subitem["ids"] = ','.join(str(e) for e in LTC_onemonth_id_dict.get(k))
            if len(subitem["ids"]) < 8:
                continue
            onemonth_trend_json.append(subitem)
            i += 1

        LTC_event_dict["onemonth"] = json.dumps(onemonth_trend_json)


        i = 0
        tmp_dict = {}
        tmp_id_dict = {}
        for topic in threemonths_trend:
            if i >= 300:
                break
            if len(tmp_dict) == 0:
                tmp_dict[topic[0]] = topic[1]
                tmp_id_dict[topic[0]] = LTC_threemonths_id_dict.get(topic[0])
            else:
                same_id = 0
                is_dup = False
                for exist_key in tmp_id_dict:
                    for id in LTC_threemonths_id_dict.get(topic[0]):
                        if id in tmp_id_dict[exist_key]:
                            same_id += 1
                    if same_id/len(LTC_threemonths_id_dict.get(topic[0])) >= 0.5:
                        is_dup = True
                        break
                    same_id = 0
                if is_dup == False:
                    tmp_dict[topic[0]] = topic[1]
                    tmp_id_dict[topic[0]] = LTC_threemonths_id_dict.get(topic[0])

            i += 1

        threemonths_trend_json = []
        i = 0
        for k in tmp_dict:
            if i >= 15:
                break
            subitem = {}
            subitem["text"] = k
            subitem["weight"] = round(tmp_dict[k], 2)
            subitem["ids"] = ','.join(str(e) for e in LTC_threemonths_id_dict.get(k))
            if len(subitem["ids"]) < 8:
                continue
            threemonths_trend_json.append(subitem)
            i += 1

        LTC_event_dict["threemonths"] = json.dumps(threemonths_trend_json)
        
        add_to_mysql()



    # add_to_mysql()
    ETH_tmp_headline_list = []
       
    # add_to_mysql()
    BTC_tmp_headline_list = []

    # add_to_mysql()
    XRP_tmp_headline_list = []

    # add_to_mysql()
    BCH_tmp_headline_list = []

    # add_to_mysql()
    LTC_tmp_headline_list = []
        
        
        


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


    for period, trend in BTC_event_dict.items():
        trend_text, ids = extract_id(trend)
                   
            
        if period == "twelvehours":
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
               
    for period, trend in ETH_event_dict.items():
        trend_text, ids = extract_id(trend)
                   
        if period == "twelvehours":
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

    for period, trend in XRP_event_dict.items():
        trend_text, ids = extract_id(trend)
                    
        if period == "twelvehours":
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

    for period, trend in BCH_event_dict.items():
        trend_text, ids = extract_id(trend)
                    
        if period == "twelvehours":
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

    for period, trend in LTC_event_dict.items():
        trend_text, ids = extract_id(trend)
                    
        if period == "twelvehours":
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
        if "btc" in lower_args:
                BTC_tmp_headline_list.append(args_str)
        if "eth" in lower_args:
                ETH_tmp_headline_list.append(args_str)
        if "xrp" in lower_args:
                XRP_tmp_headline_list.append(args_str)
        if "bch" in lower_args:
                BCH_tmp_headline_list.append(args_str)
        if "ltc" in lower_args:
                LTC_tmp_headline_list.append(args_str)
        


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


def one_time_import():
    init_dict()
    Now = datetime.datetime.now()

    for (line, time, ID, importance) in zip(BTC_twelvehours_headline_list, BTC_twelvehours_time_list, BTC_twelvehours_ID_list, BTC_twelvehours_importance_list):

        
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
            if BTC_twelvehours_topic_dict.get(topic_list[i]) == None:
                BTC_twelvehours_topic_dict[topic_list[i]] = enhance_weight * (1 - (Now - datetime.datetime.strptime(time, time_format)).seconds/43200)
            # Add weight
            else:
                BTC_twelvehours_topic_dict[topic_list[i]] = BTC_twelvehours_topic_dict.get(topic_list[i]) + enhance_weight * (1 - (Now - datetime.datetime.strptime(time, time_format)).seconds/43200)

            # Add new id in dictionary
            if BTC_twelvehours_id_dict.get(topic_list[i]) == None:
                l = [ID]
                BTC_twelvehours_id_dict[topic_list[i]] = l
            else:
                BTC_twelvehours_id_dict[topic_list[i]].append(ID)  

    for (line, time, ID, importance) in zip(BTC_oneday_headline_list, BTC_oneday_time_list, BTC_oneday_ID_list, BTC_oneday_importance_list):
        
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
            if BTC_oneday_topic_dict.get(topic_list[i]) == None:
                BTC_oneday_topic_dict[topic_list[i]] = enhance_weight * (1 - (Now - datetime.datetime.strptime(time, time_format)).seconds/86400)
            # Add weight
            else:
                BTC_oneday_topic_dict[topic_list[i]] = BTC_oneday_topic_dict.get(topic_list[i]) + enhance_weight * (1 - (Now - datetime.datetime.strptime(time, time_format)).seconds/86400)

            # Add new id in dictionary
            if BTC_oneday_id_dict.get(topic_list[i]) == None:
                l = [ID]
                BTC_oneday_id_dict[topic_list[i]] = l
            else:
                BTC_oneday_id_dict[topic_list[i]].append(ID)

    for (line, time, ID, importance) in zip(BTC_oneweek_headline_list, BTC_oneweek_time_list, BTC_oneweek_ID_list, BTC_oneweek_importance_list):
        
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
            if BTC_oneweek_topic_dict.get(topic_list[i]) == None:
                BTC_oneweek_topic_dict[topic_list[i]] = enhance_weight * (1 - ((Now - datetime.datetime.strptime(time, time_format)).seconds + (Now - datetime.datetime.strptime(time, time_format)).days * 86400)/604800)
            # Add weight
            else:
                BTC_oneweek_topic_dict[topic_list[i]] = BTC_oneweek_topic_dict.get(topic_list[i]) + enhance_weight * (1 - ((Now - datetime.datetime.strptime(time, time_format)).seconds + (Now - datetime.datetime.strptime(time, time_format)).days * 86400)/604800)

            # Add new id in dictionary
            if BTC_oneweek_id_dict.get(topic_list[i]) == None:
                l = [ID]
                BTC_oneweek_id_dict[topic_list[i]] = l
            else:
                BTC_oneweek_id_dict[topic_list[i]].append(ID)

    for (line, time, ID, importance) in zip(BTC_onemonth_headline_list, BTC_onemonth_time_list, BTC_onemonth_ID_list, BTC_onemonth_importance_list):
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
            if BTC_onemonth_topic_dict.get(topic_list[i]) == None:
                BTC_onemonth_topic_dict[topic_list[i]] = enhance_weight * (1 - ((Now - datetime.datetime.strptime(time, time_format)).seconds + (Now - datetime.datetime.strptime(time, time_format)).days * 86400)/2592000)
            # Add weight
            else:
                BTC_onemonth_topic_dict[topic_list[i]] = BTC_onemonth_topic_dict.get(topic_list[i]) + enhance_weight * (1 - ((Now - datetime.datetime.strptime(time, time_format)).seconds + (Now - datetime.datetime.strptime(time, time_format)).days * 86400)/2592000)
            
            # Add new id in dictionary
            if BTC_onemonth_id_dict.get(topic_list[i]) == None:
                l = [ID]
                BTC_onemonth_id_dict[topic_list[i]] = l
            else:
                BTC_onemonth_id_dict[topic_list[i]].append(ID)
    
    for (line, time, ID, importance) in zip(BTC_threemonths_headline_list, BTC_threemonths_time_list, BTC_threemonths_ID_list, BTC_threemonths_importance_list):

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
            if BTC_threemonths_topic_dict.get(topic_list[i]) == None:
                BTC_threemonths_topic_dict[topic_list[i]] = enhance_weight * (1 - ((Now - datetime.datetime.strptime(time, time_format)).seconds + (Now - datetime.datetime.strptime(time, time_format)).days * 86400)/7776000)
            # Add weight
            else:
                BTC_threemonths_topic_dict[topic_list[i]] = BTC_threemonths_topic_dict.get(topic_list[i]) + enhance_weight * (1 - ((Now - datetime.datetime.strptime(time, time_format)).seconds + (Now - datetime.datetime.strptime(time, time_format)).days * 86400)/7776000)
    
            # Add new id in dictionary
            if BTC_threemonths_id_dict.get(topic_list[i]) == None:
                l = [ID]
                BTC_threemonths_id_dict[topic_list[i]] = l
            else:
                BTC_threemonths_id_dict[topic_list[i]].append(ID)


    twelvehours_trend = sorted(BTC_twelvehours_topic_dict.items(), key = lambda x:x[1], reverse = True)

    twelvehours_trend_json = json.dumps(dict(twelvehours_trend[0:15]))


    oneday_trend = sorted(BTC_oneday_topic_dict.items(), key = lambda x:x[1], reverse = True)

    oneday_trend_json = json.dumps(dict(oneday_trend[0:15]))



    oneweek_trend = sorted(BTC_oneweek_topic_dict.items(), key = lambda x:x[1], reverse = True)

    oneweek_trend_json = json.dumps(dict(oneweek_trend[0:15]))


    onemonth_trend = sorted(BTC_onemonth_topic_dict.items(), key = lambda x:x[1], reverse = True)

    onemonth_trend_json = json.dumps(dict(onemonth_trend[0:15]))
    

    threemonths_trend = sorted(BTC_threemonths_topic_dict.items(), key = lambda x:x[1], reverse = True)

    threemonths_trend_json = json.dumps(dict(threemonths_trend[0:15]))


    twelvehours_trend_json = []
    for k in twelvehours_trend[0:15] :
        subitem = {}
        subitem["text"] = k[0]
        subitem["weight"] = round(k[1], 2)
        subitem["ids"] = ','.join(str(e) for e in BTC_twelvehours_id_dict.get(k[0]))
        if len(subitem["ids"]) < 8:
            continue
        twelvehours_trend_json.append(subitem)
        # twelvehours_trend_json.append(json.dumps(subitem))

    oneday_trend_json = []
    for k in oneday_trend[0:15] :
        subitem = {}
        subitem["text"] = k[0]
        subitem["weight"] = round(k[1], 2)
        subitem["ids"] = ','.join(str(e) for e in BTC_oneday_id_dict.get(k[0]))
        if len(subitem["ids"]) < 8:
            continue
        oneday_trend_json.append(subitem)
        # oneday_trend_json.append(json.dumps(subitem))

    oneweek_trend_json = []
    for k in oneweek_trend[0:15] :
        subitem = {}
        subitem["text"] = k[0]
        subitem["weight"] = round(k[1], 2)
        subitem["ids"] = ','.join(str(e) for e in BTC_oneweek_id_dict.get(k[0]))
        if len(subitem["ids"]) < 8:
            continue
        oneweek_trend_json.append(subitem)
        # oneweek_trend_json.append(json.dumps(subitem))
    
    onemonth_trend_json = []
    for k in onemonth_trend[0:15] :
        subitem = {}
        subitem["text"] = k[0]
        subitem["weight"] = round(k[1], 2)
        subitem["ids"] = ','.join(str(e) for e in BTC_onemonth_id_dict.get(k[0]))
        if len(subitem["ids"]) < 8:
            continue
        onemonth_trend_json.append(subitem)
        # onemonth_trend_json.append(json.dumps(subitem))

    threemonths_trend_json = []
    for k in threemonths_trend[0:15] :
        subitem = {}
        subitem["text"] = k[0]
        subitem["weight"] = round(k[1], 2)
        subitem["ids"] = ','.join(str(e) for e in BTC_threemonths_id_dict.get(k[0]))
        if len(subitem["ids"]) < 8:
            continue
        threemonths_trend_json.append(subitem)
        # threemonths_trend_json.append(json.dumps(subitem))
    BTC_event_dict["twelvehours"] = json.dumps(twelvehours_trend_json)
    BTC_event_dict["oneday"] = json.dumps(oneday_trend_json)
    BTC_event_dict["oneweek"] = json.dumps(oneweek_trend_json)
    BTC_event_dict["onemonth"] = json.dumps(onemonth_trend_json)
    BTC_event_dict["threemonths"] = json.dumps(threemonths_trend_json)

    for (line, time, ID, importance) in zip(ETH_twelvehours_headline_list, ETH_twelvehours_time_list, ETH_twelvehours_ID_list, ETH_twelvehours_importance_list):

        
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
            if ETH_twelvehours_topic_dict.get(topic_list[i]) == None:
                ETH_twelvehours_topic_dict[topic_list[i]] = enhance_weight * (1 - (Now - datetime.datetime.strptime(time, time_format)).seconds/43200)
            # Add weight
            else:
                ETH_twelvehours_topic_dict[topic_list[i]] = ETH_twelvehours_topic_dict.get(topic_list[i]) + enhance_weight * (1 - (Now - datetime.datetime.strptime(time, time_format)).seconds/43200)

            # Add new id in dictionary
            if ETH_twelvehours_id_dict.get(topic_list[i]) == None:
                l = [ID]
                ETH_twelvehours_id_dict[topic_list[i]] = l
            else:
                ETH_twelvehours_id_dict[topic_list[i]].append(ID)  

    for (line, time, ID, importance) in zip(ETH_oneday_headline_list, ETH_oneday_time_list, ETH_oneday_ID_list, ETH_oneday_importance_list):
        
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
            if ETH_oneday_topic_dict.get(topic_list[i]) == None:
                ETH_oneday_topic_dict[topic_list[i]] = enhance_weight * (1 - (Now - datetime.datetime.strptime(time, time_format)).seconds/86400)
            # Add weight
            else:
                ETH_oneday_topic_dict[topic_list[i]] = ETH_oneday_topic_dict.get(topic_list[i]) + enhance_weight * (1 - (Now - datetime.datetime.strptime(time, time_format)).seconds/86400)

            # Add new id in dictionary
            if ETH_oneday_id_dict.get(topic_list[i]) == None:
                l = [ID]
                ETH_oneday_id_dict[topic_list[i]] = l
            else:
                ETH_oneday_id_dict[topic_list[i]].append(ID)

    for (line, time, ID, importance) in zip(ETH_oneweek_headline_list, ETH_oneweek_time_list, ETH_oneweek_ID_list, ETH_oneweek_importance_list):
        
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
            if ETH_oneweek_topic_dict.get(topic_list[i]) == None:
                ETH_oneweek_topic_dict[topic_list[i]] = enhance_weight * (1 - ((Now - datetime.datetime.strptime(time, time_format)).seconds + (Now - datetime.datetime.strptime(time, time_format)).days * 86400)/604800)
            # Add weight
            else:
                ETH_oneweek_topic_dict[topic_list[i]] = ETH_oneweek_topic_dict.get(topic_list[i]) + enhance_weight * (1 - ((Now - datetime.datetime.strptime(time, time_format)).seconds + (Now - datetime.datetime.strptime(time, time_format)).days * 86400)/604800)

            # Add new id in dictionary
            if ETH_oneweek_id_dict.get(topic_list[i]) == None:
                l = [ID]
                ETH_oneweek_id_dict[topic_list[i]] = l
            else:
                ETH_oneweek_id_dict[topic_list[i]].append(ID)

    for (line, time, ID, importance) in zip(ETH_onemonth_headline_list, ETH_onemonth_time_list, ETH_onemonth_ID_list, ETH_onemonth_importance_list):
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
            if ETH_onemonth_topic_dict.get(topic_list[i]) == None:
                ETH_onemonth_topic_dict[topic_list[i]] = enhance_weight * (1 - ((Now - datetime.datetime.strptime(time, time_format)).seconds + (Now - datetime.datetime.strptime(time, time_format)).days * 86400)/2592000)
            # Add weight
            else:
                ETH_onemonth_topic_dict[topic_list[i]] = ETH_onemonth_topic_dict.get(topic_list[i]) + enhance_weight * (1 - ((Now - datetime.datetime.strptime(time, time_format)).seconds + (Now - datetime.datetime.strptime(time, time_format)).days * 86400)/2592000)
            
            # Add new id in dictionary
            if ETH_onemonth_id_dict.get(topic_list[i]) == None:
                l = [ID]
                ETH_onemonth_id_dict[topic_list[i]] = l
            else:
                ETH_onemonth_id_dict[topic_list[i]].append(ID)
    
    for (line, time, ID, importance) in zip(ETH_threemonths_headline_list, ETH_threemonths_time_list, ETH_threemonths_ID_list, ETH_threemonths_importance_list):

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
            if ETH_threemonths_topic_dict.get(topic_list[i]) == None:
                ETH_threemonths_topic_dict[topic_list[i]] = enhance_weight * (1 - ((Now - datetime.datetime.strptime(time, time_format)).seconds + (Now - datetime.datetime.strptime(time, time_format)).days * 86400)/7776000)
            # Add weight
            else:
                ETH_threemonths_topic_dict[topic_list[i]] = ETH_threemonths_topic_dict.get(topic_list[i]) + enhance_weight * (1 - ((Now - datetime.datetime.strptime(time, time_format)).seconds + (Now - datetime.datetime.strptime(time, time_format)).days * 86400)/7776000)
    
            # Add new id in dictionary
            if ETH_threemonths_id_dict.get(topic_list[i]) == None:
                l = [ID]
                ETH_threemonths_id_dict[topic_list[i]] = l
            else:
                ETH_threemonths_id_dict[topic_list[i]].append(ID)



    twelvehours_trend = sorted(ETH_twelvehours_topic_dict.items(), key = lambda x:x[1], reverse = True)

    twelvehours_trend_json = json.dumps(dict(twelvehours_trend[0:15]))


    oneday_trend = sorted(ETH_oneday_topic_dict.items(), key = lambda x:x[1], reverse = True)

    oneday_trend_json = json.dumps(dict(oneday_trend[0:15]))



    oneweek_trend = sorted(ETH_oneweek_topic_dict.items(), key = lambda x:x[1], reverse = True)

    oneweek_trend_json = json.dumps(dict(oneweek_trend[0:15]))


    onemonth_trend = sorted(ETH_onemonth_topic_dict.items(), key = lambda x:x[1], reverse = True)

    onemonth_trend_json = json.dumps(dict(onemonth_trend[0:15]))
    

    threemonths_trend = sorted(ETH_threemonths_topic_dict.items(), key = lambda x:x[1], reverse = True)

    threemonths_trend_json = json.dumps(dict(threemonths_trend[0:15]))


    twelvehours_trend_json = []
    for k in twelvehours_trend[0:15] :
        subitem = {}
        subitem["text"] = k[0]
        subitem["weight"] = round(k[1], 2)
        subitem["ids"] = ','.join(str(e) for e in ETH_twelvehours_id_dict.get(k[0]))
        if len(subitem["ids"]) < 8:
            continue
        twelvehours_trend_json.append(subitem)
        # twelvehours_trend_json.append(json.dumps(subitem))

    oneday_trend_json = []
    for k in oneday_trend[0:15] :
        subitem = {}
        subitem["text"] = k[0]
        subitem["weight"] = round(k[1], 2)
        subitem["ids"] = ','.join(str(e) for e in ETH_oneday_id_dict.get(k[0]))
        if len(subitem["ids"]) < 8:
            continue
        oneday_trend_json.append(subitem)
        # oneday_trend_json.append(json.dumps(subitem))

    oneweek_trend_json = []
    for k in oneweek_trend[0:15] :
        subitem = {}
        subitem["text"] = k[0]
        subitem["weight"] = round(k[1], 2)
        subitem["ids"] = ','.join(str(e) for e in ETH_oneweek_id_dict.get(k[0]))
        if len(subitem["ids"]) < 8:
            continue
        oneweek_trend_json.append(subitem)
        # oneweek_trend_json.append(json.dumps(subitem))
    
    onemonth_trend_json = []
    for k in onemonth_trend[0:15] :
        subitem = {}
        subitem["text"] = k[0]
        subitem["weight"] = round(k[1], 2)
        subitem["ids"] = ','.join(str(e) for e in ETH_onemonth_id_dict.get(k[0]))
        if len(subitem["ids"]) < 8:
            continue
        onemonth_trend_json.append(subitem)
        # onemonth_trend_json.append(json.dumps(subitem))

    threemonths_trend_json = []
    for k in threemonths_trend[0:15] :
        subitem = {}
        subitem["text"] = k[0]
        subitem["weight"] = round(k[1], 2)
        subitem["ids"] = ','.join(str(e) for e in ETH_threemonths_id_dict.get(k[0]))
        if len(subitem["ids"]) < 8:
            continue
        threemonths_trend_json.append(subitem)
        # threemonths_trend_json.append(json.dumps(subitem))
    ETH_event_dict["twelvehours"] = json.dumps(twelvehours_trend_json)
    ETH_event_dict["oneday"] = json.dumps(oneday_trend_json)
    ETH_event_dict["oneweek"] = json.dumps(oneweek_trend_json)
    ETH_event_dict["onemonth"] = json.dumps(onemonth_trend_json)
    ETH_event_dict["threemonths"] = json.dumps(threemonths_trend_json)


    for (line, time, ID, importance) in zip(XRP_twelvehours_headline_list, XRP_twelvehours_time_list, XRP_twelvehours_ID_list, XRP_twelvehours_importance_list):

        
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
            if XRP_twelvehours_topic_dict.get(topic_list[i]) == None:
                XRP_twelvehours_topic_dict[topic_list[i]] = enhance_weight * (1 - (Now - datetime.datetime.strptime(time, time_format)).seconds/43200)
            # Add weight
            else:
                XRP_twelvehours_topic_dict[topic_list[i]] = XRP_twelvehours_topic_dict.get(topic_list[i]) + enhance_weight * (1 - (Now - datetime.datetime.strptime(time, time_format)).seconds/43200)

            # Add new id in dictionary
            if XRP_twelvehours_id_dict.get(topic_list[i]) == None:
                l = [ID]
                XRP_twelvehours_id_dict[topic_list[i]] = l
            else:
                XRP_twelvehours_id_dict[topic_list[i]].append(ID)  

    for (line, time, ID, importance) in zip(XRP_oneday_headline_list, XRP_oneday_time_list, XRP_oneday_ID_list, XRP_oneday_importance_list):
        
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
            if XRP_oneday_topic_dict.get(topic_list[i]) == None:
                XRP_oneday_topic_dict[topic_list[i]] = enhance_weight * (1 - (Now - datetime.datetime.strptime(time, time_format)).seconds/86400)
            # Add weight
            else:
                XRP_oneday_topic_dict[topic_list[i]] = XRP_oneday_topic_dict.get(topic_list[i]) + enhance_weight * (1 - (Now - datetime.datetime.strptime(time, time_format)).seconds/86400)

            # Add new id in dictionary
            if XRP_oneday_id_dict.get(topic_list[i]) == None:
                l = [ID]
                XRP_oneday_id_dict[topic_list[i]] = l
            else:
                XRP_oneday_id_dict[topic_list[i]].append(ID)

    for (line, time, ID, importance) in zip(XRP_oneweek_headline_list, XRP_oneweek_time_list, XRP_oneweek_ID_list, XRP_oneweek_importance_list):
        
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
            if XRP_oneweek_topic_dict.get(topic_list[i]) == None:
                XRP_oneweek_topic_dict[topic_list[i]] = enhance_weight * (1 - ((Now - datetime.datetime.strptime(time, time_format)).seconds + (Now - datetime.datetime.strptime(time, time_format)).days * 86400)/604800)
            # Add weight
            else:
                XRP_oneweek_topic_dict[topic_list[i]] = XRP_oneweek_topic_dict.get(topic_list[i]) + enhance_weight * (1 - ((Now - datetime.datetime.strptime(time, time_format)).seconds + (Now - datetime.datetime.strptime(time, time_format)).days * 86400)/604800)

            # Add new id in dictionary
            if XRP_oneweek_id_dict.get(topic_list[i]) == None:
                l = [ID]
                XRP_oneweek_id_dict[topic_list[i]] = l
            else:
                XRP_oneweek_id_dict[topic_list[i]].append(ID)

    for (line, time, ID, importance) in zip(XRP_onemonth_headline_list, XRP_onemonth_time_list, XRP_onemonth_ID_list, XRP_onemonth_importance_list):
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
            if XRP_onemonth_topic_dict.get(topic_list[i]) == None:
                XRP_onemonth_topic_dict[topic_list[i]] = enhance_weight * (1 - ((Now - datetime.datetime.strptime(time, time_format)).seconds + (Now - datetime.datetime.strptime(time, time_format)).days * 86400)/2592000)
            # Add weight
            else:
                XRP_onemonth_topic_dict[topic_list[i]] = XRP_onemonth_topic_dict.get(topic_list[i]) + enhance_weight * (1 - ((Now - datetime.datetime.strptime(time, time_format)).seconds + (Now - datetime.datetime.strptime(time, time_format)).days * 86400)/2592000)
            
            # Add new id in dictionary
            if XRP_onemonth_id_dict.get(topic_list[i]) == None:
                l = [ID]
                XRP_onemonth_id_dict[topic_list[i]] = l
            else:
                XRP_onemonth_id_dict[topic_list[i]].append(ID)
    
    for (line, time, ID, importance) in zip(XRP_threemonths_headline_list, XRP_threemonths_time_list, XRP_threemonths_ID_list, XRP_threemonths_importance_list):

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
            if XRP_threemonths_topic_dict.get(topic_list[i]) == None:
                XRP_threemonths_topic_dict[topic_list[i]] = enhance_weight * (1 - ((Now - datetime.datetime.strptime(time, time_format)).seconds + (Now - datetime.datetime.strptime(time, time_format)).days * 86400)/7776000)
            # Add weight
            else:
                XRP_threemonths_topic_dict[topic_list[i]] = XRP_threemonths_topic_dict.get(topic_list[i]) + enhance_weight * (1 - ((Now - datetime.datetime.strptime(time, time_format)).seconds + (Now - datetime.datetime.strptime(time, time_format)).days * 86400)/7776000)
    
            # Add new id in dictionary
            if XRP_threemonths_id_dict.get(topic_list[i]) == None:
                l = [ID]
                XRP_threemonths_id_dict[topic_list[i]] = l
            else:
                XRP_threemonths_id_dict[topic_list[i]].append(ID)



    twelvehours_trend = sorted(XRP_twelvehours_topic_dict.items(), key = lambda x:x[1], reverse = True)

    twelvehours_trend_json = json.dumps(dict(twelvehours_trend[0:15]))


    oneday_trend = sorted(XRP_oneday_topic_dict.items(), key = lambda x:x[1], reverse = True)

    oneday_trend_json = json.dumps(dict(oneday_trend[0:15]))



    oneweek_trend = sorted(XRP_oneweek_topic_dict.items(), key = lambda x:x[1], reverse = True)

    oneweek_trend_json = json.dumps(dict(oneweek_trend[0:15]))


    onemonth_trend = sorted(XRP_onemonth_topic_dict.items(), key = lambda x:x[1], reverse = True)

    onemonth_trend_json = json.dumps(dict(onemonth_trend[0:15]))
    

    threemonths_trend = sorted(XRP_threemonths_topic_dict.items(), key = lambda x:x[1], reverse = True)

    threemonths_trend_json = json.dumps(dict(threemonths_trend[0:15]))


    twelvehours_trend_json = []
    for k in twelvehours_trend[0:15] :
        subitem = {}
        subitem["text"] = k[0]
        subitem["weight"] = round(k[1], 2)
        subitem["ids"] = ','.join(str(e) for e in XRP_twelvehours_id_dict.get(k[0]))
        if len(subitem["ids"]) < 8:
            continue
        twelvehours_trend_json.append(subitem)
        # twelvehours_trend_json.append(json.dumps(subitem))

    oneday_trend_json = []
    for k in oneday_trend[0:15] :
        subitem = {}
        subitem["text"] = k[0]
        subitem["weight"] = round(k[1], 2)
        subitem["ids"] = ','.join(str(e) for e in XRP_oneday_id_dict.get(k[0]))
        if len(subitem["ids"]) < 8:
            continue
        oneday_trend_json.append(subitem)
        # oneday_trend_json.append(json.dumps(subitem))

    oneweek_trend_json = []
    for k in oneweek_trend[0:15] :
        subitem = {}
        subitem["text"] = k[0]
        subitem["weight"] = round(k[1], 2)
        subitem["ids"] = ','.join(str(e) for e in XRP_oneweek_id_dict.get(k[0]))
        if len(subitem["ids"]) < 8:
            continue
        oneweek_trend_json.append(subitem)
        # oneweek_trend_json.append(json.dumps(subitem))
    
    onemonth_trend_json = []
    for k in onemonth_trend[0:15] :
        subitem = {}
        subitem["text"] = k[0]
        subitem["weight"] = round(k[1], 2)
        subitem["ids"] = ','.join(str(e) for e in XRP_onemonth_id_dict.get(k[0]))
        if len(subitem["ids"]) < 8:
            continue
        onemonth_trend_json.append(subitem)
        # onemonth_trend_json.append(json.dumps(subitem))

    threemonths_trend_json = []
    for k in threemonths_trend[0:15] :
        subitem = {}
        subitem["text"] = k[0]
        subitem["weight"] = round(k[1], 2)
        subitem["ids"] = ','.join(str(e) for e in XRP_threemonths_id_dict.get(k[0]))
        if len(subitem["ids"]) < 8:
            continue
        threemonths_trend_json.append(subitem)
        # threemonths_trend_json.append(json.dumps(subitem))
    XRP_event_dict["twelvehours"] = json.dumps(twelvehours_trend_json)
    XRP_event_dict["oneday"] = json.dumps(oneday_trend_json)
    XRP_event_dict["oneweek"] = json.dumps(oneweek_trend_json)
    XRP_event_dict["onemonth"] = json.dumps(onemonth_trend_json)
    XRP_event_dict["threemonths"] = json.dumps(threemonths_trend_json)



    for (line, time, ID, importance) in zip(BCH_twelvehours_headline_list, BCH_twelvehours_time_list, BCH_twelvehours_ID_list, BCH_twelvehours_importance_list):

        
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
            if BCH_twelvehours_topic_dict.get(topic_list[i]) == None:
                BCH_twelvehours_topic_dict[topic_list[i]] = enhance_weight * (1 - (Now - datetime.datetime.strptime(time, time_format)).seconds/43200)
            # Add weight
            else:
                BCH_twelvehours_topic_dict[topic_list[i]] = BCH_twelvehours_topic_dict.get(topic_list[i]) + enhance_weight * (1 - (Now - datetime.datetime.strptime(time, time_format)).seconds/43200)

            # Add new id in dictionary
            if BCH_twelvehours_id_dict.get(topic_list[i]) == None:
                l = [ID]
                BCH_twelvehours_id_dict[topic_list[i]] = l
            else:
                BCH_twelvehours_id_dict[topic_list[i]].append(ID)  

    for (line, time, ID, importance) in zip(BCH_oneday_headline_list, BCH_oneday_time_list, BCH_oneday_ID_list, BCH_oneday_importance_list):
        
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
            if BCH_oneday_topic_dict.get(topic_list[i]) == None:
                BCH_oneday_topic_dict[topic_list[i]] = enhance_weight * (1 - (Now - datetime.datetime.strptime(time, time_format)).seconds/86400)
            # Add weight
            else:
                BCH_oneday_topic_dict[topic_list[i]] = BCH_oneday_topic_dict.get(topic_list[i]) + enhance_weight * (1 - (Now - datetime.datetime.strptime(time, time_format)).seconds/86400)

            # Add new id in dictionary
            if BCH_oneday_id_dict.get(topic_list[i]) == None:
                l = [ID]
                BCH_oneday_id_dict[topic_list[i]] = l
            else:
                BCH_oneday_id_dict[topic_list[i]].append(ID)

    for (line, time, ID, importance) in zip(BCH_oneweek_headline_list, BCH_oneweek_time_list, BCH_oneweek_ID_list, BCH_oneweek_importance_list):
        
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
            if BCH_oneweek_topic_dict.get(topic_list[i]) == None:
                BCH_oneweek_topic_dict[topic_list[i]] = enhance_weight * (1 - ((Now - datetime.datetime.strptime(time, time_format)).seconds + (Now - datetime.datetime.strptime(time, time_format)).days * 86400)/604800)
            # Add weight
            else:
                BCH_oneweek_topic_dict[topic_list[i]] = BCH_oneweek_topic_dict.get(topic_list[i]) + enhance_weight * (1 - ((Now - datetime.datetime.strptime(time, time_format)).seconds + (Now - datetime.datetime.strptime(time, time_format)).days * 86400)/604800)

            # Add new id in dictionary
            if BCH_oneweek_id_dict.get(topic_list[i]) == None:
                l = [ID]
                BCH_oneweek_id_dict[topic_list[i]] = l
            else:
                BCH_oneweek_id_dict[topic_list[i]].append(ID)

    for (line, time, ID, importance) in zip(BCH_onemonth_headline_list, BCH_onemonth_time_list, BCH_onemonth_ID_list, BCH_onemonth_importance_list):
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
            if BCH_onemonth_topic_dict.get(topic_list[i]) == None:
                BCH_onemonth_topic_dict[topic_list[i]] = enhance_weight * (1 - ((Now - datetime.datetime.strptime(time, time_format)).seconds + (Now - datetime.datetime.strptime(time, time_format)).days * 86400)/2592000)
            # Add weight
            else:
                BCH_onemonth_topic_dict[topic_list[i]] = BCH_onemonth_topic_dict.get(topic_list[i]) + enhance_weight * (1 - ((Now - datetime.datetime.strptime(time, time_format)).seconds + (Now - datetime.datetime.strptime(time, time_format)).days * 86400)/2592000)
            
            # Add new id in dictionary
            if BCH_onemonth_id_dict.get(topic_list[i]) == None:
                l = [ID]
                BCH_onemonth_id_dict[topic_list[i]] = l
            else:
                BCH_onemonth_id_dict[topic_list[i]].append(ID)
    
    for (line, time, ID, importance) in zip(BCH_threemonths_headline_list, BCH_threemonths_time_list, BCH_threemonths_ID_list, BCH_threemonths_importance_list):

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
            if BCH_threemonths_topic_dict.get(topic_list[i]) == None:
                BCH_threemonths_topic_dict[topic_list[i]] = enhance_weight * (1 - ((Now - datetime.datetime.strptime(time, time_format)).seconds + (Now - datetime.datetime.strptime(time, time_format)).days * 86400)/7776000)
            # Add weight
            else:
                BCH_threemonths_topic_dict[topic_list[i]] = BCH_threemonths_topic_dict.get(topic_list[i]) + enhance_weight * (1 - ((Now - datetime.datetime.strptime(time, time_format)).seconds + (Now - datetime.datetime.strptime(time, time_format)).days * 86400)/7776000)
    
            # Add new id in dictionary
            if BCH_threemonths_id_dict.get(topic_list[i]) == None:
                l = [ID]
                BCH_threemonths_id_dict[topic_list[i]] = l
            else:
                BCH_threemonths_id_dict[topic_list[i]].append(ID)



    twelvehours_trend = sorted(BCH_twelvehours_topic_dict.items(), key = lambda x:x[1], reverse = True)

    twelvehours_trend_json = json.dumps(dict(twelvehours_trend[0:15]))


    oneday_trend = sorted(BCH_oneday_topic_dict.items(), key = lambda x:x[1], reverse = True)

    oneday_trend_json = json.dumps(dict(oneday_trend[0:15]))



    oneweek_trend = sorted(BCH_oneweek_topic_dict.items(), key = lambda x:x[1], reverse = True)

    oneweek_trend_json = json.dumps(dict(oneweek_trend[0:15]))


    onemonth_trend = sorted(BCH_onemonth_topic_dict.items(), key = lambda x:x[1], reverse = True)

    onemonth_trend_json = json.dumps(dict(onemonth_trend[0:15]))
    

    threemonths_trend = sorted(BCH_threemonths_topic_dict.items(), key = lambda x:x[1], reverse = True)

    threemonths_trend_json = json.dumps(dict(threemonths_trend[0:15]))


    twelvehours_trend_json = []
    for k in twelvehours_trend[0:15] :
        subitem = {}
        subitem["text"] = k[0]
        subitem["weight"] = round(k[1], 2)
        subitem["ids"] = ','.join(str(e) for e in BCH_twelvehours_id_dict.get(k[0]))
        if len(subitem["ids"]) < 8:
            continue
        twelvehours_trend_json.append(subitem)
        # twelvehours_trend_json.append(json.dumps(subitem))

    oneday_trend_json = []
    for k in oneday_trend[0:15] :
        subitem = {}
        subitem["text"] = k[0]
        subitem["weight"] = round(k[1], 2)
        subitem["ids"] = ','.join(str(e) for e in BCH_oneday_id_dict.get(k[0]))
        if len(subitem["ids"]) < 8:
            continue
        oneday_trend_json.append(subitem)
        # oneday_trend_json.append(json.dumps(subitem))

    oneweek_trend_json = []
    for k in oneweek_trend[0:15] :
        subitem = {}
        subitem["text"] = k[0]
        subitem["weight"] = round(k[1], 2)
        subitem["ids"] = ','.join(str(e) for e in BCH_oneweek_id_dict.get(k[0]))
        if len(subitem["ids"]) < 8:
            continue
        oneweek_trend_json.append(subitem)
        # oneweek_trend_json.append(json.dumps(subitem))
    
    onemonth_trend_json = []
    for k in onemonth_trend[0:15] :
        subitem = {}
        subitem["text"] = k[0]
        subitem["weight"] = round(k[1], 2)
        subitem["ids"] = ','.join(str(e) for e in BCH_onemonth_id_dict.get(k[0]))
        if len(subitem["ids"]) < 8:
            continue
        onemonth_trend_json.append(subitem)
        # onemonth_trend_json.append(json.dumps(subitem))

    threemonths_trend_json = []
    for k in threemonths_trend[0:15] :
        subitem = {}
        subitem["text"] = k[0]
        subitem["weight"] = round(k[1], 2)
        subitem["ids"] = ','.join(str(e) for e in BCH_threemonths_id_dict.get(k[0]))
        if len(subitem["ids"]) < 8:
            continue
        threemonths_trend_json.append(subitem)
        # threemonths_trend_json.append(json.dumps(subitem))
    BCH_event_dict["twelvehours"] = json.dumps(twelvehours_trend_json)
    BCH_event_dict["oneday"] = json.dumps(oneday_trend_json)
    BCH_event_dict["oneweek"] = json.dumps(oneweek_trend_json)
    BCH_event_dict["onemonth"] = json.dumps(onemonth_trend_json)
    BCH_event_dict["threemonths"] = json.dumps(threemonths_trend_json)



    for (line, time, ID, importance) in zip(LTC_twelvehours_headline_list, LTC_twelvehours_time_list, LTC_twelvehours_ID_list, LTC_twelvehours_importance_list):

        
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
            if LTC_twelvehours_topic_dict.get(topic_list[i]) == None:
                LTC_twelvehours_topic_dict[topic_list[i]] = enhance_weight * (1 - (Now - datetime.datetime.strptime(time, time_format)).seconds/43200)
            # Add weight
            else:
                LTC_twelvehours_topic_dict[topic_list[i]] = LTC_twelvehours_topic_dict.get(topic_list[i]) + enhance_weight * (1 - (Now - datetime.datetime.strptime(time, time_format)).seconds/43200)

            # Add new id in dictionary
            if LTC_twelvehours_id_dict.get(topic_list[i]) == None:
                l = [ID]
                LTC_twelvehours_id_dict[topic_list[i]] = l
            else:
                LTC_twelvehours_id_dict[topic_list[i]].append(ID)  

    for (line, time, ID, importance) in zip(LTC_oneday_headline_list, LTC_oneday_time_list, LTC_oneday_ID_list, LTC_oneday_importance_list):
        
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
            if LTC_oneday_topic_dict.get(topic_list[i]) == None:
                LTC_oneday_topic_dict[topic_list[i]] = enhance_weight * (1 - (Now - datetime.datetime.strptime(time, time_format)).seconds/86400)
            # Add weight
            else:
                LTC_oneday_topic_dict[topic_list[i]] = LTC_oneday_topic_dict.get(topic_list[i]) + enhance_weight * (1 - (Now - datetime.datetime.strptime(time, time_format)).seconds/86400)

            # Add new id in dictionary
            if LTC_oneday_id_dict.get(topic_list[i]) == None:
                l = [ID]
                LTC_oneday_id_dict[topic_list[i]] = l
            else:
                LTC_oneday_id_dict[topic_list[i]].append(ID)

    for (line, time, ID, importance) in zip(LTC_oneweek_headline_list, LTC_oneweek_time_list, LTC_oneweek_ID_list, LTC_oneweek_importance_list):
        
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
            if LTC_oneweek_topic_dict.get(topic_list[i]) == None:
                LTC_oneweek_topic_dict[topic_list[i]] = enhance_weight * (1 - ((Now - datetime.datetime.strptime(time, time_format)).seconds + (Now - datetime.datetime.strptime(time, time_format)).days * 86400)/604800)
            # Add weight
            else:
                LTC_oneweek_topic_dict[topic_list[i]] = LTC_oneweek_topic_dict.get(topic_list[i]) + enhance_weight * (1 - ((Now - datetime.datetime.strptime(time, time_format)).seconds + (Now - datetime.datetime.strptime(time, time_format)).days * 86400)/604800)

            # Add new id in dictionary
            if LTC_oneweek_id_dict.get(topic_list[i]) == None:
                l = [ID]
                LTC_oneweek_id_dict[topic_list[i]] = l
            else:
                LTC_oneweek_id_dict[topic_list[i]].append(ID)

    for (line, time, ID, importance) in zip(LTC_onemonth_headline_list, LTC_onemonth_time_list, LTC_onemonth_ID_list, LTC_onemonth_importance_list):
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
            if LTC_onemonth_topic_dict.get(topic_list[i]) == None:
                LTC_onemonth_topic_dict[topic_list[i]] = enhance_weight * (1 - ((Now - datetime.datetime.strptime(time, time_format)).seconds + (Now - datetime.datetime.strptime(time, time_format)).days * 86400)/2592000)
            # Add weight
            else:
                LTC_onemonth_topic_dict[topic_list[i]] = LTC_onemonth_topic_dict.get(topic_list[i]) + enhance_weight * (1 - ((Now - datetime.datetime.strptime(time, time_format)).seconds + (Now - datetime.datetime.strptime(time, time_format)).days * 86400)/2592000)
            
            # Add new id in dictionary
            if LTC_onemonth_id_dict.get(topic_list[i]) == None:
                l = [ID]
                LTC_onemonth_id_dict[topic_list[i]] = l
            else:
                LTC_onemonth_id_dict[topic_list[i]].append(ID)
    
    for (line, time, ID, importance) in zip(LTC_threemonths_headline_list, LTC_threemonths_time_list, LTC_threemonths_ID_list, LTC_threemonths_importance_list):

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
            if LTC_threemonths_topic_dict.get(topic_list[i]) == None:
                LTC_threemonths_topic_dict[topic_list[i]] = enhance_weight * (1 - ((Now - datetime.datetime.strptime(time, time_format)).seconds + (Now - datetime.datetime.strptime(time, time_format)).days * 86400)/7776000)
            # Add weight
            else:
                LTC_threemonths_topic_dict[topic_list[i]] = LTC_threemonths_topic_dict.get(topic_list[i]) + enhance_weight * (1 - ((Now - datetime.datetime.strptime(time, time_format)).seconds + (Now - datetime.datetime.strptime(time, time_format)).days * 86400)/7776000)
    
            # Add new id in dictionary
            if LTC_threemonths_id_dict.get(topic_list[i]) == None:
                l = [ID]
                LTC_threemonths_id_dict[topic_list[i]] = l
            else:
                LTC_threemonths_id_dict[topic_list[i]].append(ID)



    twelvehours_trend = sorted(LTC_twelvehours_topic_dict.items(), key = lambda x:x[1], reverse = True)

    twelvehours_trend_json = json.dumps(dict(twelvehours_trend[0:15]))


    oneday_trend = sorted(LTC_oneday_topic_dict.items(), key = lambda x:x[1], reverse = True)

    oneday_trend_json = json.dumps(dict(oneday_trend[0:15]))



    oneweek_trend = sorted(LTC_oneweek_topic_dict.items(), key = lambda x:x[1], reverse = True)

    oneweek_trend_json = json.dumps(dict(oneweek_trend[0:15]))


    onemonth_trend = sorted(LTC_onemonth_topic_dict.items(), key = lambda x:x[1], reverse = True)

    onemonth_trend_json = json.dumps(dict(onemonth_trend[0:15]))
    

    threemonths_trend = sorted(LTC_threemonths_topic_dict.items(), key = lambda x:x[1], reverse = True)

    threemonths_trend_json = json.dumps(dict(threemonths_trend[0:15]))


    twelvehours_trend_json = []
    for k in twelvehours_trend[0:15] :
        subitem = {}
        subitem["text"] = k[0]
        subitem["weight"] = round(k[1], 2)
        subitem["ids"] = ','.join(str(e) for e in LTC_twelvehours_id_dict.get(k[0]))
        if len(subitem["ids"]) < 8:
            continue
        twelvehours_trend_json.append(subitem)
        # twelvehours_trend_json.append(json.dumps(subitem))

    oneday_trend_json = []
    for k in oneday_trend[0:15] :
        subitem = {}
        subitem["text"] = k[0]
        subitem["weight"] = round(k[1], 2)
        subitem["ids"] = ','.join(str(e) for e in LTC_oneday_id_dict.get(k[0]))
        if len(subitem["ids"]) < 8:
            continue
        oneday_trend_json.append(subitem)
        # oneday_trend_json.append(json.dumps(subitem))

    oneweek_trend_json = []
    for k in oneweek_trend[0:15] :
        subitem = {}
        subitem["text"] = k[0]
        subitem["weight"] = round(k[1], 2)
        subitem["ids"] = ','.join(str(e) for e in LTC_oneweek_id_dict.get(k[0]))
        if len(subitem["ids"]) < 8:
            continue
        oneweek_trend_json.append(subitem)
        # oneweek_trend_json.append(json.dumps(subitem))
    
    onemonth_trend_json = []
    for k in onemonth_trend[0:15] :
        subitem = {}
        subitem["text"] = k[0]
        subitem["weight"] = round(k[1], 2)
        subitem["ids"] = ','.join(str(e) for e in LTC_onemonth_id_dict.get(k[0]))
        if len(subitem["ids"]) < 8:
            continue
        onemonth_trend_json.append(subitem)
        # onemonth_trend_json.append(json.dumps(subitem))

    threemonths_trend_json = []
    for k in threemonths_trend[0:15] :
        subitem = {}
        subitem["text"] = k[0]
        subitem["weight"] = round(k[1], 2)
        subitem["ids"] = ','.join(str(e) for e in LTC_threemonths_id_dict.get(k[0]))
        if len(subitem["ids"]) < 8:
            continue
        threemonths_trend_json.append(subitem)
        # threemonths_trend_json.append(json.dumps(subitem))
    LTC_event_dict["twelvehours"] = json.dumps(twelvehours_trend_json)
    LTC_event_dict["oneday"] = json.dumps(oneday_trend_json)
    LTC_event_dict["oneweek"] = json.dumps(oneweek_trend_json)
    LTC_event_dict["onemonth"] = json.dumps(onemonth_trend_json)
    LTC_event_dict["threemonths"] = json.dumps(threemonths_trend_json)






    add_to_mysql()
    

one_time_import()
pusher = pysher.Pusher("25d8d236bc7237b8c5d6", cluster='us2', secret="826a351f3e62e24152ee", )
# contents = urllib.request.urlopen("https:beta.terminal.io/api/v1/oauth/authenticate").read()
# r = requests.post("https://beta.cryptoterminal.io/api/v1/broadcast/auth?channel_name=headline", headers={"Accept":"application/json", "Authorization":"Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiIsImp0aSI6ImQzZmRjOWU0NGU1N2JlMTZkOTRjN2RhMGFlMjQyNGE2N2UyY2YzNmI3ZTBhMmE4OGRmZTM0ZTg2MTNmMGIxNDFmMzcyNWJhZTljMjgzMzM3In0.eyJhdWQiOiIzIiwianRpIjoiZDNmZGM5ZTQ0ZTU3YmUxNmQ5NGM3ZGEwYWUyNDI0YTY3ZTJjZjM2YjdlMGEyYTg4ZGZlMzRlODYxM2YwYjE0MWYzNzI1YmFlOWMyODMzMzciLCJpYXQiOjE1NDIzMTYzMjIsIm5iZiI6MTU0MjMxNjMyMiwiZXhwIjoxNTczODUyMzIyLCJzdWIiOiI4OCIsInNjb3BlcyI6W119.fAPGi60UQsVtvDQ1Y-K9Nsol7F1bJtdpXuZWYGG3nQ5YtGqVx0GlPLWI0fPKxLPmT6L54CM5458c5LiDSqxzuJj2N4_TZBwQGOec2L09dus5R0Gk_vaIAVLZWNVcJdWql7_3kj2LnffsSGLB7Be-eXXAnxkzztjJPQr3GDtFx-v3Axe3pUoQZIrcKDriY0ureiNre_HJPzLyXzggWkXZa-3Hpd-W_Al93moYMYmn260yuz-epRyQDC3WADGi1Bi_aGea9JUtRxpjUnimMvz2VxiL4Z1NhaoM-OLAPCm6FwesPTUDGOJ_IeaRTGMFXV6W5eybK_BHsN28NVRUDbXlJPfsZNzhovYjYDVHCnXH7b53hq3Zx8gELUGT2POBAMhPNBPFxEjXG20btfflU8x8734lSOkvotzZajnfCUh3atSuskau2olV1nL1GztViOOtGxe3nfH8Xl3TeX6xpUsrG74Lv5MV7OyeYqkHLwVf2Mq4XmWLegWXrE-OE6XUhqELY79wCYXqpqt12P-iqsELXW1r-A0iDdn4RQGCOMIQO4MrUJwyT-4j4FwzWOsFaIhsUKzvhWSKHauH0SYDr8FZHUKr7H66XrThhGU2UDWq9fjfBF9mLLoDC-00NvTjH_ZaN16245K85Mf71qfNcl4GqegRsIa2K2FtT2UC_Ij_t28"})
pusher.connection.bind('pusher:connection_established', connect_handler)
pusher.connect()

push = Pusher("551871", "25d8d236bc7237b8c5d6", "826a351f3e62e24152ee", cluster="us2")

def push_json():
    for key, value in BTC_event_dict_plusID.items():
        if value:
                
            print("push:")
            print("=========================================")
            print("value is:")
            print(value)
            print("=========================================")
            
            push.trigger(channel_BTC, "App\\Events\\"+key, value[1:-1])
            
        else:
            print("{} is empty ".format(key))

    for key, value in ETH_event_dict_plusID.items():
        if value:
                
            print("push:")
            print("=========================================")
            print("value is:")
            print(value)
            print("=========================================")
            
            push.trigger(channel_ETH, "App\\Events\\"+key, value[1:-1])
            
        else:
            print("{} is empty ".format(key))

    for key, value in XRP_event_dict_plusID.items():
        if value:
                
            print("push:")
            print("=========================================")
            print("value is:")
            print(value)
            print("=========================================")
            
            push.trigger(channel_XRP, "App\\Events\\"+key, value[1:-1])
            
        else:
            print("{} is empty ".format(key))

    for key, value in BCH_event_dict_plusID.items():
        if value:
                
            print("push:")
            print("=========================================")
            print("value is:")
            print(value)
            print("=========================================")
            
            push.trigger(channel_BCH, "App\\Events\\"+key, value[1:-1])
            
        else:
            print("{} is empty ".format(key))

    for key, value in LTC_event_dict_plusID.items():
        if value:
                
            print("push:")
            print("=========================================")
            print("value is:")
            print(value)
            print("=========================================")
            
            push.trigger(channel_LTC, "App\\Events\\"+key, value[1:-1])
            
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
