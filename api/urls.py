from django.urls import include, path
from rest_framework.routers import DefaultRouter

from api.views import MailingViewSet, ClientViewSet, MessageViewSet
from Notifications.yasg import urlpatterns as docs

router_v1 = DefaultRouter()
router_v1.register('mailings', MailingViewSet, basename='mailings')
router_v1.register('clients', ClientViewSet, basename='clients')
router_v1.register('messages', MessageViewSet, basename='messages')

urlpatterns = [
    path('v1/', include(router_v1.urls)),
    path('auth/', include('rest_framework.urls', namespace='rest_framework'))
]

urlpatterns += docs