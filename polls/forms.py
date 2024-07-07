from django import forms


from .models import Comment

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text', 'name', 'email']

#class UploadPoll(forms.Form):
#    new_poll = forms.FrileField()
