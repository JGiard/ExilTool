FROM python:3.6

ADD . /src
RUN pip3 install /src
RUN pip3 install uwsgi

ADD uwsgi.ini /uwsgi.ini
CMD uwsgi --ini /uwsgi.ini
