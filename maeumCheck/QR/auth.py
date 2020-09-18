import string
import random
import datetime

from django.shortcuts import get_object_or_404
from django.http import HttpResponse

import os
import django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "maeumCheck.settings")
django.setup()
from QR.models import *

import qrcode



def generateToken(type):
    token = ""
    list = []

    list.extend(string.ascii_letters)
    list.extend(string.digits)

    for i in range(0, settings.TOKEN_LENGTH):
        token += str(random.choice(list))

    if type == 0:
        objects = PlaceQRToken.objects.all()
    elif type == 1:
        objects = MeetingQRToken.objects.all()

    isSame = False
    for object in objects:
        if object.token == token:
            isSame = True
            break

    if isSame == True:
        token = generateToken(type)

    return token

def registerToken(type, spaceId, day):
    if type == 0:

        placeQRToken = PlaceQRToken()
        token = generateToken(0)
        placeQRToken.token = token
        placeQRToken.target = Place(pk=spaceId)
        placeQRToken.generated_at = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        placeQRToken.expired_at = (datetime.datetime.now() + datetime.timedelta(days=day)).strftime('%Y-%m-%d')
        placeQRToken.save()

        place = get_object_or_404(Place, pk=spaceId)
        place.recentQRToken = token
        place.tokenRegistered_at = datetime.datetime.now()
        place.save()


    elif type == 1:

        meetingQRToken = MeetingQRToken()
        token = generateToken(1)
        meetingQRToken.token = token
        meetingQRToken.target = Meeting(pk=spaceId)
        meetingQRToken.generated_at = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        meetingQRToken.expired_at = (datetime.datetime.now() + datetime.timedelta(days=day)).strftime('%Y-%m-%d')
        meetingQRToken.save()

        meeting = get_object_or_404(Meeting, pk=spaceId)
        meeting.recentQRToken = token
        meeting.tokenRegistered_at = datetime.datetime.now()
        meeting.save()

def generateQRimage(url):
    img = qrcode.make(url)
    response = HttpResponse(content_type = "image/png")
    img.save(response, "png")
    return response
