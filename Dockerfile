FROM jupyter/notebook

ADD . /opt/owls
WORKDIR /opt/owls
RUN apt-get update && \
    apt-get install -y libpng12-dev libfreetype6-dev

RUN python3 -m pip install numpy
RUN python3 -m pip install pandas

RUN python3 -m pip install matplotlib

RUN python3 setup.py install

WORKDIR /notebooks

ENTRYPOINT ["tini", "--"]
CMD ["jupyter", "notebook"]
