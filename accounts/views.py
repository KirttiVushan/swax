from django.views.generic import CreateView
from django.urls import reverse_lazy
from . import forms
# Create your views here.


class SignIn(CreateView):
    form_class = forms.CreateUserForm
    success_url=reverse_lazy('login',current_app='accounts')
    template_name='accounts/signin.html'


    def register_user():
        pass

    def register_social_id():
        pass


