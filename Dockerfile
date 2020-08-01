FROM python:3.8-slim

ENV COLUMNS 80

RUN echo \
    deb https://mirrors.tuna.tsinghua.edu.cn/debian/ buster main contrib non-free\
    deb https://mirrors.tuna.tsinghua.edu.cn/debian/ buster-updates main contrib non-free\
    deb https://mirrors.tuna.tsinghua.edu.cn/debian/ buster-backports main contrib non-free\
    deb https://mirrors.tuna.tsinghua.edu.cn/debian-security buster/updates main contrib non-free\
    > /etc/apt/sources.list

RUN apt-get update && apt-get -y install ffmpeg mediainfo supervisor nginx

COPY requirements.txt /requirements.txt

RUN pip install -r /requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple \
    && rm -rf ~/.cache

RUN mkdir -p /var/web/ptools && cd /var/web/ptools && mkdir -p db log supervisor app

COPY ./supervisor /var/web/ptools/supervisor
COPY ./nginx/nginx.conf /etc/nginx/nginx.conf

ENV env docker

RUN apt-get -y install unzip

COPY ./backend/app /var/web/ptools/app/app
COPY ./frontend/dist /var/web/ptools/app/frontend
COPY ./backend/manager /var/web/ptools/manager

CMD ["/usr/bin/supervisord", "-c", "/var/web/ptools/supervisor/supervisord.conf"]
# /usr/bin/supervisord -c /var/web/ptools/supervisor/supervisord.conf
