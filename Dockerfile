FROM python:3
ENV PYTHONUNBUFFERED 1
RUN mkdir /code
WORKDIR /code
COPY . /code/
RUN  pip install django
EXPOSE 8888
CMD ["python","manage.py","runserver","0.0.0.0:8888"]