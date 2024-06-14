from django.urls import path
from .views import *

urlpatterns = [
    path('all_videos/', VideoListView.as_view(), name='video_list'),
    path('video/<int:pk>/', VideoDetailView.as_view(), name='video_detail'),
]
