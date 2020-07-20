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

RUN cmkdir -p /var/web/ptools && cd /var/web/ptools && mkdir -p db log supervisor &&

COPY ./supervisor /var/web/ptools/supervisor
ADD ./nginx/nginx.conf /var/web/ptools/nginx.conf

ENV env docker

COPY ./app /app

CMD ["/usr/bin/supervisord", "-c", "/var/web/ptools/supervisor/supervisord.conf"]
# /usr/bin/supervisord -c /var/web/ptools/supervisor/supervisord.conf
