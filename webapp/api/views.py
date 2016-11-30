from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

def index(req):
    res = '''You\'ve  reached the API. Congrats!
             This is where we would do our classifier calculation and just return the answer for the website to display.
             Super simple, huh?'''
    return HttpResponse(content=res, status=200)