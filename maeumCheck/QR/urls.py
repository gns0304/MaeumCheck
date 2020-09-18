from django.urls import path, re_path

import QR.views

urlpatterns = [
    path('login', QR.views.login, name="login"),
    path('', QR.views.index, name="index"),
    path('error', QR.views.error, name="error"),

    # 대시보드 관련
    path('dashboard', QR.views.dashboard, name="dashboard"),
    path('dashboard/place/<int:placeId>', QR.views.detailPlace, name="detailPlace"),
    path('dashboard/meeting/<int:meetingId>', QR.views.detailMeeting, name="detailMeeting"),

    # 공간 및 모임 등록관련
    path('dashboard/register/place', QR.views.registerPlace, name="registerPlace"),
    path('dashboard/register/meeting', QR.views.registerMeeting, name="registerMeeting"),
    path('dashboard/create/place', QR.views.createPlace, name="createPlace"),
    path('dashboard/create/meeting', QR.views.createMeeting, name="createMeeting"),

    # QR관련
    re_path(r'^auth/(?P<type>[0-1])/(?P<token>[a-zA-Z0-9]{50})/$', QR.views.authQR, name="authQR"),
    re_path(r'auth/(?P<type>[0-1])/refresh', QR.views.refreshQR, name="refreshQR"),
    re_path(r'^auth/(?P<type>[0-1])/(?P<token>[a-zA-Z0-9]{50})/code$', QR.views.generateQR, name="generateQR"),
    re_path(r'auth/success', QR.views.successQR, name="successQR"),

]