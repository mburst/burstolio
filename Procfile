web: python manage.py collectstatic --noinput ; python manage.py gunicorn_django -b 0.0.0.0:$PORT -w 3 burstolio/settings.py
