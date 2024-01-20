from django.core.validators import RegexValidator
from django.db import models
import pytz
from django.utils import timezone


class Mailing(models.Model):
    """Класс для рассылок."""

    start_date = models.DateTimeField(
        verbose_name='Дата и время запуска рассылки'
    )
    text = models.TextField(
        max_length=200,
        verbose_name='Сообщение клиенту'
    )
    mobile_code = models.CharField(
        max_length=3,
        verbose_name='Поиск по коду оператора',
        blank=True
    )
    tag = models.CharField(
        max_length=20,
        verbose_name='Поиск по тегу',
        blank=True
    )
    end_date = models.DateTimeField(
        verbose_name='Дата и время окончания рассылки'
    )

    class Meta:
        ordering = ('-start_date',)
        verbose_name = 'Рассылка'
        verbose_name_plural = 'Рассылки'

    @property
    def to_send(self):
        return bool(self.start_date <= timezone.now() <= self.end_date)

    def __str__(self):
        return f'Рассылка {self.id}'


class Client(models.Model):
    """Класс для клиентов."""

    TIMEZONES = tuple(zip(pytz.all_timezones, pytz.all_timezones))

    phone_number = models.CharField(
        verbose_name='Телефонный номер',
        max_length=11,
        unique=True,
        validators=[
            RegexValidator(
                regex=r'^7\d{10}$',
                message='Phone number must be entered in the format: 7XXXXXXXXXX'
            )
        ]
    )
    code = models.CharField(max_length=3, verbose_name='Код мобильного оператора')
    tag = models.CharField(max_length=20, verbose_name='Тег')
    time_zone = models.CharField(
        max_length=32,
        choices=TIMEZONES,
        default='Europe/Moscow',
        verbose_name='Часовой пояс'
    )

    class Meta:
        ordering = ('id',)
        verbose_name = 'Клиент'
        verbose_name_plural = 'Клиенты'

    def __str__(self):
        return f'Клиент +{self.phone_number}'


class Message(models.Model):
    """Класс для сообщений."""

    SEND_STATUS = [
        ('send', 'Send'),
        ('not send', 'Not send'),
    ]

    create_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата и время создания сообщения'
    )
    status = models.CharField(
        max_length=10,
        choices=SEND_STATUS,
        verbose_name='Статус отправки'
    )
    mailing = models.ForeignKey(
        Mailing,
        verbose_name='Рассылка',
        related_name='messages',
        on_delete=models.CASCADE
    )
    client = models.ForeignKey(
        Client,
        verbose_name='Клиент',
        related_name='messages',
        on_delete=models.CASCADE
    )

    class Meta:
        ordering = ('-create_date',)
        verbose_name = 'Сообщение'
        verbose_name_plural = 'Сообщения'

    def __str__(self):
        return f'{self.mailing} - {self.client}'
