import os
import requests
from datetime import datetime

import pytz
from celery.utils.log import get_task_logger
from dotenv import load_dotenv

from Notifications.celery import app
from api.models import Mailing, Client, Message

logger = get_task_logger(__name__)

load_dotenv()
URL = os.getenv("URL")
TOKEN = os.getenv("TOKEN")


@app.task(bind=True, retry_backoff=True)
def send_message(self, data, client_id, mailing_id, url=URL, token=TOKEN):
    mail = Mailing.objects.get(id=mailing_id)
    client = Client.objects.get(id=client_id)
    timezone = pytz.timezone(client.time_zone)
    now = datetime.now(timezone)

    if mail.start_date <= now <= mail.end_date:
        header = {
            'Authorization': f'Basic {token}',
            'content-type': 'application/json',
        }
        try:
            requests.post(url=url+str(data['id']), json=data, headers=header)
        except requests.exceptions.RequestException as exc:
            logger.error(f'Ответ с ошибкой {exc} message_id:{data["id"]}')
            raise self.retry(exc=exc)
        else:
            logger.info(f'Сообщение {data["id"]} отправлено')
            Message.objects.filter(id=data["id"]).update(status='send')
    else:
        time = 24 - (
                int(now.time().strftime("%H:%M:%S")[:2])
                - int(mail.time_start.strftime("%H:%M:%S")[:2])
        )
        logger.info(
            f"Message id: {data['id']}, "
            f"Данное время не предназначено для отправки сообщения,"
            f"Повтор будет через {60 * 60 * time} секунд"
        )
        return self.retry(countdown=60 * 60 * time)