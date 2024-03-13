#! /bin/bash

source ./venv/bin/activate
python3 fe.py ./ ./facetemp
python3 cluster.py