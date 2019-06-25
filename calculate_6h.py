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

from datetime import datetime

KEEP_TIME = 21600
DECAY_SPEED = 5

lemmatizer = WordNetLemmatizer()
stemmer = PorterStemmer()
stop = set(stopwords.words('english'))

headline_list = []
time_list = []
importance_list = []
topic_dict = {}

report_list = ["long on", "short on", "worth of", "USD) transferred"]

clean_word_dic = {}

time_format = '%Y-%m-%d %H:%M:%S'

Now = datetime.strptime('2018-11-20 20:53:10', time_format)

def headline_cutting(headline):
    
    is_report = False
    for report_word in report_list:
        if report_word in headline:
            is_report = True
            return [], is_report
    
    words = headline.split()
    topic_list = []
    word_list = []
    clean_headline = ""
    for word in words:
        if word[0] == '@' or word[0] == '#' or word[0] == '&':
            continue
        word = word.replace(',', '')
        word = word.replace('?', '')
        word = word.replace('.', '')
        word = word.replace("'", '')
        word = word.replace("\"", '')
        word = word.replace('-', '')
        if word != '':
            #clean_word = lemmatizer.lemmatize(word)
            #clean_word = stemmer.stem(clean_word)
            clean_word = word.lower()

            if clean_word in stop:
                continue
        else:
            continue
        word_list.append(clean_word)
        clean_headline = clean_headline + clean_word + " "

    # insert 1 word topic:
    for i in range(len(word_list)):
        topic_list.append(word_list[i])
    
    # insert 2 words topic:
    for i in range(len(word_list) - 1):
        topic = word_list[i] + ' ' + word_list[i+1]
        topic_list.append(topic)
    
    # insert 3 words topic:
    for i in range(len(word_list) - 2):
        topic = word_list[i] + ' ' + word_list[i+1] + ' ' + word_list[i+2]
        topic_list.append(topic)

    return topic_list, is_report

def delete_old_topic():
    for i in range(len(headline_list[0])):
        topic_dict[headline_list[0][i]] = topic_dict.get(headline_list[0][i]) - importance_list[0]
        # delete topic if weight = 0
        if topic_dict[headline_list[0][i]] <= 0:
            topic_dict.pop(headline_list[0][i])
    headline_list.pop(0)
    time_list.pop(0)
    importance_list.pop(0)

def decay():
    decay_speed = DECAY_SPEED/KEEP_TIME
    for key in topic_dict:
        topic_dict[key] = topic_dict.get(key) * (1 - decay_speed)
        topic_dict[key] -= 0.001


def my_func(*args, **kwargs):
    # print("processing Args:", args)
    # print("===========================================================")

    headline_list = []
    time_list = []

    with open("headlines.txt") as in1, open("times.txt") as in2:
        for line1, line2 in zip(in1, in2):
            headline_list.append(line1[:-1])
            time_list.append(line2[:-1])
    in1.close()
    in2.close()

    for (line, time) in zip(headline_list, time_list):
        topic_list, is_report = headline_cutting(line)
        if is_report == True:
            continue
        for i in range(len(topic_list)):
            words = topic_list[i].split()
            if len(words) == 1:
                enhance_weight = 1
                continue
            elif len(words) == 2:
                enhance_weight = 1
            else:
                enhance_weight = 1

            # Add new topic in dictionary
            if topic_dict.get(topic_list[i]) == None:
                topic_dict[topic_list[i]] = enhance_weight * (1 - (Now - datetime.strptime(time, time_format)).seconds/75086)
            # Add weight
            else:
                topic_dict[topic_list[i]] = topic_dict.get(topic_list[i]) + enhance_weight * (1 - (Now - datetime.strptime(time, time_format)).seconds/75086)
    
    
   


    trend = sorted(topic_dict.items(), key = lambda x:x[1], reverse = True)

    # get 3 words topics
    i = 0
    trend_3 = []
    trend_3_weight = []
    for key in trend:
        if i >= 25:
            break
        words = key[0].split()
        if len(words) == 3:
            trend_3.append(key)
            trend_3_weight.append(key[1])
        i += 1
    # clean dup in2 words
    i = 0
    for key in trend:
        if i >= 25:
            break
        words = key[0].split()
        if len(words) == 3:
            continue
        for i in range(len(trend_3)):
            if key[0] in trend_3[i][0]:
                if len(words) == 2:
                    topic_dict[key[0]] -= trend_3_weight[i]
        i += 1
    trend = sorted(topic_dict.items(), key = lambda x:x[1], reverse = True)

    # get 2 words topics
    i = 0
    trend_2 = []
    trend_2_weight = []
    for key in trend:
        if i >= 25:
            break
        words = key[0].split()
        if len(words) == 2:
            trend_2.append(key)
            trend_2_weight.append(key[1])
        i += 1
    
    # clean dup in 1 word
    i = 0
    for key in trend:
        if i >= 25:
            break
        words = key[0].split()
        if len(words) == 2 or len(words) == 3:
            continue
        for i in range(len(trend_2)):
            if key[0] in trend_2[i][0]:
                topic_dict[key[0]] -= trend_2_weight[i]
        i += 1

    trend = sorted(topic_dict.items(), key = lambda x:x[1], reverse = True)
    # print(clean_word_dic)
    print(trend[0:25])


my_func()