release: which python && python -m venv /opt/venv && . /opt/venv/bin/activate && pip install -r requirements.txt  && python manage.py migrate
web: gunicorn core.wsgi --log-file -


