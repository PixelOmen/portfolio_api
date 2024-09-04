import os
from unittest.mock import patch

from django.urls import reverse
from django.conf import settings
from django.contrib.auth import get_user_model
from django.test import TestCase, override_settings
from django.core.files.uploadedfile import SimpleUploadedFile

from rest_framework.test import APIClient, APITestCase

from .models import (
    AllowedImageMimeType,
    UserLimits,
    AllowedImageMimeType,
    UserPost,
    UserImage,
    AnonMessage,
)
from .serializers import UserLimitsSerializer


# ----------------- Model Tests -------------------------------------------------------------
# -------------------------------------------------------------------------------------------
# -------------------------------------------------------------------------------------------
class AllowedImageMimeTypeTest(TestCase):
    def setUp(self):
        self.mime_type = AllowedImageMimeType.objects.create(name="image/png")

    def test_mime_type_creation(self):
        self.assertEqual(self.mime_type.name, "image/png")

    def test_mime_type_str_representation(self):
        self.assertEqual(str(self.mime_type), "image/png")


class UserLimitsTest(TestCase):
    def setUp(self):
        self.image_mime = AllowedImageMimeType.objects.create(name="image/jpeg")
        self.user_limit = UserLimits.objects.create(
            name="testlimits",
            max_image_size=5000,
            max_user_images=10,
            max_post_length=1000,
        )
        self.user_limit.allowed_image_mimes.add(self.image_mime)

    def test_user_limits_creation(self):
        self.assertEqual(self.user_limit.name, "testlimits")
        self.assertEqual(self.user_limit.max_image_size, 5000)
        self.assertEqual(self.user_limit.max_user_images, 10)
        self.assertEqual(self.user_limit.max_post_length, 1000)

    def test_user_limits_mime_types(self):
        self.assertIn(self.image_mime, self.user_limit.allowed_image_mimes.all())

    def test_user_limits_str_representation(self):
        self.assertEqual(str(self.user_limit), "testlimits")


class UserPostTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="testuser", password="testpassword"
        )
        self.user_post = UserPost.objects.create(
            owner=self.user, content="This is a test post."
        )

    def test_user_post_creation(self):
        self.assertEqual(self.user_post.owner.username, "testuser")
        self.assertEqual(self.user_post.content, "This is a test post.")

    def test_user_post_str_representation(self):
        self.assertEqual(str(self.user_post), str(self.user_post.id))


class UserImageTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="testuser", password="testpassword"
        )
        self.user_image = UserImage.objects.create(
            owner=self.user, image="images/test_image.jpg"
        )

    def test_user_image_creation(self):
        self.assertEqual(self.user_image.owner.username, "testuser")
        self.assertEqual(self.user_image.image.name, "images/test_image.jpg")

    def test_user_image_str_representation(self):
        self.assertEqual(str(self.user_image), str(self.user_image.id))


class AnonMessageTest(TestCase):
    def setUp(self):
        self.anon_message = AnonMessage.objects.create(
            name="John Doe", email="john@example.com", content="This is a test message."
        )

    def test_anon_message_creation(self):
        self.assertEqual(self.anon_message.name, "John Doe")
        self.assertEqual(self.anon_message.email, "john@example.com")
        self.assertEqual(self.anon_message.content, "This is a test message.")

    def test_anon_message_str_representation(self):
        self.assertEqual(str(self.anon_message), "John Doe")


