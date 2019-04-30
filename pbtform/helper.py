# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import urllib
# from urllib import parse as urlparse
from six.moves.urllib.parse import urlparse
from urllib.request import urlopen
from pbtform.models import (IssueReport, ContactEmail, BarrierReport, IssueExtraData, BarrierAutoTest)
from pbtdemo import settings
from threading import Thread
import requests, json, re

demo_paths = [
  '/tingtun/',
  '/government-se/',
  '/government-no/'
]

url_regex = re.compile(
        r'^(?:http|ftp)s?://' # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|' #domain...
        r'localhost|' #localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})' # ...or ip
        r'(?::\d+)?' # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)

def getDomain(urlString):
    # parsed_uri = urllib.request(urlString)
    response = urlparse(urlString)
    # print("Parsed ",parsed_uri)
    return response

def setReferer(request):
    referer = request.META.get('HTTP_REFERER', '')
    if referer and (not getDomain(referer).netloc in settings.ALLOWED_HOSTS or getDomain(referer).path in demo_paths):
        request.session['report_site'] = request.META.get('HTTP_REFERER', '')
    else:
        print('No referer url')

def getReferer(request):
    referer = request.META.get('HTTP_REFERER', '')
    if referer and not getDomain(referer).netloc in settings.ALLOWED_HOSTS:
        setReferer(request)
        return referer
    elif referer and getDomain(referer).path in demo_paths:
        setReferer(request)
        return referer
    return request.session['report_site']

def storeAutomaticCollectedData(request, barrier):
    newExtra = IssueExtraData()
    newExtra.barrier = barrier
    newExtra.http_user_agent = request.META['HTTP_USER_AGENT']
    newExtra.http_languages = request.META['HTTP_ACCEPT_LANGUAGE']
    newExtra.http_accept = request.META['HTTP_ACCEPT']
    newExtra.http_accept_encoding = request.META['HTTP_ACCEPT_ENCODING']
    newExtra.save()

def addSessionContext(request, context):
    if 'font_family' in request.session:
        context['font_family'] = request.session["font_family"]
    return context

def getParamData(request, context):
    context['url_params'] = ''
    context['style'] = request.GET.get('style', '')
    if context['style']:
        context['url_params'] = 'style=' + context['style']
    #if context['url_params']:
     #   context['url_params'] = '?' + context['url_params']
    return context

def runTesting(issue):
    page = issue.webpage_reported
    if not re.match(url_regex, page):
        print('Not valid url: ', page)
        return
    print(page)
    response = requests.get('http://checkers.eiii.eu/export-jsonld/pagecheck2.0/?url='+page)
    json_data = json.loads(response.text)
    try:
        new_auto_test = BarrierAutoTest()
        new_auto_test.barrier = issue.barrier_report
        new_auto_test.url_to_report = 'http://checkers.wtkollen.se/en/pagecheck2.0/?uuid=' + json_data['uid']
        new_auto_test.score_given = float(json_data['score-sc']) * 100
        new_auto_test.save()
    except:
        print(json_data ['error'])
    return

def runAutomaticTestingOnPage(issue):
    if not issue:
        return
    t = Thread(target=runTesting, args=([issue]))
    t.start()
    return
