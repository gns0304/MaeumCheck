from django.urls import path
import QR.views

urlpatterns = [
    path('login', QR.views.login, name="login"),
    path('test', QR.views.index, name = "index")
]