# ----------------- View Tests -------------------------------------------------------------
# ------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------
class UserLimitsViewTest(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user_limits = UserLimits.objects.create(
            name="default",
            max_image_size=5000,
            max_user_images=10,
            max_post_length=1000,
        )

    def test_get_user_limits(self):
        response = self.client.get(reverse("user-limits"))
        self.assertEqual(response.status_code, 200)
        user_limits_data = UserLimitsSerializer(self.user_limits).data
        self.assertEqual(response.data, user_limits_data)  # type: ignore


class TokenTestViewTest(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            username="testuser",
            password="testpassword",
            email="test@example.com",
            welcome_email_sent=False,
        )
        self.client.force_authenticate(user=self.user)

    @patch("api.tasks.send_welcome_email_task.delay")
    def test_authenticated_user_sends_email(self, mock_send_email):
        response = self.client.get(reverse("token-test"))
        self.user.refresh_from_db()

        self.assertEqual(response.status_code, 200)
        self.assertTrue(self.user.welcome_email_sent)  # type: ignore
        mock_send_email.assert_called_once_with(self.user.first_name, self.user.email)

    def test_authenticated_user_without_email(self):
        """Test if email is not sent if user lacks email address"""
        self.user.email = ""
        self.user.save()
        response = self.client.get(reverse("token-test"))
        self.assertEqual(response.status_code, 200)


class AnonMessageViewSetTest(APITestCase):
    def setUp(self):
        self.client = APIClient()

    def test_create_anon_message(self):
        data = {
            "name": "John Doe",
            "email": "john@example.com",
            "content": "Test message",
        }
        response = self.client.post(reverse("anon-messages"), data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(AnonMessage.objects.count(), 1)
        message = AnonMessage.objects.first()
        self.assertIsNotNone(message)
        self.assertEqual(message.name, "John Doe")  # type: ignore
        self.assertEqual(message.email, "john@example.com")  # type: ignore

    def test_create_anon_message_invalid(self):
        data = {"name": "", "email": "not an email"}
        response = self.client.post(reverse("anon-messages"), data)
        self.assertEqual(response.status_code, 400)


class UserPostViewSetTest(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            username="testuser", password="testpassword"
        )
        self.post = UserPost.objects.create(
            owner=self.user, content="This is a test post."
        )
        self.client.force_authenticate(user=self.user)

    def test_get_user_posts(self):
        response = self.client.get(reverse("user-posts-list"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data[0]["content"], "This is a test post.")  # type: ignore

    def test_create_user_post(self):
        data = {"content": "Another test post"}
        response = self.client.post(reverse("user-posts-list"), data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(UserPost.objects.count(), 2)

    def test_update_user_post(self):
        data = {"content": "Updated content"}
        response = self.client.put(
            reverse("user-posts-detail", args=[self.post.id]), data
        )
        self.assertEqual(response.status_code, 200)
        self.post.refresh_from_db()
        self.assertEqual(self.post.content, "Updated content")

    def test_delete_user_post(self):
        response = self.client.delete(reverse("user-posts-detail", args=[self.post.id]))
        self.assertEqual(response.status_code, 204)
        self.assertEqual(UserPost.objects.count(), 0)


@override_settings(
    STORAGES={
        "default": {
            "BACKEND": "django.core.files.storage.FileSystemStorage",
        }
    },
    MEDIA_ROOT=os.path.join(os.path.dirname(__file__), "testdata/"),
    MEDIA_URL="/media/",
)
class UserImageViewSetTest(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            username="testuser", password="testpassword"
        )
        self.image = UserImage.objects.create(owner=self.user, image="test_image.jpg")
        self.client.force_authenticate(user=self.user)

    def tearDown(self):
        img_dir = settings.MEDIA_ROOT + "images/"
        img_path = img_dir + "test_image.jpg"
        if os.path.exists(img_path):
            os.remove(settings.MEDIA_ROOT + "images/test_image.jpg")
        if os.path.exists(img_dir):
            os.removedirs(settings.MEDIA_ROOT + "images/")
        if os.path.exists(settings.MEDIA_ROOT):
            os.removedirs(settings.MEDIA_ROOT)

    def test_get_user_images(self):
        """Test if user can get their own images"""
        response = self.client.get(reverse("user-images-list"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data[0]["image"], "http://testserver/media/test_image.jpg")  # type: ignore

    def test_create_user_image(self):
        """Test if user can upload an image"""
        image_data = SimpleUploadedFile(
            "test_image.jpg", b"file_content", content_type="image/jpeg"
        )
        data = {"image": image_data}
        response = self.client.post(
            reverse("user-images-list"), data, format="multipart"
        )
        self.assertEqual(response.status_code, 201)
        self.assertEqual(UserImage.objects.count(), 2)

    def test_delete_user_image(self):
        """Test if user can delete their own image"""
        response = self.client.delete(
            reverse("user-images-detail", args=[self.image.id])
        )
        self.assertEqual(response.status_code, 204)
        self.assertEqual(UserImage.objects.count(), 0)
