from django.test import TestCase
from django.urls import reverse, resolve
from django.contrib.auth.models import User
from rest_framework import status
from ..views import CommentListView
from rest_framework.test import APIRequestFactory
from rest_framework.test import force_authenticate
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient


class TestCommentsListView(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.user = User.objects.create(username='testuser')
        self.user.set_password('123456')
        self.user.save()
        self.view = CommentListView.as_view()

        token = Token.objects.get(user__username='testuser')
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        self.data = {'name': 'thallison', 'icon_perfil': 'null', 'category': 'Palestra', 'comment': 'Legal'}

    def test_comments_view_success_status_code(self):
        url = reverse('api:comments')
        request = self.factory.get(url)
        force_authenticate(request, user=self.user)
        response = self.view(request)
        self.assertEquals(response.status_code, status.HTTP_200_OK)

    def test_comments_view_failure_status_code(self):
        url = reverse('api:comments')
        request = self.factory.get(url)
        response = self.view(request)
        self.assertEquals(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_comments_url_resolves_view(self):
        view = resolve('/v1/comments/')
        self.assertEquals(view.func.view_class, CommentListView)

    def test_comments_post_success_status_code(self):
        url = reverse('api:comments')
        request = self.client.post(url, self.data)
        self.assertEqual(request.status_code, status.HTTP_201_CREATED)

    def test_comments_post_failure_status_code(self):
        url = reverse('api:comments')
        request = self.client.post(url)
        self.assertEqual(request.status_code, status.HTTP_400_BAD_REQUEST)
