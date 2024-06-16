from django.test import TestCase, Client
from django.urls import reverse
from .models import Video
from accounts.models import CustomUser

class VideoViewsTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = CustomUser.objects.create_user(email='testuser@example.com', password='testpass')
        self.admin_user = CustomUser.objects.create_superuser(email='adminuser@example.com', password='adminpass')
        self.video1 = Video.objects.create(
            title='Test Video 1',
            description='Test Description 1',
            video_file='video1.mp4',
            uploaded_by=self.admin_user
        )
        self.video2 = Video.objects.create(
            title='Test Video 2',
            description='Test Description 2',
            video_file='video2.mp4',
            uploaded_by=self.admin_user
        )

    def test_video_list_view(self):
        response = self.client.get(reverse('video_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'video_pages/all_videos.html')
        self.assertContains(response, self.video1.title)
        self.assertContains(response, self.video2.title)

    def test_video_detail_view(self):
        response = self.client.get(reverse('video_detail', args=[self.video1.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'video_pages/video_detail.html')
        self.assertContains(response, self.video1.title)
        self.assertContains(response, self.video1.description)


