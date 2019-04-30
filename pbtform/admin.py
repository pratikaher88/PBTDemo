# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from pbtform.models import (ContactEmail, IssueReport, BarrierReport, InformationRequest,
                            IssueComments, IssueExtraData, IssueStatus, IssueState)

# Register your models here.
class ContactEmailAdmin(admin.ModelAdmin):
    pass

class IssueReportAdmin(admin.ModelAdmin):
    pass

class BarrierReportAdmin(admin.ModelAdmin):
    pass

class InformationRequestAdmin(admin.ModelAdmin):
    pass

class IssueCommentsAdmin(admin.ModelAdmin):
    pass

class IssueExtraDataAdmin(admin.ModelAdmin):
    pass

class IssueStatusAdmin(admin.ModelAdmin):
    pass

class IssueStateAdmin(admin.ModelAdmin):
    pass

admin.site.register(ContactEmail, ContactEmailAdmin)
admin.site.register(IssueReport, IssueReportAdmin)
admin.site.register(BarrierReport, BarrierReportAdmin)
admin.site.register(InformationRequest, InformationRequestAdmin)
admin.site.register(IssueComments, IssueCommentsAdmin)
admin.site.register(IssueExtraData, IssueExtraDataAdmin)
admin.site.register(IssueStatus, IssueStatusAdmin)
admin.site.register(IssueState, IssueStateAdmin)
