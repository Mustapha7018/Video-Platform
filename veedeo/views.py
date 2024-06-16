from django.db.models import Q
from .models import Video
from django.contrib.auth import logout
from django.urls import reverse_lazy
from .forms import VideoForm
from django.views import View
from django.http import JsonResponse
from django.views.generic import (
    ListView,
    DetailView,
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
class VideoUploadView(LoginRequiredMixin, UserPassesTestMixin, View):
    def test_func(self):
        return self.request.user.is_staff

    def post(self, request, *args, **kwargs):
        if not self.test_func():
            return JsonResponse({'success': False, 'error': 'Permission denied.'})
        
        form = VideoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return JsonResponse({'success': True})
        return JsonResponse({'success': False, 'errors': form.errors})



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
        try:
            self.object = self.get_object()
            self.object.delete()
            return JsonResponse({'success': True})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})