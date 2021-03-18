from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    appartment = models.ForeignKey("Appartment", on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name} {self.appartment.number}{self.appartment.building}"


class Appartment(models.Model):
    building = models.CharField(max_length=1)
    number = models.SmallIntegerField()


class Notice(models.Model):
    topic = models.CharField(max_length=64)
    author = models.ForeignKey(Profile, on_delete=models.CASCADE)
    content = models.TextField(max_length=1000)
    date = models.DateField(auto_now_add=True)


class Message(models.Model):
    topic = models.CharField(max_length=64)
    author = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="author")
    recipient = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="recipient")
    content = models.TextField(max_length=1000)
    date = models.DateField(auto_now_add=True)


class Poll(models.Model):
    name = models.CharField(max_length=64)
    description = models.TextField(max_length=1000)
    question = models.CharField(max_length=128)
    people = models.ManyToManyField(Profile, through='Vote')
    votes_for = models.IntegerField(default=0)
    votes_against = models.IntegerField(default=0)
    votes_pass = models.IntegerField(default=0)
    date = models.DateField(auto_now_add=True)


class Vote(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    chosen_option = models.CharField(max_length=16)
