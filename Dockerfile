FROM ubuntu:latest

RUN apt update && apt -y install \
    python3 \
    python3-pip \
    dos2unix

ADD requirements.txt /
RUN pip3 install -r /requirements.txt

ADD entrypoint.sh /
RUN dos2unix /entrypoint.sh
RUN chmod +x /entrypoint.sh

CMD exec bash -c "/entrypoint.sh"