FROM python:3.8-slim

ENV COLUMNS 80

RUN echo \
    deb https://mirrors.tuna.tsinghua.edu.cn/debian/ buster main contrib non-free\
    deb https://mirrors.tuna.tsinghua.edu.cn/debian/ buster-updates main contrib non-free\
    deb https://mirrors.tuna.tsinghua.edu.cn/debian/ buster-backports main contrib non-free\
    deb https://mirrors.tuna.tsinghua.edu.cn/debian-security buster/updates main contrib non-free\
    > /etc/apt/sources.list

RUN apt-get update && apt-get -y install ffmpeg mediainfo supervisor

COPY requirements.txt /requirements.txt

RUN pip install -r /requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple \
    && rm -rf ~/.cache

RUN mkdir -p /app/tmp && mkdir -p /ptools/db && mkdir -p /ptools/log

ADD ./supervisor/supervisord.conf /etc/supervisord.conf

COPY ./ /app

CMD ["/usr/bin/supervisord"]
