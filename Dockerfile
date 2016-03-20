FROM rootproject/root-ubuntu16
USER root

ADD . /phspace
WORKDIR /phspace

# Install python pip
RUN apt-get install -y python.
RUN apt-get install -y python-pip.
RUN pip install --upgrade pip.

RUN pip install -r requirements.txt
RUN pip install .
