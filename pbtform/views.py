# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from rest_framework import generics
from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import HttpResponseRedirect
from pbtform import forms as pbtforms
from pbtform.models import (IssueReport, ContactEmail, BarrierReport, IssueExtraData)
from django.core.paginator import Paginator
from pbtform import helper
from django.core.mail import send_mail, EmailMessage
from django.template.loader import render_to_string
from pbtform import models
from pbtform import serializers
from rest_framework import permissions

# Create your views here.

def form_issue(request):

    form = pbtforms.IssueForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            model = form.save(request)
            context = helper.getParamData(request, {})
            url_ = reverse('finish', kwargs={'issue_number':model.id})
            helper.runAutomaticTestingOnPage(model)
            return HttpResponseRedirect(url_ + '?' + context['url_params'])
    else:
        referer = helper.getReferer(request)
        form = pbtforms.IssueForm(initial={'webpage_reported': referer})
    context = {'form': form}
    request.session["font_family"] = request.GET.get('font_family', None)
    context = helper.getParamData(request, context)
    return render(request, 'form_issue.html', context)

def form_report(request):
    level = request.GET.get('level', '0')
    if request.method == 'POST':
        form = pbtforms.ReportForm(request.POST)
        if form.is_valid():
            report_site = request.session.get('report_site', '')
            model = form.save(report_site)
            if 'automatic_information_included' in request.POST and request.POST['automatic_information_included']:
                helper.storeAutomaticCollectedData(request, model)
            context = helper.getParamData(request, {})
            url_ = reverse('finish', kwargs={'issue_number':model.issue_number.id})
            #helper.runAutomaticTestingOnPage(report_site, model)
            return HttpResponseRedirect(url_ + '?' + context['url_params'])
    else:
        form = pbtforms.ReportForm(initial={'issue_level': level})
    context = {'form': form, 'level': level}
    context = helper.getParamData(request, context)
    context = helper.addSessionContext(request, context)
    return render(request, 'form_report.html', context)

def form_finish(request, issue_number=''):
    form = pbtforms.AddEmailForm(request.POST or None)
    add_email = True
    try:
        issue = IssueReport.objects.get(id = issue_number)
        if request.method == 'POST':
            if form.is_valid():
                model = form.save()
                issue.email_list.add(model)
                add_email = False
                issue_url = request.META['HTTP_HOST'] + '/issue_presentation/' + str(issue.id) + '/'
                
                subject = 'Link to your issue submitted to the Public Barrier Tracker'
                message = render_to_string('email_reg_message.html', {'website': issue.webpage_reported, 'issue_url': issue_url}) 
                to = [model.email]
                #msg = render_to_string('email_reg_message.html', {'website': issue.webpage_reported, 'issue_url': issue_url})
                #msg.content_subtype = 'html'
                msg = EmailMessage(subject, message, to=to)
                msg.content_subtype = 'html'
                msg.send()
               # send_mail('Link to your issue submitted to the Public Barrier Tracker',
                #  msg,
                 # model.email,
                  #['contact@tingtun.no'],
                  #fail_silently=False)
  
    except IssueReport.DoesNotExist:
        print ('Error')
    context = {'issue_number': issue_number, 'form': form, 'add_email': add_email}
    context = helper.getParamData(request, context)
    context = helper.addSessionContext(request, context)
    return render(request, 'form_finish.html', context)

def form_request(request):
    form = pbtforms.RequestForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            report_site = request.session.get('report_site', '')
            model = form.save(report_site)
            context = helper.getParamData(request, {})
            url_ = reverse('finish', kwargs={'issue_number':model.issue_number.id})
            return HttpResponseRedirect(url_ + '?' + context['url_params'])
    context = {'form': form}
    context = helper.getParamData(request, context)
    context = helper.addSessionContext(request, context)
    return render(request, 'form_request.html', context)

def form_add_email(request, issue_number=''):
    form = pbtforms.AddEmailForm(request.POST or None)
    try:
        issue = IssueReport.objects.get(id = issue_number)
        if request.method == 'POST':
            if form.is_valid():
                model = form.save()
                issue.email_list.add(model)
    except IssueReport.DoesNotExist:
        print ('Error')    
    context = {'form': form}
    context = helper.getParamData(request, context)
    context = helper.addSessionContext(request, context)
    return render(request, 'add_email.html', context)

