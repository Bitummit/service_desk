import imaplib
import smtplib
import email
import re
from email.header import decode_header
from email.utils import parseaddr
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from celery import shared_task
from service_desk import celery_app
from .models import Issue, Message
from django.core.exceptions import ObjectDoesNotExist
from service_desk.settings import (
    IMAP_SERVER,
    EMAIL_ACCOUNT,
    EMAIL_PASSWORD,
    SMTP_SERVER,
    SMTP_PORT
)


AUTO_REPLY_TEXT = "Спасибо за обращение, скоро с Вами свяжется менеджер"


@celery_app.task
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


@celery_app.task
def send_mail(issue, body):
    msg = MIMEMultipart()
    msg['From'] = EMAIL_ACCOUNT
    msg['To'] = issue.client
    msg['Subject'] = issue.title
    msg.attach(MIMEText(body, 'plain'))

    try:
        with smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT) as server:
            server.login(EMAIL_ACCOUNT, EMAIL_PASSWORD)
            server.sendmail(EMAIL_ACCOUNT, issue.client, msg.as_string())
            Message.objects.create(
                answer=True,
                subject=issue.title,
                body=body
            )
            print(f"Автоответ отправлен {issue.client}")
    except Exception as e:
        print(f"Ошибка при отправке автоответа: {e}")


def parse_email(msg_data: list[bytes | tuple[bytes, bytes]]) -> None:
    # само содержание письма
    msg = email.message_from_bytes(msg_data[0][1])

    # получение темы письма
    subject = get_subject(msg)
    # получение отправителя
    from_header = msg.get("From")
    from_email = parseaddr(from_header)[1]
    # проверка на наличие id обращения в теме
    issue_id = get_issue_from_subject(subject)
    print(issue_id)
    if issue_id:
        try:
            # проверка, что данное обращение сущетсвует в БД
            issue = Issue.objects.get(pk=issue_id)
        except ObjectDoesNotExist:
            print(f"Несуществующий id обращения: {issue_id}")
    else:
        # создание нового обращения, если в теме письма нету id
        issue = Issue.objects.create(
            title=subject,
            client=from_email,
        )
        issue.title = issue.title + f"[Issue #{issue.pk}]"
        issue.save()

        send_mail.delay(issue, AUTO_REPLY_TEXT)
    try:
        # получение содержания письма
        body = get_body(msg)
    except Exception as e:
        print(f"Невозможно прочитать тело письма: {e}")
        return

    # создание сообщения и привяка к обращению
    Message.objects.create(
        subject=subject,
        body=body,
        issue=issue
    )


def get_subject(msg) -> str:
    subject, encoding = decode_header(msg["Subject"])[0]
    try:
        subject = subject.decode(encoding if encoding else "utf-8")
    except Exception as e:
        print(f"Невозможно прочитать тему письма: {e}")
    return subject

def get_body(msg) -> str:
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


def get_issue_from_subject(subject: str) -> str:
    match = re.search(r"\[Issue #(\d+)]", subject)
    return match.group(1) if match else None