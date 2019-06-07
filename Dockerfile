FROM python:3.7.0

RUN groupadd -r uwsgi && useradd -r -g uwsgi uwsgi
RUN pip install Flask -U
RUN pip install uWSGI -U
RUN pip install requests -U
RUN pip install redis -U
WORKDIR /app
COPY app /app
COPY cmd.sh /

EXPOSE 9090 9191
USER uwsgi

CMD ["/cmd.sh"]
