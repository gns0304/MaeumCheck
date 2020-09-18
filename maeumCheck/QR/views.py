from django.shortcuts import render, redirect, get_object_or_404, reverse
from django.contrib.auth.decorators import login_required
from .models import *
from .generator import *
from django.views.decorators.http import require_POST
import json
from django.http import JsonResponse

# Create your views here.

def login(request):
    return render(request, 'login.html')

def index(request):
    return render(request, 'index.html')

def error(request):
    return render(request, 'error.html')

@login_required
def registerPlace(request):
    return render(request, 'registerPlace.html')

@login_required
def registerMeeting(request):
    return render(request, 'registerMeeting.html')

@login_required
def createPlace(request):
    if(request.method == 'POST'):
        place = Place()
        address = request.POST.get('roadAddress') + ', ' + request.POST.get('detailAddress') + request.POST.get('extraAddress')
        place.name = request.POST.get('name')
        place.owner = request.user
        place.postcode = request.POST.get('postcode')
        place.address = address
        place.maxPeople = request.POST.get('quantity')
        place.nowPeople = 0
        place.congestion = 0
        place.save()
        registerToken(0, place.id, settings.RETENTION_PERIOD)
    return redirect('index')

@login_required
def createMeeting(request):
    if(request.method == 'POST'):
        meeting = Meeting()
        address = request.POST.get('roadAddress') + ', ' + request.POST.get('detailAddress') + request.POST.get('extraAddress')
        meeting.name = request.POST.get('name')
        meeting.owner = request.user
        meeting.postcode = request.POST.get('postcode')
        meeting.address = address
        meeting.expired_at = request.POST.get('expiredDate')
        meeting.save()
        registerToken(1, meeting.id, settings.RETENTION_PERIOD)
    return redirect('index')

# Auth

@login_required
def generateQR(request, type, token):
    return generateQRimage("{0}/auth/{1}/{2}/code".format(settings.DEFAULT_DOMAIN, type, token))

def authQR(request, type, token):
    if type == 0:
        records = PlaceRecord.objects.all().order_by('-id')
    elif type == 1:
        records = MeetingRecord.objects.all().order_by('-id')

    for record in records:
        if get_object_or_404(PlaceQRToken, pk=record.target_id).token == token:
            return render(request, 'error.html', {"errorCode": "이미 사용된 토큰입니다."})

    if type == 0:
        targetRecord = PlaceRecord()
        targetQRTokenId = get_object_or_404(PlaceQRToken, token=token).id
    elif type == 1:
        targetRecord = MeetingRecord()
        targetQRTokenId = get_object_or_404(MeetingQRToken, token=token).id

    targetRecord.visitor = request.user
    targetRecord.placeToken = PlaceQRToken(pk= targetQRTokenId)
    targetRecord.save()
    name = get_object_or_404(PlaceQRToken, token=token).target.name
    id = get_object_or_404(PlaceQRToken, token=token).target.id
    auth_at = targetRecord.visited_at
    registerToken(0,id, settings.RETENTION_PERIOD)
    return render(request, 'authSuccess.html', {"name": name, "auth_at": auth_at})

@login_required
def refreshQR(request, type):
    type = int(type)
    token_requested = request.POST.get('token')
    targetId = request.POST.get('id')

    if type == 0:
        target = get_object_or_404(Place, pk=targetId)
    elif type == 1:
        target = get_object_or_404(Meeting, pk=targetId)


    token_now = target.recentQRToken

    if token_requested == token_now:
        response = {"type": 0}
        return JsonResponse(response)
    else:
        response = {"type": 1, 'codeQR': "{0}/auth/{1}/{2}/code".format(settings.DEFAULT_DOMAIN, type, token_now), 'token':token_now}
        return JsonResponse(response)


@login_required
def generatePlaceQR(request, token):
    return generateQRimage(settings.DEFAULT_DOMAIN+'/auth/place/'+token+'/code')

@login_required
def generateMeetingQR(request, token):
    return generateQRimage(settings.DEFAULT_DOMAIN+'/auth/meeting/'+token+'/code')

