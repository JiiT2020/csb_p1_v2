import datetime
from django.db import models
from django.utils import timezone
#from django_bleach.models import BleachField


class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published', default=timezone.now)
    def __str__(self):
        return self.question_text
    def was_published_recently(self):
        return self.pub_date >= timezone.now() - datetime.timedelta(days=1)


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)
    def __str__(self):
        return self.choice_text


class Comment(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    text = models.TextField()   # here (together with comment_thank_you.html) is a vulnerability for XSS-injection
    # text = BleachField()          # this fix bleaches (sanitizes) end-user's input before it is taken to the database
    name = models.CharField(max_length=30, blank=True, null=True)
    email = models.EmailField(blank=False, null=True)  # blank=False => email is mandated; it is representing "sensitive information" in this exercise)
    created_at = models.DateTimeField(auto_now_add=True)
    url = models.CharField(max_length=100, blank=True, null=True)

    