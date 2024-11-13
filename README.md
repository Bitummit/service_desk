# Service Desk

Приложение работает с пользовательскими обращениями через электронную почту. Все обращения фиксируются в базе данных, сотрудники поддержки уже обрабатывают данные обращения.
## 🚀 Getting Started


### Prerequisites

Убедитесь, что у Вас установлен Docker:
- [Docker](https://docs.docker.com/get-docker/)
- [Docker Compose](https://docs.docker.com/compose/install/)

### Project Stack
- **Backend**: DRF, Celery
- **Database**: PostgreSQL
- **API Doc**: Swagger, Redoc
- **Conteinerization**: Docker, docker compose
### Environment Variables

 Создайте .env файл в корне проекта. Ниже приведены переменные, которые необходимо установить:

| Variable               | Description                                     | Example      |
|------------------------|-------------------------------------------------|--------------|
| IMAP_SERVER    | Сервер для получения писем                      | imap.mail.ru |
| EMAIL_ACCOUNT              | Почтовый аккаунт для получения и отправки писем | 1@mail.ru    |
| EMAIL_PASSWORD              | Пароль от почтового аккаунта                    | 1111         |
| SMTP_SERVER          | Сервер для отправки писем                       | smtp.mail.ru |
| SMTP_PORT              | Порт сервера для отправки писем                 | 465          |
| SECRET_KEY              | Секретный ключ приложения                       | seufg67ewgd8 |
| DB_NAME        | Название базы данных                            | service_desk |
| DB_USER                | Пользователь базы данных                        | postgres     |
| DB_PASSWORD                | Пароль пользователя базы данных                 | postgres     |
| DB_HOST                | Хост базы данных                                | 0.0.0.0      |
| DB_PORT                | Порт базы данных                                | 5432         |
| DJANGO_SUPERUSER_PASSWORD                | Пароль суперпользователя                        | 1111         |
| DJANGO_SUPERUSER_USERNAME                | Имя суперпользователя                           | admin        |
| DJANGO_SUPERUSER_EMAIL                | Почта суперпользователя                         | ""           |



### Пример .env файла:


```plaintext
IMAP_SERVER="imap.mail.ru"
EMAIL_ACCOUNT="1@mail.ru"
EMAIL_PASSWORD="password"
SMTP_SERVER="smtp.mail.ru"
SMTP_PORT="465"
SECRET_KEY="erjgoergh97yt823wfhiu2wfh3o823urj9p2wjfpwouhfu8w237fg8iw"
DB_NAME="service_desk"
DB_USER="postgres"
DB_PASSWORD="postgres"
DB_HOST="0.0.0.0"
DB_PORT="5432"
DJANGO_SUPERUSER_PASSWORD="1111"
DJANGO_SUPERUSER_USERNAME="admin"
DJANGO_SUPERUSER_EMAIL=""
```
### Для запуска проекта:
```commandline
docker-compose up --build
```

### Доступ к приложению:
Приложение запускается по адресу
```plaintext
http://0.0.0.0:8000/
```
Для перехода в swagger используется url-адрес
```plaintext
http://0.0.0.0:8000/swagger
```
Пользователь может получать все обращения, фильтровать по статусу и сортировать по дате создания.
Пользователь может поставить исполнителя обращения, поменять статусы и отправить ответ электронным письмом на номер обращения.