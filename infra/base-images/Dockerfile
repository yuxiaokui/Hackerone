From alpine

MAINTAINER xi4okui@gmail.com

RUN sed -i 's/dl-cdn.alpinelinux.org/mirrors.aliyun.com/g' /etc/apk/repositories
RUN apk update
RUN apk add python3
RUN python3 -m pip install --upgrade pip
RUN python3 -m pip install PyChromeDevTools requests aiohttp bs4
RUN mkdir fuzz

Workdir fuzz

COPY lib lib


