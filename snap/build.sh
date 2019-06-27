#!/bin/bash

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"

cd "$DIR"

docker build -t story-snapcraft .

docker run --rm -v $PWD/../:/story story-snapcraft /bin/sh -c 'cd /story && snapcraft clean && snapcraft'
