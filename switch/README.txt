Installation

In the freeswitch source directory change to libs/esl and run:
make pymod
make pymod-install

cd /usr/src/freeswitch/libs/esl/
cp ESL.py /usr/local/venv/lib/python2.7/site-packages/
cp _ESL.so /usr/local/venv/lib/python2.7/site-packages/