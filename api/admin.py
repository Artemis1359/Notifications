from django.contrib import admin

from api.models import Mailing, Client, Message


@admin.register(Mailing)
class MailingAdmin(admin.ModelAdmin):
    list_display = ('id', 'start_date', 'end_date', 'tag', 'mobile_code', 'text')
    list_filter = ('start_date', 'end_date', 'tag', 'mobile_code')
    search_fields =('id', 'start_date', 'end_date', 'tag', 'mobile_code', 'text')
    empty_value_display = '-пусто-'


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('id','phone_number', 'code', 'tag', 'time_zone')
    search_fields = ('id', 'phone_number', 'code', 'tag', 'time_zone')
    empty_value_display = '-пусто-'


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('id', 'create_date', 'status', 'mailing', 'client')
    list_filter = ('create_date', 'status')
    search_fields =('id', 'create_date', 'status', 'mailing', 'client')
    empty_value_display = '-пусто-'
