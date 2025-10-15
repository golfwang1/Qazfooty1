# QazFooty

## Локальный запуск
```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
# Linux/Mac: source .venv/bin/activate
pip install -U pip
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver

