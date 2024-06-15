from django.db.models import Q
from .models import Video
from django.views.generic import ListView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import logout
from django.views import View

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
        return context

