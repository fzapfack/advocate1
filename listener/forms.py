from django import forms
from .models import Tweet
from registration.forms import RegistrationFormUniqueEmail
from .models import Profile


class ProfileForm(RegistrationFormUniqueEmail):
    code = forms.CharField(max_length=20)

    def clean_code(self):
        code_entered = self.cleaned_data.get('code')
        if code_entered not in Profile.CODES.values():
            raise forms.ValidationError("Ce code est incorrect")
        return code_entered


class TweetForm(forms.ModelForm):

    class Meta:
        model = Tweet
        fields = ['sentiment_label']
        labels = {
            'sentiment_label': "D'après vous quel est le sentiment",
        }

    def clean_sentiment_label(self):
        sent = self.cleaned_data.get('sentiment_label')
        if sent == Tweet.SENTIMENTS['UNKNOWN']:
            raise forms.ValidationError("Si tu ne sais pas qui donc saura :p")
        return sent
