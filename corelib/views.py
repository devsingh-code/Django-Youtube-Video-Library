from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import generic
from django.contrib.auth.forms import UserCreationForm
from .models import VideoLib, Video
from django.contrib.auth import authenticate, login
from .forms import VideoForm, SearchForm
from django.http import Http404, JsonResponse
from  django.forms.utils import ErrorList
from django.conf import settings
from django.contrib.auth.decorators import  login_required
from django.contrib.auth.mixins import LoginRequiredMixin
import urllib, requests



def home(request):
    recent_videolibs = VideoLib.objects.all().order_by('-id')[:3]
    popular_videolibs = [VideoLib.objects.get(pk=1),VideoLib.objects.get(pk=2)]
    return render(request, 'corelib/home.html',{'recent_videolibs':recent_videolibs,'popular_videolibs':popular_videolibs})

@login_required
def dashboard(request):
    videolibs = VideoLib.objects.filter(user=request.user)

    return render(request,'corelib/dashboard.html',{'videolibs':videolibs})

@login_required
def add_video(request, pk):
    form = VideoForm()
    search_form = SearchForm()
    videolib= VideoLib.objects.get(pk=pk)

    if not videolib.user == request.user:
        raise Http404

    if request.method == 'POST':

        form = VideoForm(request.POST)
        if form.is_valid():
            video= Video()
            video.videolib= videolib
            video.url= form.cleaned_data['url']
            parsed_url = urllib.parse.urlparse(video.url)
            video_id = urllib.parse.parse_qs(parsed_url.query).get('v')
            if video_id:
                 
                video.youtube_id= video_id[0]
                response = requests.get(f'https://www.googleapis.com/youtube/v3/videos?part=snippet&id={ video_id[0] }&key={settings.YOUTUBE_API_KEY}')
                json = response.json()
                
                title = json['items'][0]['snippet']['title']
                
                video.title= title 
                video.save()
                return redirect('detail_videolib',pk)
            else:
                errors = form._errors.setdefault('url', ErrorList())
                errors.append('Needs to be a Youtube URL')

    return render(request, 'corelib/add_video.html',{'form':form, 'search_form':search_form, 'videolib':videolib})

@login_required
def video_search(request):
    search_form = SearchForm(request.GET)
    if search_form.is_valid():
        encoded_search_term = urllib.parse.quote(search_form.cleaned_data['search_term'])
        response = requests.get(f'https://www.googleapis.com/youtube/v3/search?part=snippet&maxResults=6&q={encoded_search_term}&key={settings.YOUTUBE_API_KEY}')
        # HTTP/1.1

        return JsonResponse(response.json())
    return JsonResponse({'error':'Not able to validate form'})

class SignUp( generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('dashboard')
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
class CreateVideoLib(LoginRequiredMixin,generic.CreateView):
    model = VideoLib
    fields = ['title']
    template_name = 'corelib/create_videolib.html'
    success_url=reverse_lazy('dashboard')
    
    def form_valid(self,form):
        form.instance.user = self.request.user
        super(CreateVideoLib,self).form_valid(form)
        return redirect('dashboard')

class DetailVideoLib(generic.DetailView):
    model = VideoLib
    template_name = 'corelib/detail_videolib.html'

class UpdateVideoLib(LoginRequiredMixin,generic.UpdateView):
    model = VideoLib
    template_name = 'corelib/update_videolib.html'
    fields = ['title']
    success_url = reverse_lazy('dashboard')

    def get_object(self):
        videolib = super(DeleteVideo, self).get_object()
        if not videolib.user == self.request.user:
            raise Http404
        return video


class DeleteVideoLib(LoginRequiredMixin,generic.DeleteView):
    model = VideoLib
    template_name = 'corelib/delete_videolib.html'
    success_url = reverse_lazy('dashboard')


class DeleteVideo(LoginRequiredMixin,generic.DeleteView):
    model = Video
    template_name = 'corelib/delete_video.html'
    success_url = reverse_lazy('dashboard')

    def get_object(self):
        video = super(DeleteVideo, self).get_object()
        if not video.videolib.user == self.request.user:
            raise Http404
        return video