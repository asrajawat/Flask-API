# FROM python:3.10
# EXPOSE 5000 
# WORKDIR /FLASKAPI
# COPY ./requirements.txt requirements.txt
# RUN pip install --no-cache-dir --upgrade -r requirements.txt
# COPY . /FLASKAPI/
# CMD ["gunicorn", "--bind", "0.0.0.0", "app:create_app()"]
FROM python:3.10
WORKDIR /FLASKAPI
COPY ./requirements.txt requirements.txt
RUN pip install --no-cache-dir --upgrade -r requirements.txt
COPY . /FLASKAPI/
CMD ["/bin/bash", "docker-entrypoint.sh"]