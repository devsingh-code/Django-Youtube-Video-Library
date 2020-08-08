from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import generic
from django.contrib.auth.forms import UserCreationForm
from .models import VideoLib
from django.contrib.auth import authenticate, login
from .forms import VideoForm

# Create your views here.
def home(request):
    return render(request, 'corelib/home.html')

def dashboard(request):
    return render(request,'corelib/dashboard.html')

def add_video(request, pk):
    form = VideoForm()
    return render(request, 'corelib/add_video.html',{'form':form})


class SignUp(generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('home')
    template_name = 'registration/signup.html'

    def form_valid(self,form):
        view = super(SignUp,self).form_valid(form)
        username, password = form.cleaned_data.get('username'), form.cleaned_data.get('password1')
        user = authenticate(username=username, password=password)
        login(self.request, user)
        return view



# def create_videolib(request):
    # if request.method == 'POST':
    #     #get form data
    #     # validate form data
    #     # create hall
    #     #save hall
    # else:
    #     # create a form for a hall
    #     # return template

#CRUD
class CreateVideoLib(generic.CreateView):
    model = VideoLib
    fields = ['title']
    template_name = 'corelib/create_videolib.html'
    success_url=reverse_lazy('home')
    
    def form_valid(self,form):
        form.instance.user = self.request.user
        super(CreateVideoLib,self).form_valid(form)
        return redirect('dashboard')

class DetailVideoLib(generic.DetailView):
    model = VideoLib
    template_name = 'corelib/detail_videolib.html'

class UpdateVideoLib(generic.UpdateView):
    model = VideoLib
    template_name = 'corelib/update_videolib.html'
    fields = ['title']
    success_url = reverse_lazy('dashboard')

class DeleteVideoLib(generic.DeleteView):
    model = VideoLib
    template_name = 'corelib/delete_videolib.html'
    success_url = reverse_lazy('dashboard')



