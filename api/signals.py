from django.db.models import Q
from django.db.models.signals import post_save
from django.dispatch import receiver

from api.models import Mailing, Client, Message
from api.tasks import send_message



@receiver(post_save, sender=Mailing)
def create_message(sender, instance, created, **kwargs):
    print(f"Object with id {instance.id} saved successfully!")
    if created:
        mailing = Mailing.objects.filter(id=instance.id).first()
        clients = Client.objects.filter(
            Q(code=mailing.mobile_code) | Q(tag=mailing.tag)
        ).all()

        for client in clients:
            Message.objects.create(
                status='not send',
                client_id=client.id,
                mailing_id=instance.id
            )
            message = Message.objects.filter(
                mailing_id=instance.id
            ).first()
            data = {
                'id': message.id,
                'phone': client.phone_number,
                'text': mailing.text,
            }
            client_id = client.id
            mailing_id = mailing.id

            if instance.to_send:
                send_message.apply_async(
                    (data, client_id, mailing_id), expires=mailing.end_date
                )
            else:
                send_message.apply_async(
                    (data, client_id, mailing_id),
                    eta=mailing.start_date,
                    expires=mailing.end_date
                )