web: python manage.py collectstatic --noinput ; newrelic-admin run-program python manage.py run_gunicorn -k tornado -b 0.0.0.0:$PORT -w 3 burstolio/settings.py