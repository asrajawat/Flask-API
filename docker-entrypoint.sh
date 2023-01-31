#we want a solution where the database migrations run before the app starts. That way, it will be impossible for us to forget to run the migrations when we deploy.
#!/bin/sh

flask db upgrade

exec gunicorn --bind 0.0.0.0:80 "app:create_app()"