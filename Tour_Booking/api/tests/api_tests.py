from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from tour_booking.models import Tour, FavoriteTour

class LoginViewTestCase(APITestCase):
        def setUp(self):
            self.client = APIClient()
            self.user = User.objects.create_user(username='testuser', password='testpassword')

        def test_successful_login(self):
            response = self.client.post(
                reverse("api-login"),
                data={"username": "testuser", "password": "testpassword"},
                format="json",
            )
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertIn("access_token", response.data)
            self.assertIn("message", response.data)
            self.assertEqual(response.data["message"], "Login successful")

        def test_incorrect_password(self):
            response = self.client.post(
                reverse("api-login"),
                data={"username": "testuser", "password": "wrongpassword"},
                format="json",
            )
            self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
            self.assertIn("message", response.data)
            self.assertEqual(response.data["message"], "Incorrect username or password")

        def test_nonexistent_account(self):
            response = self.client.post(
                reverse("api-login"),
                data={"username": "nonexistentuser", "password": "testpassword"},
                format="json",
            )
            self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
            self.assertIn("message", response.data)
            self.assertEqual(response.data["message"], "Account does not exist")

        def test_missing_username(self):
            response = self.client.post(
                reverse("api-login"),
                data={"password": "testpassword"},
                format="json",
            )
            self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
            self.assertIn("message", response.data)
            self.assertEqual(response.data["message"], "Account does not exist")

        def test_missing_password(self):
            response = self.client.post(
                reverse("api-login"),
                data={"username": "testuser"},
                format="json",
            )
            self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
            self.assertIn("message", response.data)
            self.assertEqual(response.data["message"], "Incorrect username or password")

        def test_inactive_account(self):
            self.user.is_active = False
            self.user.save()

            response = self.client.post(
                reverse("api-login"),
                data={"username": "testuser", "password": "testpassword"},
                format="json",
            )
            self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
            self.assertIn("message", response.data)
            self.assertEqual(response.data["message"], "Account does not exist")

class ToggleFavoriteTourViewTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username="testuser", password="testpassword")
        self.client.force_authenticate(user=self.user)
        self.tour = Tour.objects.create(name="Test Tour", price=100.00, average_rating=5.0)

    def test_toggle_favorite_authenticated(self):
        response = self.client.post(reverse("toggle-favorite-tour", args=[self.tour.id]))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("message", response.data)
        self.assertTrue(
            "Tour đã được thêm vào danh sách yêu thích." in response.data["message"]
            or "Tour đã được xóa khỏi danh sách yêu thích." in response.data["message"]
        )

    def test_toggle_favorite_unauthenticated(self):
        self.client.logout()
        response = self.client.post(reverse("toggle-favorite-tour", args=[self.tour.id]))

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class FavoriteToursListViewTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username="testuser", password="testpassword")
        self.client.force_authenticate(user=self.user)
        self.tour = Tour.objects.create(name="Test Tour", price=100.00, average_rating=5.0)

    def test_favorite_tours_list_authenticated_empty(self):
        response = self.client.post(reverse("favorite-tours-list"))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["message"], "Không có tour yêu thích nào.")

    def test_favorite_tours_list_authenticated_non_empty(self):
        favorite_tour = FavoriteTour.objects.create(user=self.user, tour=self.tour)
        
        response = self.client.post(reverse("favorite-tours-list"))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["message"], "Danh sách các tour yêu thích.")
        self.assertIn("favorite_tours", response.data)
        self.assertEqual(len(response.data["favorite_tours"]), 1)
        self.assertEqual(response.data["favorite_tours"][0]["id"], favorite_tour.tour.id)
