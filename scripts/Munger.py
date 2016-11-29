import re
import datetime
import json
from watson_developer_cloud import ToneAnalyzerV3

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
    def get_Wat_json(x):
        tone_analyzer = ToneAnalyzerV3(username='95a7beae-b5b4-4193-9481-8c2cb028580b', password='YG2mBFbH1R8G', version='2016-05-19')
        return tone_analyzer.tone(text=x)
    
    @staticmethod   
    def get_Anger(x):
        return x['document_tone']['tone_categories'][0]['tones'][0]['score']
    
    @staticmethod
    def get_Disgust(x):
        return x['document_tone']['tone_categories'][0]['tones'][1]['score']

    @staticmethod
    def get_Fear(x):
        return x['document_tone']['tone_categories'][0]['tones'][2]['score']

    @staticmethod
    def get_Joy(x):
        return x['document_tone']['tone_categories'][0]['tones'][3]['score']

    @staticmethod
    def get_Sadness(x):
        return x['document_tone']['tone_categories'][0]['tones'][4]['score']

    @staticmethod
    def get_Analytical(x):
        return x['document_tone']['tone_categories'][1]['tones'][0]['score']

    @staticmethod
    def get_Confident(x):
        return x['document_tone']['tone_categories'][1]['tones'][1]['score']

    @staticmethod
    def get_Tentative(x):
        return x['document_tone']['tone_categories'][1]['tones'][2]['score']

    @staticmethod
    def get_Openness(x):
        return x['document_tone']['tone_categories'][2]['tones'][0]['score']

    @staticmethod
    def get_Conscientiousness(x):
        return x['document_tone']['tone_categories'][2]['tones'][1]['score']

    @staticmethod
    def get_Extraversion(x):
        return x['document_tone']['tone_categories'][2]['tones'][2]['score']

    @staticmethod
    def get_Agreeableness(x):
        return x['document_tone']['tone_categories'][2]['tones'][3]['score']

    @staticmethod
    def get_Emotional_Range(x):
        return x['document_tone']['tone_categories'][2]['tones'][4]['score']
    
    
    @staticmethod
    def getUpsClassification(data):
        if data < 0:
            return 'Under 0'
        elif data >= 0 and data <= 20 :
            return '0-20'
        elif data >= 21 and data <= 40 :
            return '21-40'
         elif data >= 41 and data <= 60 :
            return '41-60'
         elif data >= 61 :
            return '61+'