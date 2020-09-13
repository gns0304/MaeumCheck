from django.contrib import admin
from .models import *

# Register your models here.

admin.site.register(Place)
admin.site.register(Meeting)

admin.site.register(PlaceQRToken)
admin.site.register(MeetingQRToken)

admin.site.register(PlaceRecord)
admin.site.register(MeetingRecord)