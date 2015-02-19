
FROM phusion/baseimage

RUN sudo apt-get -qqy update
RUN sudo apt-get -qqy install git python
RUN git clone https://github.com/cloudmesh/cloudmesh.git
RUN cd cloudmesh && ./install system
RUN cd cloudmesh && ./install requirements
RUN cd cloudmesh && ./install new
RUN cd cloudmesh && ./install cloudmesh

EXPOSE 5000
CMD cd cloudmesh && fab server.start