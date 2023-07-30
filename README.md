# xlsxparser
Тестовое задание для MotionLogic

### Общая схема проекта
![схема](https://github.com/ProtKsen/xlsxparser/blob/main/figs/structure.png?raw=true)

Приложение реализовано на Django, база данных - PostgreSQL, менеджер зависимостей - poetry, парсинг файла выполняется с использованием openpyxl.

Сделан минимальный интерфейс для загрузки файла [ссылка при локальном запуске](http://127.0.0.1:8000). API передает имя файла в брокер сообщений, откуда его считывает парсер.
Парсер кладет данные в БД, используя модели из django приложения billboards.


### Схема базы данных
![db](https://github.com/ProtKsen/xlsxparser/blob/main/figs/db.png?raw=true)


### Использование

* Установка

```bash
git@github.com:ProtKsen/xlsxparser.git
```

* Установка poetry, выполняется один раз

```bash
pip install poetry
poetry config virtualenvs.in-project true
```

* Установка зависимостей

```bash
poetry init
poetry install
```

* Настройки окружения

Создать файл `.env` на базе `.env.default` (для тестового запуска достаточно переименовать .env.default в .env)

* Установка docker, выполняется один раз

См. <https://docs.docker.com/engine/install/>

* Запуск базы данных и выполнение миграций

```bash
make db.run
make db.migrate
```

* Запуск брокера сообщений

```bash
make rabbit.run
```

* Запуск api

```bash
make api.run
```

* В отдельном терминале запуск парсера
```bash
make parser.run
```
