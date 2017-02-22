from registration.backends.default.views import RegistrationView
from .forms import ProfileForm
from .models import Profile


class MyRegistrationView(RegistrationView):

    form_class = ProfileForm

    def register(self, form_class):
        new_user = super(MyRegistrationView, self).register(form_class)
        code = form_class.cleaned_data['code']
        if code == Profile.CODES['L2L']:
            staff = Profile.STAFF['L2L']
        else:
            staff = Profile.STAFF['OTHER']
        new_profile = Profile.objects.create(user=new_user, partner_code=code, staff=staff)
        new_profile.save()
        return new_user
