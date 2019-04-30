# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.

class ContactEmail(models.Model):
    email = models.EmailField()

    def __unicode__(self):
        return self.email

class IssueState(models.Model):
    state = models.TextField(blank=False, null=False)

    def __unicode__(self):
        return self.state

class IssueReport(models.Model):
    email_list = models.ManyToManyField(ContactEmail, blank=True)
    closed = models.BooleanField(default=False)
    webpage_reported = models.URLField()
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    date_closed = models.DateTimeField(null=True, blank=True)

    def __unicode__(self):
        return str(self.id) + ' : ' + self.webpage_reported

class BarrierReport(models.Model):
    issue_level = models.IntegerField(default=0)
    what_they_did = models.TextField(blank=True, null=False, default='')
    what_went_wrong = models.TextField(blank=True, null=False, default='')
    automatic_information_included = models.BooleanField(default=False)
    user_survey_included = models.BooleanField(default=False)
    issue_number = models.OneToOneField(IssueReport, on_delete=models.CASCADE, related_name="barrier_report")
    issue_fix = models.URLField(null=True, blank=True)

    def __unicode__(self):
        return str(self.issue_number.id) + ':' + self.what_went_wrong

class InformationRequest(models.Model):
    requested = models.TextField()
    format_requested = models.TextField()
    issue_number = models.OneToOneField(IssueReport, on_delete=models.CASCADE, related_name="information_request")

    def __unicode__(self):
        return str(self.issue_number.id) + ':' + self.requested

class IssueComments(models.Model):
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)
    text = models.TextField(blank=False, null=False)
    related_issue = models.ForeignKey(IssueReport, on_delete=models.CASCADE, related_name="related_comments")

    def __unicode__(self):
        return str(self.related_issue.id) + ':' + self.text

class IssueExtraData(models.Model):
    http_user_agent = models.TextField(blank=True, null=False, default='')
    http_languages = models.TextField(blank=True, null=False, default='')
    http_accept = models.TextField(blank=True, null=False, default='')
    http_accept_encoding = models.TextField(blank=True, null=False, default='')
    barrier = models.OneToOneField(BarrierReport, on_delete=models.CASCADE, related_name="extra_data")

    def __unicode__(self):
        return str(self.barrier.issue_number.id)

class IssueStatus(models.Model):
    state = models.ForeignKey(IssueState, blank=False, null=False, related_name="issue", on_delete=models.CASCADE)
    comment = models.TextField(blank=False, null=False)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    barrier = models.OneToOneField(IssueReport, on_delete=models.CASCADE, related_name="status")

    class Meta:
        verbose_name_plural = 'IssueStatus'

    def __unicode__(self):
        return str(self.barrier.id) + ':' + self.state.state

class BarrierAutoTest(models.Model):
    barrier = models.OneToOneField(BarrierReport, on_delete=models.CASCADE, related_name="auto_test")
    url_to_report = models.URLField(blank=True, null=True)
    score_given = models.FloatField(blank=True, null=True)
