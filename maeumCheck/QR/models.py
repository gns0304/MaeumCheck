from django.db import models
from model_utils.managers import InheritanceManager
from django.conf import settings


# Space Models


class Space(models.Model):
    name = models.CharField(max_length = 64)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    created_at = models.DateTimeField(auto_now_add=True)
    postcode = models.CharField(max_length=5, null=False, blank=False)
    address = models.CharField(max_length=100, null=False, blank=False)
    recentQRToken = models.CharField(max_length=settings.TOKEN_LENGTH, null=True, blank=True)
    tokenRegistered_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        abstract = True


class Place(Space):
    maxPeople = models.IntegerField(null=False, blank=False)
    nowPeople = models.IntegerField(null=False, blank=False)
    congestion = models.IntegerField(null=False, blank=False)



class Meeting(Space):
    expired_at = models.DateField()



# Randomized QR Address Models


class QRToken(models.Model):
    generated_at = models.DateTimeField(auto_now_add=True)
    expired_at = models.DateField()
    token = models.CharField(max_length=settings.TOKEN_LENGTH)

    class Meta:
        abstract = True


class PlaceQRToken(QRToken):
    target = models.ForeignKey(Place, on_delete=models.PROTECT)


class MeetingQRToken(QRToken):
    target = models.ForeignKey(Meeting, on_delete=models.PROTECT)


# Visit Record Models


class Record(models.Model):
    visitor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    visited_at = models.DateTimeField(auto_now_add=True)
    objects = InheritanceManager()

class PlaceRecord(Record):
    Token = models.ForeignKey(PlaceQRToken, on_delete=models.CASCADE)


class MeetingRecord(Record):
    Token = models.ForeignKey(MeetingQRToken, on_delete=models.CASCADE)