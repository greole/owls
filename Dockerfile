FROM greole/ipandas

ADD . /opt/owls
WORKDIR /opt/owls

RUN python3 setup.py install

WORKDIR /notebooks

ENTRYPOINT ["tini", "--"]
CMD ["jupyter", "notebook"]
