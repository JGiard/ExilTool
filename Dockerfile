FROM python:3.6

ADD . /src
RUN pip3 install /src
RUN pip3 install uwsgi
#ADD uwsgi.ini /uwsgi.ini

ENV FLASK_APP exiltool.main:app
CMD flask run --host=0.0.0.0
#CMD uwsgi --ini /uwsgi.ini
