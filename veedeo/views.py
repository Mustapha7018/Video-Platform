from django.db.models import Q
from .models import Video
from accounts.models import CustomUser
from django.contrib.auth import logout
from django.urls import reverse_lazy
from .forms import VideoForm
from django.views import View
from django.http import JsonResponse, HttpResponseRedirect

from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)
from django.contrib.auth.mixins import (
    LoginRequiredMixin,
    UserPassesTestMixin,
)


''' ALL VIDEOS LIST VIEW '''
class VideoListView(ListView):
    model = Video
    template_name = 'video_pages/all_videos.html'
    context_object_name = 'videos'
    paginate_by = 6

    def get_queryset(self):
        query = self.request.GET.get('q')
        if query:
            return Video.objects.filter(Q(title__icontains=query) | Q(description__icontains=query)).order_by('-uploaded_at')
        return Video.objects.order_by('-uploaded_at')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_admin'] = self.request.user.is_staff  
        return context


''' VIDEO DETAIL VIEW'''
class VideoDetailView(DetailView):
    model = Video
    template_name = 'video_pages/video_detail.html'
    context_object_name = 'video'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        video = self.get_object()
        context['previous_video'] = Video.objects.filter(id__lt=video.id).order_by('-id').first()
        context['next_video'] = Video.objects.filter(id__gt=video.id).order_by('id').first()
        context['is_admin'] = self.request.user.is_staff
        return context




''' VIDEO UPLOAD VIEW '''
class VideoUploadView(LoginRequiredMixin, CreateView):
    model = Video
    form_class = VideoForm
    template_name = 'video_pages/upload.html'
    success_url = reverse_lazy('video_list')

    def form_valid(self, form):
        form.instance.uploaded_by = self.request.user
        print('Form is valid')
        return super().form_valid(form)

    def form_invalid(self, form):
        print('Form is invalid')
        print(form.errors)
        return super().form_invalid(form)


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['staff_users'] = CustomUser.objects.filter(is_staff=True)
        return context




''' VIDEO UPDATE VIEW '''
class VideoUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Video
    fields = ['title', 'description', 'video_file']

    def test_func(self):
        return self.request.user.is_staff

    def form_valid(self, form):
        self.object = form.save()
        return JsonResponse({'success': True})

    def form_invalid(self, form):
        return JsonResponse({'success': False, 'errors': form.errors})



''' VIDEO DELETE VIEW '''
class VideoDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Video
    success_url = reverse_lazy('video_list')

    def test_func(self):
        return self.request.user.is_staff

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.delete()
        return HttpResponseRedirect(self.success_url)
