from rest_framework import serializers

from api.models import Mailing, Message, Client


class MailingSerializer(serializers.ModelSerializer):
    """Сериализация данных для создания рассылки."""

    class Meta:
        model = Mailing
        fields = '__all__'


class ClientSerializer(serializers.ModelSerializer):
    """Сериализация данных для создания клиента."""

    class Meta:
        model = Client
        fields = '__all__'


class MessageSerializer(serializers.ModelSerializer):
    """Сериализация данных для создания сообщения."""

    class Meta:
        model = Message
        fields = '__all__'
