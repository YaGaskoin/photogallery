import io

from PIL import Image as PilImage
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse
from rest_framework.test import APITestCase
from gallery.models import Image


class ImageTests(APITestCase):

    def setUp(self):
        adminuser = User.objects.create_user('admin', 'admin@test.com', '123')
        adminuser.save()
        adminuser.is_staff = True
        adminuser.save()

        newImage = Image()
        newImage.image = self.generate_photo_file()
        newImage.user_id = adminuser.id
        newImage.save()

        self.client.login(username='admin', password='123')

    def generate_photo_file(self, name='test.png', width=100, height=100):
        bts = io.BytesIO()
        img = PilImage.new("RGB", (width, height))
        img.save(bts, 'jpeg')
        return SimpleUploadedFile(name, bts.getvalue())

    def test_create_image(self):
        last_user = User.objects.last()
        url_post = reverse('image-list')
        image = self.generate_photo_file()
        self.client.post(url_post, {'image': image, 'user': last_user.id}, format='multipart')
        self.assertEqual(Image.objects.count(), 2)

    def test_get_image(self):
        last_obj = Image.objects.last()
        url_get = reverse('image-detail', kwargs={'pk': last_obj.id})
        response = self.client.get(url_get, format='json')

        self.assertEqual(response.data['image'], 'http://testserver' + last_obj.image.url)

    def test_update_image(self):
        image = self.generate_photo_file('test-error.png', 200, 200)
        last_obj = Image.objects.last()
        url_put = reverse('image-detail', kwargs={'pk': last_obj.id})
        response = self.client.patch(url_put, {'image': image}, format='multipart')
        self.assertEqual(Image.objects.count(), 1)
        self.assertEqual(response.status_code, 200)

    def test_delete_image(self):
        last_obj = Image.objects.last()
        url_delete = reverse('image-detail', kwargs={'pk': last_obj.id})
        self.client.delete(url_delete, format='json')
        self.assertEqual(Image.objects.count(), 0)
