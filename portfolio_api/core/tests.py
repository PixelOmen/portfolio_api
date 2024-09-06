from django.test import TestCase

from .models import AllowedImageMimeType, UserLimits, AllowedImageMimeType


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
