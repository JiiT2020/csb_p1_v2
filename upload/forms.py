from django import forms


#from .models import Comment

class UploadPoll(forms.Form):
    new_poll = forms.FileField()
