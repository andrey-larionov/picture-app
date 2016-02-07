from django.test import TestCase
from django.core.urlresolvers import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.models import User
from pics.models import Picture
from rest_framework.authtoken.models import Token
import json
from django.core.files.uploadedfile import SimpleUploadedFile
from io import BytesIO
from PIL import Image
from django.conf import settings
from shutil import rmtree
import os


class UserTest(APITestCase):

    def setUp(self):
        self.dev_user_dict = {
            'id': 1, 
            'username': 'devuser', 
            'email': 'devuser@email.com',
        }
        self.dev_user = User.objects.create(**self.dev_user_dict)
        self.dev_user.set_password('12345')
        self.dev_user.save()

    def test_get_user_list(self):
        """
        Ensure we can get user's list.
        """
        url = reverse('users-list')
        response = self.client.get(url, {})
        response_data = json.loads(json.dumps(response.data))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(len(response_data), 1)
        self.assertEqual(response_data, [self.dev_user_dict])

    def test_token_created(self):
        """
        Check that token created when user creating
        and we can get it by username an password
        """

        url = reverse('get-auth-token')
        response = self.client.post(url, {'username': 'devuser', 'password': '12345'})
        response_data = json.loads(json.dumps(response.data))
        self.assertEqual(Token.objects.get(user=self.dev_user).key, response_data['token'])
        self.assertEqual(Token.objects.count(), 1)


    def test_create_user_and_get_auth_token_by_credentials(self):
        """
        Ensure we can create user and token was created as well
        Ensure we can get token by username an password
        """
        url = reverse('users-list')
        data = {
            'username': 'johndoe',
            'email': 'johndoe@email.com',
            'password': 'qwerty'
        }
        response = self.client.post(url, data)
        response_data = json.loads(json.dumps(response.data))

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 2)
        self.assertEqual(response_data['username'], data['username'])
        self.assertEqual(response_data['email'], data['email'])
        self.assertIn('id', response_data.keys())

        url = reverse('get-auth-token')
        data.pop('email', None)

        response = self.client.post(url, data)
        response_data = json.loads(json.dumps(response.data))
        self.assertIn('token', response_data)
        self.assertEqual(Token.objects.count(), 2)


class PictureTest(APITestCase):

    def setUp(self):
        # Set test MEDIA_ROOT folder
        settings.MEDIA_ROOT += '_test'
        self.test_user_dict = {
            'id': 1, 
            'username': 'testuser1', 
            'email': 'testuser1@email.com',
        }
        self.test_user = User.objects.create(**self.test_user_dict)
        self.test_user.set_password('12345')
        self.test_user.save()

        self.test_user_2_dict = {
            'id': 2, 
            'username': 'testuser2', 
            'email': 'testuser2@email.com',
        }
        self.test_user_2 = User.objects.create(**self.test_user_2_dict)
        self.test_user_2.set_password('12345')
        self.test_user_2.save()

        self.test_picture_dict = {
            'user': self.test_user,
            'image': SimpleUploadedFile('test_image.jpg', b'image content'),
        }
        self.test_picture = Picture.objects.create(**self.test_picture_dict)

    def tearDown(self):
        # Remove test MEDIA_ROOT folder
        test_uploads_path = os.path.join(os.path.dirname(__file__), os.pardir) + '/uploads_test'
        rmtree(test_uploads_path)

    def test_get_picture_list(self):
        """
        Ensure we can get picture's list.
        """

        url = reverse('pictures-list')

        response = self.client.get(url, {})
        # Ensure we can't send unauthorized request
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        self.client.force_authenticate(user=self.test_user)
        response = self.client.get(url, {})

        response_data = json.loads(json.dumps(response.data))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('id',  response_data[0])
        self.assertIn('image',  response_data[0])
        self.assertEqual('0.00',  response_data[0]['average_rate'])

    def test_get_picture_list_with_filter_by_user(self):
        """
        Check that we can use filter by user as query parameter
        """

        picture_dict = {
            'user': self.test_user_2,
            'image': SimpleUploadedFile('test_image2.jpg', b'image content'),
        }
        test_picture = Picture.objects.create(**picture_dict)

        url = reverse('pictures-list')
        self.client.force_authenticate(user=self.test_user)

        response = self.client.get(url, {})
        response_data = json.loads(json.dumps(response.data))
        # Check pictures count without 'u' parameter
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response_data), 2)

        response = self.client.get(url, {'u': self.test_user_2.id})
        response_data = json.loads(json.dumps(response.data))
        # Check pictures count with 'u' parameter
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response_data), 1)
        # Ensure that given image belongs to user
        self.assertEqual(response_data[0]['image'], "%s/%s" % (self.test_user_2.id, 'test_image2.jpg'))

        response = self.client.get(url, {'u': 999})
        response_data = json.loads(json.dumps(response.data))
        # Check pictures count with non-exists user id parameter
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response_data), 0)


    def test_upload_picture(self):
        """
        Ensure we can create picture
        """

        url = reverse('pictures-list')
        self.client.force_authenticate(user=self.test_user)

        # In-memory image file for test upload
        file_obj = BytesIO()
        image = Image.new("RGBA", size=(50,50), color=(256,0,0))
        image.save(file_obj, 'png')
        file_obj.name = 'test.png'
        file_obj.seek(0)

        data = {
            'user': self.test_user,
            'image': file_obj
        }

        response = self.client.post(url, data)
        response_data = json.loads(json.dumps(response.data))

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response_data['image'], "%s/%s" % (self.test_user.id, file_obj.name))
        self.assertEqual(response_data['average_rate'], '0.00')


