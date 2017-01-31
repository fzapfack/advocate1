from django import forms
from .models import Tweet

class TweetForm(forms.ModelForm):

    class Meta:
        model = Tweet
        fields = ['sentiment_label']


    def clean_sentiment_label(self):
        sent = self.cleaned_data.get('sentiment_label')
        if sent==Tweet.SENTIMENTS['UNKNOWN']:
            raise forms.ValidationError("Si tu ne sais pas qui donc saura :p")
        return sent



