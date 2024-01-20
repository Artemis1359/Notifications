from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

from api.models import Mailing, Client, Message
from api.permissions import IsAdminOrReadOnly
from api.serializers import MailingSerializer, ClientSerializer, MessageSerializer


class MailingViewSet(viewsets.ModelViewSet):
    """Вьюсет для класса Mailing."""
    queryset = Mailing.objects.all()
    permission_classes = (IsAdminOrReadOnly,)
    serializer_class = MailingSerializer

    @action(methods=('get',),
            detail=True)
    def info(self, request, pk):
        mailings = Mailing.objects.all()
        get_object_or_404(mailings, id=pk)
        queryset = Message.objects.filter(mailing_id=pk)
        serializer = MessageSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(methods=('get',),
            detail=False)
    def fullinfo(self, request):
        total_count = Mailing.objects.all().count()
        mailings = Mailing.objects.values("id")
        content = {
            'Всего рассылок:': total_count,
            'Всего сообщений:': '',
        }
        messages = {}
        for mailing in mailings:
            mail = {
                'Всего сообщений:': 0,
                'Отправлено:': 0,
                'Не отправлено:': 0,
            }
            message = Message.objects.filter(mailing_id=mailing['id']).all()
            send = message.filter(status='Send').count()
            not_send = message.filter(status='Not send').count()
            mail['Всего сообщений:'] = len(message)
            mail['Отправлено:'] = send
            mail['Не отправлено:'] = not_send
            messages[mailing['id']] = mail
        content['Всего сообщений:'] = messages
        return Response(content, status=status.HTTP_200_OK)

class ClientViewSet(viewsets.ModelViewSet):
    """Вьюсет для класса Client."""
    queryset = Client.objects.all()
    permission_classes = (IsAdminOrReadOnly,)
    serializer_class = ClientSerializer


class MessageViewSet(viewsets.ModelViewSet):
    """Вьюсет для класса Message."""
    queryset = Message.objects.all()
    permission_classes = (IsAdminOrReadOnly,)
    serializer_class = MessageSerializer