def start(request):
    helper.setReferer(request)
    request.session["font_family"] = request.GET.get('font_family', None)
    context = {}
    context = helper.getParamData(request, context)
    context = helper.addSessionContext(request, context)
    return render(request, 'choice_page.html', context)

def home(request):
    context = {}
    return render(request, 'home.html', context)

def project_summary(request):
    context = {}
    return render(request, 'project_summary.html', context)

def enforcement_procedure(request):
    context = {}
    context = helper.addSessionContext(request, context)
    return render(request, 'enforcement_procedure.html', context)

def accessibility_statement(request):
    context = {}
    context = helper.addSessionContext(request, context)
    return render(request, 'accessibility_statement.html', context)

def privacy_statement(request):
    context = {}
    context = helper.addSessionContext(request, context)
    return render(request, 'privacy_statement.html', context)

def find_out_more_short(request):
    context = {}
    context = helper.getParamData(request, context)
    context = helper.addSessionContext(request, context)
    return render(request, 'find_out_more_short.html', context)

def find_out_more(request):
    context = {}
    context = helper.addSessionContext(request, context)
    return render(request, 'find_out_more.html', context)

def issues_list(request):
    all_issues = IssueReport.objects.all().order_by('-id', '-date_created')
    page = int(request.GET.get('page', 1))
    url_startwith = request.GET.get('url_startwith', None)
    url_is = request.GET.get('url_is', None)
    add_parameters = ''
    if url_is:
        add_parameters = '&url_is=' + url_is
        all_issues = all_issues.filter(webpage_reported = url_is)
    elif url_startwith:
        add_parameters = '&url_startwith=' + url_startwith
        all_issues = all_issues.filter(webpage_reported__startswith = url_startwith)

    paginator = Paginator(all_issues, 10)
    num_pages = paginator.num_pages
    try:
        issues = paginator.page(page)
    except PageNotAnInteger:
        issues = paginator.page(1)
    except EmptyPage:
        issues = paginator.page(paginator.num_pages)
    if page >= paginator.num_pages:
        next = None
    else:
        next = page + 1
    if page <= 1 or page > paginator.num_pages:
        previous = None
    else:
        previous = page - 1

    context = {'issues': issues,
               'next_page': next,
               'previous_page': previous,
               'add_parameters': add_parameters,
               'current_page': page}
    context = helper.addSessionContext(request, context)
    return render(request, 'issues_list.html', context)

def issue_presentation(request, issue_number):
    try:
        issue = IssueReport.objects.get(id=issue_number)
        parsed = helper.getDomain(issue.webpage_reported)
        domain = parsed.scheme + '://' + parsed.netloc
    except IssueReport.DoesNotExist:
        issue = None
    context = {'issue': issue,
               'domain': domain}
    context = helper.addSessionContext(request, context)
    return render(request, 'issue_presentation.html', context)

def admin_issues(request):
    all_issues = IssueReport.objects.filter(barrier_report__isnull=False).order_by('-date_created')
    page = int(request.GET.get('page', 1))
    paginator = Paginator(all_issues, 10)
    num_pages = paginator.num_pages
    try:
        issues = paginator.page(page)
    except PageNotAnInteger:
        issues = paginator.page(1)
    except EmptyPage:
        issues = paginator.page(paginator.num_pages)
    if page >= paginator.num_pages:
        next = None
    else:
        next = page + 1
    if page <= 1 or page > paginator.num_pages:
        previous = None
    else:
        previous = page - 1

    context = {'issues': issues,
               'next_page': next,
               'previous_page': previous,
               'current_page': page}
    context = helper.addSessionContext(request, context)
    return render(request, 'admin/admin_issues.html', context)


# API classes


class BarrierReport(generics.ListAPIView):

    queryset = models.BarrierReport.objects.all()
    serializer_class = serializers.BarrierReportSerializerFull
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
