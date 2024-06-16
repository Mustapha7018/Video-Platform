from django.urls import path
from .views import *

urlpatterns = [
    path('all_videos/', VideoListView.as_view(), name='video_list'),
    path('video/<int:pk>/', VideoDetailView.as_view(), name='video_detail'),
    path('video/upload/', VideoUploadView.as_view(), name='video_upload'),
    path('video/<int:pk>/edit/', VideoUpdateView.as_view(), name='video_edit'),
    path('video/<int:pk>/delete/', VideoDeleteView.as_view(), name='video_delete'),
]
