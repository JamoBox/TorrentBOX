FROM python:3
ENV PYTHONUNBUFFERED 1

RUN apt-get update
RUN apt-get install -y libboost-chrono-dev \
                       libboost-python-dev \
                       libboost-random-dev \
                       libboost-system-dev \
                       libssl-dev \
                       rabbitmq-server \
                       python3-dev

# libtorrent
RUN mkdir /libtorrent
WORKDIR /libtorrent
RUN wget https://github.com/arvidn/libtorrent/releases/download/libtorrent-1_1/libtorrent-rasterbar-1.1.0.tar.gz \
    && tar xvf libtorrent-rasterbar-1.1.0.tar.gz
WORKDIR /libtorrent/libtorrent-rasterbar-1.1.0
RUN ./configure --enable-python-binding PYTHON=`which python3` \
                --with-boost-python=py`python3 -c 'import sys; print("".join(map(str, sys.version_info[:2])))'`
RUN make && make install
ENV LD_LIBRARY_PATH=/usr/local/lib

# Application
RUN mkdir /code
WORKDIR /code
ADD requirements.txt /code/
RUN pip install -r requirements.txt
ADD . /code/