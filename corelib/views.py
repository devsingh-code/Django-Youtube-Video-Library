from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic
from django.contrib.auth.forms import UserCreationForm
from .models import VideoLib
# Create your views here.
def home(request):
    return render(request, 'corelib\home.html')

class SignUp(generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('home')
    template_name = 'registration/signup.html'

# def create_videolib(request):
    # if request.method == 'POST':
    #     #get form data
    #     # validate form data
    #     # create hall
    #     #save hall
    # else:
    #     # create a form for a hall
    #     # return template

class CreateVideoLib(generic.CreateView):
    model = VideoLib
    fields = ['title']
    template_name = 'corelib/create_videolib.html'
    success_url=reverse_lazy('home')


