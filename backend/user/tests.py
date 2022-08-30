from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework.test import APITestCase


class UserTests(APITestCase):

    def setUp(self):
        adminuser = User.objects.create_user('admin', 'admin@test.com', '123')
        adminuser.save()
        adminuser.is_staff = True
        adminuser.save()

    def test_register(self):
        url_post = reverse('register')
        self.client.post(url_post,
                         {
                             'email': 'user@mail.ru', 'login': 'user',
                             'password': 'user1234', 'username': 'username'
                         },
                         format='json')
        self.assertEqual(User.objects.count(), 2)

    def test_me(self):
        admin = User.objects.last()
        self.client.login(username='admin', password='123')
        url_get = reverse('me')
        response = self.client.get(url_get, format='json')

        self.assertEqual(response.data['id'], admin.id)

    def test_login(self):
        last_user = User.objects.last()
        url_post = reverse('register')
        self.client.post(url_post,
                         {
                             'email': 'user@mail.ru', 'login': 'user',
                             'password': 'user1234', 'username': 'username'
                         },
                         format='json')
        self.client.login(username='username', password='user1234')
        url_me = reverse('me')
        response = self.client.get(url_me, format='json')
        self.assertEqual(response.data['id'], last_user.id + 1)


