import imaplib
import email
from base64 import decode
from curses.ascii import isupper
from email.header import decode_header
from json.encoder import ESCAPE

from celery import shared_task
from .models import Issue, Message
import re
import datetime
from django.core.exceptions import ObjectDoesNotExist
from service_desk.settings import (
    IMAP_SERVER,
    EMAIL_ACCOUNT,
    EMAIL_PASSWORD
)

@shared_task
def fetch_email():
    try:
        mail_service = imaplib.IMAP4_SSL(IMAP_SERVER)
        mail_service.login(EMAIL_ACCOUNT, EMAIL_PASSWORD)
        mail_service.select("inbox")

        status, messages = mail_service.search(None, '(UNSEEN)')
        mail_ids = messages[0].split()

        for mail_id in mail_ids:
            status, msg_data = mail_service.fetch(mail_id, '(RFC822)')
            parse_email(msg_data)
            mail_service.store(mail_id, "+FLAGS", "\\Seen")
            print("Сообщение обработано!")
        mail_service.logout()
    except Exception as e:
        print(f"Ошибка при проверке почты: {e}")


def parse_email(msg_data):
    msg = email.message_from_bytes(msg_data[0][1]) # само содержание письма

    subject = get_subject(msg) # получение темы письма
    from_ = msg.get("From") # получение отправителя
    issue_id = get_issue_from_subject(subject) # проверка на сущетсвующее обращение
    if issue_id:
        try:
            issue = Issue.objects.get(pk=issue_id) # проверка, что данное обращение сущетсвует
        except ObjectDoesNotExist:
            print(f"Несуществующий id обращения: {issue_id}")
    else:
        issue = Issue.objects.create(
            title=subject,
            client=from_,
        ) # создание нового обращения, если в теме письма нету id
    try:
        body = get_body(msg) # получение содержания пиьсма
    except Exception as e:
        print(f"Невозможно прочитать тело письма: {e}")

    Message.objects.create(
        subject=subject,
        body=body,
        issue=issue
    ) # создание сообщения и привяка к обращению


def get_subject(msg):
    subject, encoding = decode_header(msg["Subject"])[0]
    try:
        subject = subject.decode(encoding if encoding else "utf-8")
    except Exception as e:
        print(f"Невозможно прочитать тему письма: {e}")
    return subject

def get_body(msg):
    body = ""
    if msg.is_multipart():
        for part in msg.walk():
            content_type = part.get_content_type()
            content_disposition = str(part.get("Content-Disposition"))
            if content_type == "text/plain" and "attachment" not in content_disposition:
                body = part.get_payload(decode=True).decode(part.get_content_charset() or "utf-8")
                break
    else:
        body = msg.get_payload(decode=True).decode(msg.get_content_charset() or "utf-8")
    return body
def get_issue_from_subject(subject):
    match = re.match(r"\[Issue #(\d+)]", subject)
    return match.group(1) if match else None