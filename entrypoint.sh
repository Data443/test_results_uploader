#!/bin/sh

set -e

export QASE_TOKEN=$QASE_TOKEN
python /app/main.py $*
