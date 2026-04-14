from http import HTTPStatus

from django.test import TestCase
from django.urls import reverse

from habits.models import Habit
from users.models import User


class RegisterUserTestCase(TestCase):
    def setUp(self):
        self.data = {
            'username': 'test',
            'email': 'test@gmail.com',
            'password': 'test',
        }
        self.path = reverse('users:register')

    def test_creates_user(self):
        response = self.client.post(self.path, data=self.data)
        json = response.json()

        self.assertEqual(json['username'], self.data['username'])
        self.assertEqual(json['email'], self.data['email'])
        self.assertEqual(response.status_code, HTTPStatus.CREATED)
        self.assertTrue(User.objects.filter(username=self.data['username']).exists())

    def test_when_request_is_invalid_nad_returns_errors(self):
        self.data['email'] = ''
        response = self.client.post(self.path, data=self.data)
        json = response.json()

        self.assertTrue(json['errors']['email'])
        self.assertEqual(response.status_code, HTTPStatus.BAD_REQUEST)


class UserHabitListCreateView(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create(username='test', email='', password='')
        cls.data = {'title': 'title'}
        cls.path = reverse('users:user_habits', args=(cls.user.username,))

    def test_user_is_attached_when_creating_habit(self):
        self.client.force_login(self.user)
        response = self.client.post(self.path, data=self.data)

        self.assertEqual(response.status_code, HTTPStatus.CREATED)
        self.assertTrue(Habit.objects.filter(user=self.user, title=self.data['title']).exists())