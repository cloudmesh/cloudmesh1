
FROM phusion/baseimage


RUN sudo apt-get -qqy update
RUN sudo apt-get -qqy install git python python-virtualenv
RUN virtualenv ~/ENV
RUN git clone https://github.com/cloudmesh/cloudmesh.git

ADD docker-with-venv with-venv
RUN echo 'export USER=docker' >>/tmp/build-env

RUN ./with-venv ~/ENV cloudmesh /tmp/build-env git checkout dev1.3
RUN ./with-venv ~/ENV cloudmesh /tmp/build-env ./install system
RUN ./with-venv ~/ENV cloudmesh /tmp/build-env ./install requirements
RUN ./with-venv ~/ENV cloudmesh /tmp/build-env ./install new
RUN ./with-venv ~/ENV cloudmesh /tmp/build-env ./install cloudmesh
RUN rm /tmp/build-env

EXPOSE 5000
# cd cloudmesh && fab server.start
CMD bash -l
