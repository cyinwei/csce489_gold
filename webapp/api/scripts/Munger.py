import re
import os
import datetime
import sys
import json
import requests
import time
from watson_developer_cloud import ToneAnalyzerV3
import grammar_check
import pandas as pd

class Munger:

    '''
    @input: body text of comment
    @output: True/False depending on if input contains Markdown
    '''
    @staticmethod
    def containsMD(body):
        heading = r'\W#{1,6}\s'
        emphasis1 = r'\*{1,2}[\s\S]+\*{1,2}'
        emphasis2 = r'_{1,2}[\s\S]+_{1,2}'
        emphasis3 = r'~~[\s\S]+~~'
        superscript = r'\w\^\w'
        unordered = r'\W[\*\-\+]\s\S'
        ordered = r'\W\d\.\s\S'
        url = r'\[[\s\S]+\]\(http[s]?://[\w/\.&=\?;\+\-]+\)'
        code = r'`[\s\S]+`'
        quote = r'(&gt;){1,2}[\s\S]+'

        return (re.search(heading, body) is not None
            or re.search(emphasis1, body) is not None
            or re.search(emphasis2, body) is not None
            or re.search(emphasis3, body) is not None
            or re.search(superscript, body) is not None
            or re.search(unordered, body) is not None
            or re.search(ordered, body) is not None
            or re.search(url, body) is not None
            or re.search(code, body) is not None
            or re.search(quote, body) is not None)

    '''
    @input: body text of comment
    @output: True/False depending on if input contains a tl;dr
    '''
    @staticmethod
    def containsTLDR(body):
        tldr = r'[tT][lL];{0,1}[dD][rR]:{0,1}\s'

        return (re.search(tldr, body) is not None)

    '''
    defines a "word" as whitespace separated text.
    nds the number of words within each comment.
    @input: body text of comment
    @output: int -> number of words
    '''
    @staticmethod
    def wordcount(text):
        words = re.findall("\S+", text)
        return len(words)
    '''
    defines a "link" with the http header string "http://".
    finds the number of links within each comment.
    @input: body text of comment
    @output: int -> number of links
    '''
    @staticmethod
    def linkcount(text):
        links = re.findall("http://", text)
        return len(links)

    @staticmethod
    def getTimeofDay(data):
        hour = int(datetime.datetime.fromtimestamp(data).strftime("%H"))
        if hour >= 5 and hour <12:
            return 'Morning'
        elif hour >= 12 and hour < 17:
            return 'Afternoon'
        elif hour >= 17 and hour < 21:
            return 'Evening'
        elif hour >=21 or hour < 5:
            return 'Night'

    @staticmethod
    def emojicount(string):
        index = 0
        count = 0
        string= string.lower()
        while True:
            index = string.find( '\u', index, len(string))
            if index == -1:
                break
            else:
                count+=1
                index +=1
        return count

    @staticmethod
    def get_Wat_json(user, password, x):
        tone_analyzer = ToneAnalyzerV3(username= user, password= password, version='2016-05-19')
        test =  tone_analyzer.tone(text=x)
        temp = test['document_tone']
        return temp

    @staticmethod
    def get_Wat_Anger(json_object):
        return json_object['tone_categories'][0]['tones'][0]['score']

    @staticmethod
    def get_Wat_Disgust(json_object):
        return json_object['tone_categories'][0]['tones'][1]['score']

    @staticmethod
    def get_Wat_Fear(json_object):
        return json_object['tone_categories'][0]['tones'][2]['score']

    @staticmethod
    def get_Wat_Joy(json_object):
        return json_object['tone_categories'][0]['tones'][3]['score']

    @staticmethod
    def get_Wat_Sadness(json_object):
        return json_object['tone_categories'][0]['tones'][4]['score']

    @staticmethod
    def get_Wat_Analytical(json_object):
        return json_object['tone_categories'][1]['tones'][0]['score']

    @staticmethod
    def get_Wat_Confident(json_object):
        return json_object['tone_categories'][1]['tones'][1]['score']

    @staticmethod
    def get_Wat_Tentative(json_object):
        return json_object['tone_categories'][1]['tones'][2]['score']

    @staticmethod
    def get_Wat_Openness(json_object):
        return json_object['tone_categories'][2]['tones'][0]['score']

    @staticmethod
    def get_Wat_Conscientiousness(json_object):
        return json_object['tone_categories'][2]['tones'][1]['score']

    @staticmethod
    def get_Wat_Extraversion(json_object):
        return json_object['tone_categories'][2]['tones'][2]['score']

    @staticmethod
    def get_Wat_Agreeableness(json_object):
        return json_object['tone_categories'][2]['tones'][3]['score']

    @staticmethod
    def get_Wat_Emotional_Range(json_object):
        return json_object['tone_categories'][2]['tones'][4]['score']

    @staticmethod
    def get_Up_Classification(data):
        return int(data/100)

    @staticmethod
    def get_listofwordcount(data, listofwords):
        temp = 0
        for x in listofwords:
            temp += data.split().count(x)
        return temp

    @staticmethod
    def get_sentiment_json(body):
        return  requests.post("http://text-processing.com/api/sentiment/", data={'text': body}).json()

    @staticmethod
    def get_sentiment_neg(json_object):
        return  json_object['probability']['neg']

    @staticmethod
    def get_sentiment_pos(json_object):
        return  json_object['probability']['pos']

    @staticmethod
    def get_sentiment_neutral(json_object):
        return  json_object['probability']['neutral']

    @staticmethod
    def get_sentiment_label(json_object):
        return  json_object['label']

    @staticmethod
    def get_grammer_error_count(body):
        try:
            tool = grammar_check.LanguageTool('en-GB')
            return len(tool.check(body))
        except:
            return 0

    @staticmethod
    def nfl_flair_number(flair):
        teams = ['lions','seahawks','texans','bears','eagles','dolphins','packers','patriots','falcons','panthers',
             'fortyniners','cowboys','saints','broncos','jaguars','raiders','giants','ravens','nfl','bills',
             'browns','colts','vikings','chargers','jets','bengals','steelers','buccaneers','cardinals','chiefs',
             'redskins','titans','rams','twitter','giants official']
        if flair in teams:
            i = 1
            for team in teams:
                if team == flair:
                    return i
                i+=1
        else:
            return 0

    @staticmethod
    def AdviceAnimals_flair_number(flair):
        animals = ['picard','sap','zoid','eel','awesomepenguin','fa','cwolf','iwolf','ocdotter','businesscat',
               'cfox','stoner','nyan','pedo','wonka','fry','aliens','ggg','skid','yuno','allthings','adog','ned']
        if flair in animals:
            i = 1
            for animal in animals:
                if animal == flair:
                    return i
                i+=1
        else:
            return 0

    @staticmethod
    def other_flair(flair):
        if flair == '':
            return False
        else:
            return True

    @staticmethod
    def remove_emptyline(text):
        return os.linesep.join([s for s in text.splitlines() if s])

    @staticmethod
    def munge_dataset(data, badwords, username, password):
        if 'body' in data:
            data['body'] = data['body'].astype(str)

            # Watson
            watson_json = data['body'].map(lambda x: Munger.get_Wat_json(username, password, x))
            data['Watson Anger'] = watson_json.map(lambda x: Munger.get_Wat_Anger(x))
            data['Watson Disgust'] = watson_json.map(lambda x: Munger.get_Wat_Disgust(x))
            data['Watson Fear'] = watson_json.map(lambda x: Munger.get_Wat_Fear(x))
            data['Watson Joy'] = watson_json.map(lambda x: Munger.get_Wat_Joy(x))
            data['Watson Sadness'] = watson_json.map(lambda x: Munger.get_Wat_Sadness(x))
            data['Watson Analytical'] = watson_json.map(lambda x: Munger.get_Wat_Analytical(x))
            data['Watson Confident'] = watson_json.map(lambda x: Munger.get_Wat_Confident(x))
            data['Watson Tenative'] = watson_json.map(lambda x: Munger.get_Wat_Tentative(x))
            data['Watson Openness'] = watson_json.map(lambda x: Munger.get_Wat_Openness(x))
            data['Watson Conscientiousness'] = watson_json.map(lambda x: Munger.get_Wat_Conscientiousness(x))
            data['Watson Extraversion'] = watson_json.map(lambda x: Munger.get_Wat_Extraversion(x))
            data['Watson Agreeableness'] = watson_json.map(lambda x: Munger.get_Wat_Agreeableness(x))
            data['Watson Emotional Range'] = watson_json.map(lambda x: Munger.get_Wat_Emotional_Range(x))

            # Sentiment
            sentiment_json = data['body'].map(lambda x: Munger.get_sentiment_json(x))
            data['Sentiment Negative'] = sentiment_json.map(lambda x: Munger.get_sentiment_neg(x))
            data['Sentiment Neutral'] = sentiment_json.map(lambda x: Munger.get_sentiment_neutral(x))
            data['Sentiment Positive'] = sentiment_json.map(lambda x: Munger.get_sentiment_pos(x))
            data['Sentiment Label'] = sentiment_json.map(lambda x: Munger.get_sentiment_label(x)).map({'neg': 1,'neutral': 2,'pos': 3})

            # Markdown
            data['Contains MD'] = data['body'].map(lambda x: Munger.containsMD(x))

            # tldr
            data['Contains tldr'] = data['body'].map(lambda x: Munger.containsTLDR(x))

            # Word Count
            data['Word Count'] = data['body'].map(lambda x: Munger.wordcount(x))

            # Emoji Count
            data['Emoji Count'] = data['body'].map(lambda x: Munger.emojicount(x))

            # Grammar Errors (Misspelled for consistency)
            data['Grammer Errors'] = data['body'].map(lambda x: Munger.get_grammer_error_count(x))

            # Bad Words
            data['Bad Words'] = data['body'].apply(lambda x: Munger.get_listofwordcount(x, badwords))

        if 'created_utc' in data:
            # Time of Day
            time_of_day = data['created_utc'].map(lambda x: Munger.getTimeofDay(x))
            data['Time of Day'] = time_of_day.map({'Afternoon': 1,'Evening': 2,'Night': 3,'Morning': 4})

        if 'author_flair_css_class' in data and 'subreddit' in data:
            # Flair
            if data['subreddit'].unique()[0] == 'nfl':
                data['flair'] = data['author_flair_css_class'].map(lambda x: Munger.nfl_flair_number(x))
            elif data['subreddit'].unique()[0] == 'Advice Animals':
                data['flair'] = data['author_flair_css_class'].map(lambda x: Munger.AdviceAnimals_flair_number(x))
            else:
                data['flair'] = data['author_flair_css_class'].map(lambda x: Munger.other_flair(x))

        if 'score' in data:
            data['Score Bracket'] = data['score'].map(lambda x: Munger.get_Up_Classification(x))

        return data
