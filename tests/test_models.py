from datetime import datetime

from django.test import TestCase

from api.models import Client, Mailing, Message


class ModelsTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.mailing = Mailing.objects.create(
            start_date=datetime.now(),
            text='Test text',
            mobile_code='777',
            tag='Tag',
            end_date=datetime.now(),
        )
        cls.test_client = Client.objects.create(
            phone_number='77777777777',
            code='777',
            tag='Tag',
            time_zone='Europe/Moscow',
        )
        cls.message = Message.objects.create(
            status='not send',
            mailing_id=1,
            client_id=1
        )

    def test_mailings_creation(self):
        """Проверяем, что у модели Mailing корректно создаются поля."""
        self.assertIsInstance(self.mailing, Mailing)
        self.assertEqual(self.mailing.text, 'Test text')
        self.assertEqual(self.mailing.mobile_code, '777')
        self.assertEqual(self.mailing.tag, 'Tag')

    def test_client_creation(self):
        """Проверяем, что у модели Client корректно создаются поля."""
        self.assertIsInstance(self.test_client, Client)
        self.assertEqual(self.test_client.phone_number, '77777777777')
        self.assertEqual(self.test_client.code, '777')
        self.assertEqual(self.test_client.tag, 'Tag')
        self.assertEqual(self.test_client.time_zone, 'Europe/Moscow')

    def test_message_creation(self):
        """Проверяем, что у модели Message корректно создаются поля."""
        self.assertIsInstance(self.message, Message)
        self.assertEqual(self.message.status, 'not send')
        self.assertEqual(self.message.client_id, 1)
        self.assertEqual(self.message.mailing_id, 1)

    def test_models_have_correct_verbose_name(self):
        """Проверяем, что у моделей корректно работает verbose_name"""
        mailings_field_verbose_names = {
            'start_date': 'Дата и время запуска рассылки',
            'text': 'Сообщение клиенту',
            'tag': 'Поиск по тегу',
            'mobile_code': 'Поиск по коду оператора',
            'end_date': 'Дата и время окончания рассылки',
        }
        clients_field_verbose_names = {
            'phone_number': 'Телефонный номер',
            'code': 'Код мобильного оператора',
            'tag': 'Тег',
            'time_zone': 'Часовой пояс',
        }
        messages_field_verbose_names = {
            'create_date': 'Дата и время создания сообщения',
            'status': 'Статус отправки',
            'mailing': 'Рассылка',
            'client': 'Клиент',
        }
        for field, expected_value in mailings_field_verbose_names.items():
            with self.subTest(field=field):
                self.assertEqual(
                    self.mailing._meta.get_field(field).verbose_name, expected_value
                )
        for field, expected_value in clients_field_verbose_names.items():
            with self.subTest(field=field):
                self.assertEqual(
                    self.test_client._meta.get_field(field).verbose_name, expected_value
                )
        for field, expected_value in messages_field_verbose_names.items():
            with self.subTest(field=field):
                self.assertEqual(
                    self.message._meta.get_field(field).verbose_name, expected_value
                )

    def test_models_have_correct_object_names(self):
        """Проверяем, что у моделей корректно работает __str__."""
        title = {
            self.mailing: f'Рассылка {self.mailing.id}',
            self.test_client: f'Клиент +{self.test_client.phone_number}',
            self.message: f'{self.mailing} - {self.test_client}',
        }
        for field, expected_value in title.items():
            with self.subTest(field=field):
                self.assertEqual(str(field), expected_value)