from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
import json

# Create your views here.

def index(req):
    res = '''You\'ve  reached the API. Congrats!
             This is where we would do our classifier calculation and just return the answer for the website to display.
             Super simple, huh?'''
    return HttpResponse(content=res, status=200)

@require_POST
@csrf_exempt
def analyze(req):
    res = {}
    res['comment'] = req.POST['comment']
    res['subreddit'] = req.POST['subreddit']
    res['datetime'] = req.POST['datetime']

    '''
    This is where we will analyze the posted data.
    We will run it through our trained classifier and return our analysis.
    '''

    return HttpResponse(json.dumps(res), content_type="application/json")