from django.db import models
from model_utils.managers import InheritanceManager


# Create your models here.


# Space Models


class Space(models.Model):
    name = models.CharField(max_length = 64)
    owner = models.CharField(max_length = 64) #임시 공간 관리자 Field
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        abstract = True


class Place(Space):
    maxPeople = models.IntegerField()
    nowPeople = models.IntegerField()


class Meeting(Space):
    expired_at = models.DateField()


# Randomized QR Address Models


class QRToken(models.Model):
    generated_at = models.DateTimeField(auto_now_add=True)
    expired_at = models.DateField()
    token = models.CharField(max_length=30)

    class Meta:
        abstract = True


class PlaceQRToken(QRToken):
    place = models.ForeignKey(Place, on_delete=models.PROTECT)


class MeetingQRToken(QRToken):
    meeting = models.ForeignKey(Meeting, on_delete=models.PROTECT)


# Visit Record Models


class Record(models.Model):
    visitor = models.CharField(max_length = 64)
    email = models.EmailField()
    visited_at = models.DateTimeField(auto_now_add=True)
    objects = InheritanceManager()


class PlaceRecord(Record):
    placeToken = models.ForeignKey(PlaceQRToken, on_delete=models.PROTECT)


class MeetingRecord(Record):
    meetingToken = models.ForeignKey(MeetingQRToken, on_delete=models.PROTECT)