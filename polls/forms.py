from django import forms


from .models import Comment

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text', 'name', 'email', 'url']
        labels = {
            'text': 'Your comment',
            'name': 'Name (optional)',
            'email': 'Email (mandatory, will not be shown)',
            'url': 'Homepage (optional)',
        }

#class UploadPoll(forms.Form):
#    new_poll = forms.FrileField()
