FROM python:3.10
EXPOSE 5000 
WORKDIR /FLASKAPI
RUN pip install flask 
COPY . /FLASKAPI/
CMD ["flask", "run", "--host", "0.0.0.0"]

