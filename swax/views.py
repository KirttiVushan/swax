from django.views.generic import TemplateView

class Home(TemplateView):
    template_name= 'home.html'


class TestPage(TemplateView):
    template_name='test.html'

class ThanksPage(TemplateView):
    template_name='thanks.html'