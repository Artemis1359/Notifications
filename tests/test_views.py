from datetime import datetime

from django.contrib.auth import get_user_model
from django.test import Client as Cl, TestCase
from rest_framework import status

from api.models import Client, Mailing, Message

User = get_user_model()


class ViewsTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_superuser(username='Auth')
        self.authorized_client = Cl()
        self.authorized_client.force_login(self.user)

    def test_mailing_view(self):
        mailing_count = Mailing.objects.all().count()
        mailing_dict = {
            'start_date': datetime.now(),
            'text': 'Test text',
            'mobile_code': '777',
            'tag': 'Tag',
            'end_date': datetime.now(),
        }
        response = self.authorized_client.post('http://127.0.0.1:8000/api/v1/mailings/', mailing_dict)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Mailing.objects.all().count(), mailing_count + 1)
        self.assertEqual(response.data['mobile_code'], '777')
        self.assertEqual(response.data['tag'], 'Tag')
        self.assertEqual(response.data['text'], 'Test text')
        self.assertIsInstance(response.data['mobile_code'], str)
        self.assertIsInstance(response.data['tag'], str)
        self.assertIsInstance(response.data['text'], str)

    def test_mailing_list_view(self):
        response = self.client.get('http://127.0.0.1:8000/api/v1/mailings/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_client_view(self):
        client_count = Client.objects.all().count()
        client_dict = {
            'phone_number': '77777777777',
            'code': '777',
            'tag': 'Tag',
            'time_zone': 'Europe/Moscow'
        }
        response = self.authorized_client.post('http://127.0.0.1:8000/api/v1/clients/', client_dict)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Client.objects.all().count(), client_count + 1)
        self.assertEqual(response.data['phone_number'], '77777777777')
        self.assertEqual(response.data['code'], '777')
        self.assertEqual(response.data['tag'], 'Tag')
        self.assertEqual(response.data['time_zone'], 'Europe/Moscow')
        self.assertIsInstance(response.data['phone_number'], str)
        self.assertIsInstance(response.data['code'], str)
        self.assertIsInstance(response.data['tag'], str)
        self.assertIsInstance(response.data['time_zone'], str)

    def test_client_list_view(self):
        response = self.client.get('http://127.0.0.1:8000/api/v1/clients/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_message_list_view(self):
        response = self.client.get('http://127.0.0.1:8000/api/v1/messages/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_info_view(self):
        self.test_mailing_view()
        response = self.client.get('http://127.0.0.1:8000/api/v1/mailings/fullinfo/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['Всего рассылок:'], 1)
        self.assertIsInstance(response.data['Всего рассылок:'], int)
        self.assertIsInstance(response.data['Всего сообщений:'], dict)
        response = self.client.get('http://127.0.0.1:8000/api/v1/mailings/2/info/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = self.client.get('http://127.0.0.1:8000/api/v1/mailings/3/info/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