class PictureRateTest(APITestCase):
    
    def setUp(self):
         # Set test MEDIA_ROOT folder
        settings.MEDIA_ROOT += '_test'
        self.test_user_dict = {
            'id': 1, 
            'username': 'testuser1', 
            'email': 'testuser1@email.com',
        }
        self.test_user = User.objects.create(**self.test_user_dict)
        self.test_user.set_password('12345')
        self.test_user.save()

        self.test_picture_dict = {
            'user': self.test_user,
            'image': SimpleUploadedFile('test_image.jpg', b'image content'),
        }
        self.test_picture = Picture.objects.create(**self.test_picture_dict)

    def tearDown(self):
        # Remove test MEDIA_ROOT folder
        test_uploads_path = os.path.join(os.path.dirname(__file__), os.pardir) + '/uploads_test'
        rmtree(test_uploads_path)

    def test_user_can_get_rated_pictures(self):
        test_user = User.objects.create(
            id=2, 
            username='testuser2', 
            email='testuser2@email.com'
        )
        test_user.set_password('12345')
        test_user.save()

        test_picture = Picture.objects.create(
            user=test_user,
            image=SimpleUploadedFile('test_image2.jpg', b'image content'),
        )

        url = reverse('picture-rate-list')
        self.client.force_authenticate(user=test_user)

        # Rate two pictures
        self.client.post(url, {
            'picture': test_picture.id,
            'rate': 10,
        })
        self.client.post(url, {
            'picture': self.test_picture.id,
            'rate': 9,
        })

        url = reverse('picture-rated')

        response = self.client.get(url, {})
        response_data = json.loads(json.dumps(response.data))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response_data), 2)

        self.client.force_authenticate(user=self.test_user)
        response = self.client.get(url, {})
        response_data = json.loads(json.dumps(response.data))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response_data), 0)



    def test_user_can_rate_picture(self):
        """
        Ensure user can rate picture
        """

        url = reverse('picture-rate-list')
        self.client.force_authenticate(user=self.test_user)

        data = {
            'picture': self.test_picture.id,
            'rate': 5
        }
        response = self.client.post(url, data)
        response_data = json.loads(json.dumps(response.data))

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response_data['rate'], 5)
        self.assertEqual(response_data['picture'], self.test_picture.id)

        data = {
            'picture': self.test_picture.id,
            'rate': 6
        }
        response = self.client.post(url, data)
        response_data = json.loads(json.dumps(response.data))
        # User can rate picture once
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response_data, ['You are already voted this picture.'])
        
    def test_average_rate_calculation(self):
        """
        Ensure user can rate picture
        """

        url = reverse('picture-rate-list')
        self.client.force_authenticate(user=self.test_user)

        data = {
            'picture': self.test_picture.id,
            'rate': 11
        }
        response = self.client.post(url, data)
        response_data = json.loads(json.dumps(response.data))
        # Check rate value max value
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response_data, ['Rate value should be in range 1 .. 10.'])

        data = {
            'picture': self.test_picture.id,
            'rate': 0
        }
        response = self.client.post(url, data)
        response_data = json.loads(json.dumps(response.data))
        # Check rate value min value
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response_data, ['Rate value should be in range 1 .. 10.'])

        data = {
            'picture': self.test_picture.id,
            'rate': 1.5
        }
        response = self.client.post(url, data)
        response_data = json.loads(json.dumps(response.data))
        # Check rate value wrong format
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response_data, {'rate': ['A valid integer is required.']})

        data = {
            'picture': self.test_picture.id,
            'rate': 5
        }
        response = self.client.post(url, data)
        response_data = json.loads(json.dumps(response.data))

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response_data['rate'], 5)
        self.assertEqual(response_data['picture'], self.test_picture.id)
        self.assertEqual(Picture.objects.get(pk=self.test_picture.id).average_rate, 5.00)

        test_user_dict = {
            'id': 2, 
            'username': 'testuser2', 
            'email': 'testuser2@email.com',
        }
        test_user = User.objects.create(**test_user_dict)
        test_user.set_password('12345')
        test_user.save()

        self.client.force_authenticate(user=test_user)

        data = {
            'picture': self.test_picture.id,
            'rate': 9,
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Picture.objects.get(pk=self.test_picture.id).average_rate, 7.00)