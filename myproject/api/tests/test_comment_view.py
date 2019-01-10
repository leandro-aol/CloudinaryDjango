from django.test import TestCase
from django.urls import reverse, resolve
from django.contrib.auth.models import User
from rest_framework import status
from ..models import EventComments
from ..views import CommentView
from rest_framework.test import APIRequestFactory
from rest_framework.test import force_authenticate
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient


class TestCommentView(TestCase):

    # É executado antes de todos os testes e serve para iniciar valores que serão usados no teste
    def setUp(self):
        self.eventComment = EventComments.objects.create(name = 'Thallison', icon_perfil = 'imagem', category = 'Palestra', comment = 'Muito bom!')
        self.factory = APIRequestFactory()
        self.user = User.objects.create(username='testuser')
        self.user.set_password('123456')
        self.user.save()
        self.view = CommentView.as_view()

        token = Token.objects.get(user__username='testuser')
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        self.data =  {
            'name': 'thallison',
            'icon_perfil': 'null',
            'category': 'Palestra',
            'comment': 'Legal'
        }

    # É passado um parâmetro válido e verifica-se se retorna o status = HTTP_200_OK
    def test_comment_view_success_status_code(self):
        url = reverse('api:comment', kwargs={'pk': self.eventComment.pk})
        request = self.factory.get(url)
        force_authenticate(request, user=self.user)
        response = self.view(request, pk=self.eventComment.pk)
        self.assertEquals(response.status_code, 200)

    # É passado mu parâmetro inválido e verifica-se se retorna o status = HTTP_404_NOT_FOUND
    def test_comment_view_not_found_status_code(self):
        url = reverse('api:comment', kwargs={'pk': 99})
        request = self.factory.get(url)
        force_authenticate(request, user=self.user)
        response = self.view(request, pk=99)
        self.assertEquals(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_comment_view_failure_status_code(self):
        url = reverse('api:comments')
        request = self.factory.get(url)
        response = self.view(request)
        self.assertEquals(response.status_code, status.HTTP_401_UNAUTHORIZED)

    # Verifica-se se a URL está chamando a view correta
    def test_comment_url_resolves_comment_view(self):
        view = resolve('/v1/comment/1/')
        self.assertEquals(view.func.view_class, CommentView)

    # Testa-se se ao alterar algum item, retorna o status = HTTP_200_OK
    def test_comment_put_success_status_code(self):
        url = '/v1/comment/{0}'.format(self.eventComment.pk)
        request = self.client.put(url, self.data)
        self.assertEqual(request.status_code, status.HTTP_200_OK)

    # Verifica-se se ao tentar alterar algum item não passando nenhum dado (ou dados incompletos) ele retorna status = HTTP_400_BAD_REQUEST
    def test_comment_put_failure_data_error_status_code(self):
        url = '/v1/comment/{0}'.format(self.eventComment.pk)
        request = self.client.put(url)
        self.assertEqual(request.status_code, status.HTTP_400_BAD_REQUEST)

    # Verifica-se se ao tentar alterar um item inexistente, retorna o status = HTTP_404_NOT_FOUND
    def test_comment_put_failure_status_code(self):
        url = '/v1/comment/99'
        request = self.client.put(url, self.data)
        self.assertEqual(request.status_code, status.HTTP_404_NOT_FOUND)

    # Deleta-se um item e verifica-se se o status de retorno é HTTP_204_NO_CONTENT
    def test_comment_delete_success_status_code(self):
        url = '/v1/comment/{0}/'.format(self.eventComment.pk)
        request = self.client.delete(url)
        self.assertEqual(request.status_code, status.HTTP_204_NO_CONTENT)

    # Tenta-se deletar um item inexistente e verifica-se se o status = HTTP_404_NOT_FOUND
    def test_comment_delete_failure_status_code(self):
        url = '/v1/comment/99'
        request = self.client.delete(url)
        self.assertEqual(request.status_code, status.HTTP_404_NOT_FOUND)
