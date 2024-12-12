from rest_framework.test import APITestCase
from rest_framework.reverse import reverse
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models import User
import json

from .models import Book


# Create your tests here.
class BookAPITestCase(APITestCase):
    def setUp(self):
        self.book = Book.objects.create(
            title="Test Book",
            author="Author",
            published_date="2023-01-01",
            isbn="1234567890123",
            pages=100
        )

        self.user = User.objects.create_user(
            username="testuser1",
            email="testuser1@example.com",
            password="securepassword123"
        )

        refresh = RefreshToken.for_user(user=self.user)
        refresh['username'] = self.user.username
        refresh['email'] = self.user.email

        self.token = str(refresh.access_token)

    def test_get_all_books(self):
        endpoint = reverse('book-list')
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)
        response = self.client.get(endpoint)
        # print(json.dumps(response.data))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_book(self):
        data = {
            "title": "New Book",
            "author": "New Author",
            "published_date": "2024-01-01",
            "isbn": "1234567890987",
            "pages": 150
        }
        endpoint = reverse('book-create')
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)
        response = self.client.post(endpoint, data)
        # print(json.dumps(response.data))
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_get_book_by_id(self):
        endpoint = reverse('book-detail', kwargs={'pk':self.book.id})
        # endpoint = reverse('book-detail', kwargs={'pk': 999})
        response = self.client.get(endpoint)
        # print(json.dumps(response.data))
        self.assertEqual(response.status_code, status.HTTP_200_OK)


    def test_update_book(self):
        data = {
            "title": "New Book",
            "author": "Lee Author",
            "published_date": "2024-11-01",
            "isbn": "1234297890987",
            "pages": 1800
        }
        endpoint = reverse('book-update', kwargs={'pk':self.book.id})
        response = self.client.put(endpoint, data=data)
        # print(json.dumps(response.data))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_book(self):
        endpoint = reverse('book-delete', kwargs={'pk':self.book.id})
        # endpoint = reverse('book-delete', kwargs={'pk': 999})
        response = self.client.delete(endpoint)
        # print(json.dumps(response.data))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


    def test_user_signup(self):
        data = {
            "username": "testuser2",
            "email": "testuser2@example.com",
            "password": "securepassword123"
        }

        endpoint  = reverse('signup')
        response = self.client.post(endpoint,data)
        # print(json.dumps(response.data))
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


    def test_user_login(self):
        data = {
            "username": "testuser1",
            "password": "securepassword123"
        }

        endpoint = reverse('login')
        response = self.client.post(endpoint, data)
        # print(json.dumps(response.data))
        self.assertEqual(response.status_code, status.HTTP_200_OK)