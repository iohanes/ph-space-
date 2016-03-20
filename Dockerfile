FROM rootproject/root-ubuntu16

ADD . /phspace
WORKDIR /phspace

RUN pip install requirements.txt
RUN pip install .
