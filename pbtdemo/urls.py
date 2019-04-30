"""pbtdemo URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from pbtform import views as formviwes
from rest_framework.routers import DefaultRouter
from restfull_api import views as restviews
from django.views.generic.base import TemplateView

router = DefaultRouter()
router.register(r'BarrierReport', restviews.BarrierReport)
router.register(r'InformationRequest', restviews.InformationRequest)
router.register(r'IssueReport', restviews.IssueReport)
router.register(r'BarrierStatus', restviews.BarrierStatus)

urlpatterns = [

    url(r'^songs/', formviwes.BarrierReport.as_view(), name="songs-all"),
    # Demo pages
    url(r'^tingtun/$', TemplateView.as_view(template_name='demo_pages/tingtun.html')),
    url(r'^government-se/$', TemplateView.as_view(template_name='demo_pages/government-se.html')),
    url(r'^government-no/$', TemplateView.as_view(template_name='demo_pages/goverment-no-_en_version.html')),

    # Website
    url(r'^admin/', admin.site.urls),
    url(r'^finished/(?P<issue_number>[0-9]+)/$', formviwes.form_finish, name="finish"),
    url(r'^report/$', formviwes.form_report),
    url(r'^report_issue/$', formviwes.form_issue),
    url(r'^request/$', formviwes.form_request),
    url(r'^add-email/(?P<issue_number>[0-9]+)/$', formviwes.form_add_email, name="add-email"),
    url(r'^enforcement_procedure/$', formviwes.enforcement_procedure),
    url(r'^accessibility_statement/$', formviwes.accessibility_statement),
    url(r'^privacy_statement/$', formviwes.privacy_statement),
    url(r'^find_out_more_short/$', formviwes.find_out_more_short),
    url(r'^find_out_more/$', formviwes.find_out_more),
    url(r'^api/', include(router.urls)),
    url(r'^issue_presentation/(?P<issue_number>[0-9]+)/$', formviwes.issue_presentation),
    url(r'^issues_list/$', formviwes.issues_list),
    url(r'^admin_issues/$', formviwes.admin_issues),
    url(r'^start_report/$', formviwes.start, name='start-report'),
    url(r'^project_summary/$', formviwes.project_summary, name='project-summary'),
    url(r'^$', formviwes.home, name='home'),
]