@login_required
def authPlaceQR(request, token):
    placesRecords = PlaceRecord.objects.all().order_by('-id')
    for placesRecord in placesRecords:
        if get_object_or_404(PlaceQRToken, pk=placesRecord.target_id).token == token:
            return render(request, 'error.html', {"errorCode": "이미 사용된 토큰입니다."})
    placesRecord = PlaceRecord()
    PlaceQRTokenId = get_object_or_404(PlaceQRToken, token=token).id
    placesRecord.visitor = request.user
    placesRecord.placeToken = PlaceQRToken(pk=PlaceQRTokenId)
    placesRecord.save()
    name = get_object_or_404(PlaceQRToken, token=token).target.name
    id = get_object_or_404(PlaceQRToken, token=token).target.id
    auth_at = placesRecord.visited_at
    registerToken(0,id, settings.RETENTION_PERIOD)
    return render(request, 'authSuccess.html', {"name": name, "auth_at": auth_at})

@login_required
def authMeetingQR(request, token):
    meetingRecords = MeetingRecord.objects.all().order_by('-id')
    for meetingRecord in meetingRecords:
        if get_object_or_404(MeetingQRToken, pk=meetingRecord.meetingToken_id).token == token:
            return render(request, 'error.html', {"errorCode": "이미 사용된 토큰입니다."})
    meetingRecord = MeetingRecord()
    MeetingQRTokenId = get_object_or_404(MeetingQRToken, token=token).id
    meetingRecord.visitor = request.user
    meetingRecord.meetingToken = MeetingQRToken(pk=MeetingQRTokenId)
    meetingRecord.save()
    name = get_object_or_404(MeetingQRToken, token=token).target.name
    id = get_object_or_404(MeetingQRToken, token=token).target.id
    auth_at = meetingRecord.visited_at
    registerToken(1,id, settings.RETENTION_PERIOD)
    return render(request, 'authSuccess.html', {"name": name, "auth_at": auth_at})


@login_required
def dashboard(request):
    places = Place.objects.filter(owner=request.user).order_by('-id')[:3]
    meetings = Meeting.objects.filter(owner=request.user).order_by('-id')[:3]
    return render(request, 'dashboard.html', {'places': places, 'meetings': meetings})


@login_required
def refreshPlaceQR(request):
    token_requested = request.POST.get('token')
    placeId = request.POST.get('id')
    place = get_object_or_404(Place, pk=placeId)
    token_now = place.recentQRToken
    if token_requested == token_now:
        response = {"type": 0}
        return JsonResponse(response)
    else:
        codeQR = settings.DEFAULT_DOMAIN + '/auth/place/' + token_now + '/code'
        response = {"type": 1, 'codeQR': codeQR, 'token':token_now}
        return JsonResponse(response)

@login_required
def refreshMeetingQR(request):
    token_requested = request.POST.get('token')
    meetingId = request.POST.get('id')
    meeting = get_object_or_404(Meeting, pk=meetingId)
    token_now = meeting.recentQRToken
    if token_requested == token_now:
        response = {"type": 0}
        return JsonResponse(response)
    else:
        codeQR = settings.DEFAULT_DOMAIN + '/auth/meeting/' + token_now + '/code'
        response = {"type": 1, 'codeQR': codeQR, 'token':token_now}
        return JsonResponse(response)


@login_required
def detailPlace(request, placeId):
    place = get_object_or_404(Place, pk=placeId)
    token = place.recentQRToken
    codeQR = settings.DEFAULT_DOMAIN + '/auth/0/' + token +'/code'
    if place.owner == request.user:
        return render(request, 'detailPlace.html', {'place': place, 'codeQR': codeQR, 'token': token})
    else:
        return render(request, 'error.html', {"errorCode": "권한이 없습니다."})

@login_required
def detailMeeting(request, meetingId):
    meeting = get_object_or_404(Meeting, pk=meetingId)
    token = meeting.recentQRToken
    codeQR = settings.DEFAULT_DOMAIN + '/auth/1/' + token + '/code'
    if meeting.owner == request.user:
        return render(request, 'detailMeeting.html', {'meeting': meeting, 'codeQR': codeQR, 'token': token})
    else:
        return render(request, 'error.html', {"errorCode": "권한이 없습니다."})



