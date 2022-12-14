### Проектная работа
### "Поиск групп с целевой аудиторией в ВКонтакте"
#### Цель:
Приложение позволяет найти группы популярной сети ВКонтакте с интересующей Вас аудиторией.
#### Описание:
Поиск целевой аудитории происходит как по общей информации о группах, так и по поиску пользователей
групп по определенным параметрам.

#### В проекте реализованы следующие функциональные возможности:
- в Django интегрирован Celery для повышения производительности вебприложения и 
для эффективного скачивания информации о группах и их пользователей с VKAPI
- для хранения очередей сообщений и результатов выполнения задач Celery
использован брокер сообщений Rabbitmq
- для мониторинга и администрирования заданий применялся Flower
- данные хранятся в базе данных postgresql
- база данных обновляется каждые 48 часов при запуске приложения
- для запуска и развертывания приложения использовался Docker и Docker Compose
- для работы приложения необходимо получить токены доступа 
- (https://vk.com/dev/access_token) и записать в файл "vksearch/tokens.txt" через символ '\n'.

#### Запуск приложения:

```
docker-compose up -d --build 
``` 