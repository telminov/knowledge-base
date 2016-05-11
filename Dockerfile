FROM telminov/ubuntu-14.04-python-3.5

EXPOSE 8000

VOLUME /conf/
VOLUME /static/

ADD . /opt/kb/
WORKDIR /opt/kb/
RUN pip3 install -r requirements.txt
CMD test "$(ls /conf/local_settings.py)" || cp project/local_settings.sample.py /conf/local_settings.py; \
    rm /opt/kb/project/local_settings.py; ln -s /conf/local_settings.py /opt/kb/project/local_settings.py;\
    rm -rf static; ln -s /static static; \
    python3 ./manage.py migrate; \
    python3 ./manage.py collectstatic --noinput; \
    python3 ./manage.py runserver 0.0.0.0:8000;
    #TODO Статика
    # Сделать запуск