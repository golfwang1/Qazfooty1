# manage.py — точка входа для управления Django-проектом (команды runserver, migrate и т.д.)
# В реальном проекте этот файл генерируется django-admin, но здесь мы пишем минимальную версию с комментариями.
import os
import sys

def main():
    # Указываем Django, где искать настройки проекта
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'qazfooty.settings')
    try:
        from django.core.management import execute_from_command_line  # импортируем командный интерфейс Django
    except ImportError as exc:
        raise ImportError(
            "Django не установлен. Установите его через 'pip install django'."
        ) from exc
    # Передаём аргументы командной строки в Django (например, runserver)
    execute_from_command_line(sys.argv)

if __name__ == '__main__':
    main()
