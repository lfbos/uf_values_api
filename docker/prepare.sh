#!/bin/sh

set -ex

prepare () {
    pip install -U -r requirements.txt
}

prepare
