from django import forms
from .models import (BarrierReport, InformationRequest, IssueReport, ContactEmail)
from pbtform import helper

class IssueForm(forms.ModelForm):
    webpage_reported = forms.URLField(required=False)
    class Meta:
        model = IssueReport
        fields = ('webpage_reported',)

    def save(self, request=None, commit=True):
        m = super(IssueForm, self).save(commit=False)
        # do custom stuff
        extra_data = request.POST
        if commit:
            m.save()
        if 'information_request' in extra_data:
            info_description = extra_data['information_description']
            new_info = InformationRequest()
            new_info.format_requested = info_description
            new_info.issue_number = m
            new_info.save()

        bar_rep = BarrierReport()
        bar_rep.what_went_wrong = extra_data['description']
        bar_rep.issue_number = m
        if 'automatic_information' in extra_data:
            bar_rep.automatic_information_included = True
            bar_rep.save()
            helper.storeAutomaticCollectedData(request, bar_rep)
        else:
            bar_rep.save()
        return m

class ReportForm(forms.ModelForm):
    class Meta:
        model = BarrierReport
        fields = ('what_went_wrong',
                  'automatic_information_included',
                  'user_survey_included',
                  'issue_level')
        widgets = {
          'what_went_wrong': forms.Textarea(attrs={'rows':2, 'title': 'Please describe:\n - what is inaccessible\n - how the barrier makes the content inaccessible'}),
          'issue_level' : forms.HiddenInput()
        }

    def save(self, reported_site, commit=True):
        m = super(ReportForm, self).save(commit=False)
        # do custom stuff
        new_issue = IssueReport.objects.create(webpage_reported=reported_site)
        m.issue_number = new_issue
        if commit:
            m.save()
        return m

class RequestForm(forms.ModelForm):
    class Meta:
        model = InformationRequest
        fields = ('requested', 'format_requested')
        widgets = {
          'requested': forms.Textarea(attrs={'rows':1, 'title':'Please indicate the piece of information on the website that is inaccessible. For example a link to a document or video will be helpful.'}),
          'format_requested': forms.Textarea(attrs={'rows':2, 'title':'Please describe how we can make the information accessible for you.'}),
        }

    def save(self, reported_site, commit=True):
        m = super(RequestForm, self).save(commit=False)
        # do custom stuff
        new_issue = IssueReport.objects.create(webpage_reported=reported_site)
        m.issue_number = new_issue
        if commit:
            m.save()
        return m

class AddEmailForm(forms.ModelForm):
    class Meta:
        model = ContactEmail
        fields = ('email',)
        widgets = {
          'email': forms.EmailInput(attrs={'title': 'Enter your email here if you want to recive updates about your barrier report'})
        }

    def save(self, commit=True):
        m = super(AddEmailForm, self).save(commit=False)
        # do custom stuff
        try:
            go = ContactEmail.objects.get(email=m.email)
        except ContactEmail.DoesNotExist:
            go = None
        if commit and not go:
            m.save()
            go = m
        return go
