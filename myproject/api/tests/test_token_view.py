from django.test import TestCase, RequestFactory
from django.urls import resolve
from django.contrib.auth.models import User, AnonymousUser
from rest_framework import status
from ..views import token_request


class TestTokenView(TestCase):
    
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user('johnSnow', 'lennon@johnSnow.com', 'johnSnow')

    def test_token_url_resolves_view(self):
        view = resolve('/token/')
        self.assertEquals(view.func, token_request)

    def test_token_create_new_user(self):
        request = self.factory.get('/token/')
        request.user = self.user
        response = token_request(request)
        self.assertContains(response, 'token')

    def test_token_success_status_code(self):
        request = self.factory.get('/token/')
        request.user = self.user
        response = token_request(request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_token_failure_status_code(self):
        request = self.factory.get('/token/')
        request.user = AnonymousUser()
        response = token_request(request)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        