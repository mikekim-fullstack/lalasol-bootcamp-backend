# release:  python manage.py migrate —log-file -
# python manage.py runserver 0.0.0.0:8000
web: python manage.py migrate && gunicorn core.wsgi —log-file -


